from abc import ABC, abstractmethod
from typing import Dict, Any


class Module(ABC):
    """
    Abstract base class for all Prometheus modules.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = self.__class__.__name__
        self.id = self.name.lower().replace("module", "")
        self.category = "unknown"
        self.description = ""

    @abstractmethod
    def get_template(self) -> str:
        """
        Return the Python code template for this module.
        This will be inserted into the final payload.
        """
        pass

    @abstractmethod
    def get_config_schema(self) -> Dict[str, Any]:
        """
        Return the configuration schema for this module.
        Used for generating configuration UI.
        """
        return {
            "enabled": {"type": "boolean", "default": False, "label": "Enabled"},
        }

    def get_config(self) -> Dict[str, Any]:
        """Get the module's configuration."""
        return self.config

    def get_enabled(self) -> bool:
        """Check if this module is enabled."""
        return self.config.get("enabled", False)

    def set_enabled(self, enabled: bool):
        """Enable or disable this module."""
        self.config["enabled"] = enabled
