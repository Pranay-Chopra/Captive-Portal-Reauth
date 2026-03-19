# Captive Portal Auto Reauth (Linux)

A lightweight script + systemd service that automatically re-authenticates you on captive portal networks (like college WiFi) when your session expires.

No GUI. No nonsense. Just keeps your internet alive.

---

## Features

- Detects connection loss
- Automatically re-authenticates via browser automation
- Runs in background using systemd (user service)
- Logs everything via journald
- Minimal dependencies

---

## Requirements

- Linux (with systemd)
- Python 3
- pip

---

## Installation

### 1. Extract the tarball

```bash
tar -xzf portal-reauth.tar.gz
cd portal-reauth
```

---

### 2. Run installer

```bash
make install
```

You will be prompted for:
- Username
- Password

---

### 3. Done

The service will start automatically and keep running in the background.

---

## Usage

### Check service status

```bash
systemctl --user status portal-reauth.service
```

---

### View logs

```bash
journalctl --user -u portal-reauth.service -f
```

---

### Stop service

```bash
systemctl --user stop portal-reauth.service
```

---

### Restart service

```bash
systemctl --user restart portal-reauth.service
```

---

## How It Works

- Periodically checks if internet is accessible
- If not, opens captive portal using Playwright
- Waits briefly for portal to initialize
- Performs login automatically
- Repeats as needed

---

## Dependencies

PIP dependencies:
- playwright
- systemd-python
- requests

Playwright dependencies:
- libicu74
- libflite1
- libxml2

The script tries to manage the dependencies for you, but manual intervention may be needed.
It does this by pip-installing and then running:

```bash
playwright install
```

---

## Notes

- Credentials are stored locally in the installed script
- Designed for a specific captive portal system (may require tweaks for others)
- Uses a small delay (~2s) to handle portal initialization timing

---

## Uninstall

```bash
make uninstall
```

---

## Disclaimer

This tool is intended for personal use on networks you are authorized to access.

---

## License

MIT (or don’t, no one’s stopping you)
