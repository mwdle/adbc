#!/usr/bin/env python3

import subprocess
import time
import socket
from zeroconf import ServiceBrowser, Zeroconf
import re

DISCOVERY_TIMEOUT = 5
DEBOUNCE_WAIT = 1.25
ADB_SERVICE_TYPE = "_adb-tls-connect._tcp.local."

class AdbServiceListener:
    def __init__(self):
        self.found_devices = {}
        self.last_discovery_time = 0

    def remove_service(self, zeroconf, type, name):
        self.found_devices.pop(name, None)

    def update_service(self, zeroconf, type, name):
        self.add_service(zeroconf, type, name)

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            self.found_devices[name] = info
            self.last_discovery_time = time.monotonic()

def get_ipv4_address(info) -> str | None:
    if not info or not info.addresses: return None
    for addr in info.addresses:
        try: 
            return socket.inet_ntoa(addr)
        except (OSError, AttributeError): continue
    return None

def connect_to_device(device):
    command = ["adb", "connect", f"{device['ip']}:{device['port']}"]
    try:
        subprocess.run(command, check=True)
    except FileNotFoundError:
        print("Error: 'adb' command not found. Ensure it is in your system's PATH.")
    except subprocess.CalledProcessError:
        pass
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def prompt_for_device_selection(choices):
    if not choices:
        return []

    if len(choices) == 1:
        return [choices[0]]

    for i, device in enumerate(choices):
        print(f"[{i+1}] {device['name']} ({device['ip']}:{device['port']})")
    
    try:
        prompt = "Enter number(s), or 'a' for all: "
        user_input = input(prompt).lower().strip()

        if user_input in ['a', 'all']:
            return choices
        
        if not user_input:
            return []
            
        selected_devices = []
        selected_indices = [int(i.strip()) - 1 for i in re.split(r'[,\s]+', user_input)]
        for index in selected_indices:
            if 0 <= index < len(choices):
                if choices[index] not in selected_devices:
                    selected_devices.append(choices[index])
        return selected_devices

    except (ValueError, KeyboardInterrupt):
        return []

def find_and_connect():
    zeroconf = Zeroconf()
    listener = AdbServiceListener()
    ServiceBrowser(zeroconf, ADB_SERVICE_TYPE, listener)

    print("Discovering devices...")
    
    start_time = time.monotonic()
    
    while time.monotonic() - start_time < DISCOVERY_TIMEOUT:
        if listener.found_devices and (time.monotonic() - listener.last_discovery_time > DEBOUNCE_WAIT):
            break
        time.sleep(0.1)

    zeroconf.close()

    if not listener.found_devices:
        print("No devices found. Ensure 'Wireless debugging' is enabled and you are paired.")
        return

    choices = {}
    for info in sorted(listener.found_devices.values(), key=lambda i: i.server):
        ip_address = get_ipv4_address(info)
        if ip_address:
            device_key = f"{info.server.rstrip('.')}-{ip_address}"
            choices[device_key] = {
                "name": info.server.rstrip('.'),
                "ip": ip_address,
                "port": info.port
            }

    devices_to_connect = prompt_for_device_selection(list(choices.values()))

    if not devices_to_connect:
        print("No valid devices were selected.")
        return

    for device in devices_to_connect:
        connect_to_device(device)

if __name__ == "__main__":
    find_and_connect()