#!/bin/bash
# ============================================
# Prometheus Framework - Install Script
# ============================================

set -e

echo "🚀 Installing Prometheus Offensive Framework..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
if [ "$1" == "--full" ]; then
    pip install -r requirements.txt
elif [ "$1" == "--minimal" ]; then
    pip install -r requirements_minimal.txt
elif [ "$1" == "--telegram" ]; then
    pip install -r requirements_telegram.txt
else
    pip install -r requirements.txt
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p output logs config

# Copy example config
if [ ! -f "config/config.json" ]; then
    cp config/config.example.json config/config.json
    echo "⚠️  Please edit config/config.json with your settings"
fi

# Set permissions
chmod +x main.py

echo "✅ Installation complete!"
echo ""
echo "Run with: python main.py"
echo "For Telegram mode: python main.py --telegram --config config/config.json"
