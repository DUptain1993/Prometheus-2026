@echo off
:: ============================================
:: Prometheus Framework - Install Script (Windows)
:: ============================================

echo 🚀 Installing Prometheus Offensive Framework...

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

:: Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo 📥 Installing dependencies...
if "%1"=="--full" (
    pip install -r requirements.txt
) else if "%1"=="--minimal" (
    pip install -r requirements_minimal.txt
) else if "%1"=="--telegram" (
    pip install -r requirements_telegram.txt
) else (
    pip install -r requirements.txt
)

:: Create directories
echo 📁 Creating directories...
mkdir output logs config 2>nul

:: Copy example config
if not exist config\config.json (
    copy config\config.example.json config\config.json
    echo ⚠️  Please edit config\config.json with your settings
)

echo ✅ Installation complete!
echo.
echo Run with: python main.py
echo For Telegram mode: python main.py --telegram --config config/config.json
pause
