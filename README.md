# adbc

A small Python utility that auto-discovers and connects to Android devices over ADB wireless debugging using mDNS/Zeroconf, eliminating the need to manually enter IP addresses. Compatible with Windows, macOS, and Linux.

## Prerequisites

- **ADB:** Must be installed and available on your `PATH`.
- **Android 11+:** Device must have **Wireless debugging** enabled. (Note: This is not compatible with legacy "ADB over WiFi" on older devices).
- **Paired:** Your device must already be **paired** with your machine (Settings → Developer options → Wireless debugging → Pair device with pairing code).

## Installation

Install via `uvx` or `pipx` (recommended):

```bash
uv tool install git+https://github.com/mwdle/adbc.git
# OR
pipx install git+https://github.com/mwdle/adbc.git
```

> `pipx` installs CLI tools in an isolated environment and exposes them globally — no virtualenv management required. Install it with `pip install pipx` if you don't have it. Alternatively, use `pip install git+https://github.com/mwdle/adbc.git` inside an active virtual environment.

## Usage

```bash
adbc
```

**How it works:**

- **Discovery:** The script scans your local network for ADB-over-Wi-Fi services for up to 5 seconds.
- **Auto-Connect:** If only one device is found, it connects automatically.
- **Interactive Menu:** If multiple devices are found, you can enter a number, a list (e.g. `1 2` or `1,2`), or `a` for all.

**Example Output:**

```text
me@mypc:~$ adbc
Discovering devices...
[1] Android-2.local (192.168.0.100:41061)
[2] Android.local (192.168.0.91:41624)

Enter number(s), or 'a' for all: a
connected to 192.168.0.100:41061
connected to 192.168.0.91:41624
```

## Troubleshooting

- **No devices found:** Ensure your PC and phone are on the exact same Wi-Fi network. Some public or corporate networks use "AP Isolation" which blocks devices from seeing each other.
- **Command succeeds but fails to connect:** Your PC's RSA key is likely not authorized. Run `adb pair <ip>:<pairing_port>` manually once and accept the prompt on your device to establish trust.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
