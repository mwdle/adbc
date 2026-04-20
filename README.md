# adbc

A small Python utility that auto-discovers and connects to Android devices over ADB wireless debugging using mDNS/Zeroconf, eliminating the need to manually enter IP addresses. Compatible with Windows, macOS, and Linux.

## Prerequisites

- **ADB:** Must be installed and available on your `PATH`.
- **Android 11+:** Device must have **Wireless debugging** enabled. (Note: This is not compatible with legacy "ADB over WiFi" on older devices).
- **Paired:** Your device must already be **paired** with your machine (Settings → Developer options → Wireless debugging → Pair device with pairing code).
- **Python 3** with dependencies installed:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

If you have set the script as executable, you can run it directly. Otherwise, use `python3`:

```bash
./adbc.py
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

> **Tip:** To invoke the script as just `adbc` from anywhere, you can add a shell alias or create a small wrapper script on your `PATH`. Refer to your OS and shell's documentation for the exact steps.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
