import os
import importlib
import inspect
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from .base import Module


class ModuleRegistry:
    """
    Discovers, loads, and manages all available modules.
    """

    def __init__(self, module_dir: str = "modules"):
        self.logger = logging.getLogger(__name__)
        self.module_dir = Path(module_dir)
        self._modules: Dict[str, Any] = {}
        self._manifest: Dict[str, Dict[str, Any]] = {}
        self._loaded = False

    def discover_modules(self):
        """Discover and load all modules from the modules directory."""
        if self._loaded:
            return

        self._modules = {}
        self._manifest = {}

        if not self.module_dir.exists():
            self.logger.warning(f"Module directory {self.module_dir} does not exist.")
            return

        # Import all Python files in the modules directory
        for file_path in self.module_dir.rglob("*.py"):
            if file_path.name == "__init__.py":
                continue

            try:
                # Convert file path to module name
                rel_path = file_path.relative_to(self.module_dir)
                module_name = "modules." + ".".join(rel_path.with_suffix("").parts)

                # Import the module
                module = importlib.import_module(module_name)

                # Find all Module subclasses
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Module) and obj is not Module:
                        # Instantiate the module with default config
                        instance = obj({})
                        self._modules[instance.id] = instance
                        self._manifest[instance.id] = {
                            "name": instance.name,
                            "category": getattr(instance, "category", "unknown"),
                            "description": getattr(instance, "description", ""),
                            "enabled": False,
                            "path": str(file_path),
                        }
                        self.logger.debug(f"Loaded module: {instance.name} ({instance.id})")

            except Exception as e:
                self.logger.error(f"Failed to load module {file_path}: {e}")

        self._loaded = True
        self.logger.info(f"Loaded {len(self._modules)} modules")

    def get_manifest(self) -> Dict[str, Dict[str, Any]]:
        """Get the module manifest."""
        if not self._loaded:
            self.discover_modules()
        return self._manifest

    def get_module(self, module_id: str) -> Optional[Module]:
        """Get a module instance by ID."""
        if not self._loaded:
            self.discover_modules()
        return self._modules.get(module_id)

    def get_template(self, module_id: str) -> Optional[str]:
        """Get the template code for a module."""
        module = self.get_module(module_id)
        if module:
            return module.get_template()
        return None

    def get_enabled_modules(self) -> List[Module]:
        """Get all enabled modules."""
        return [m for m in self._modules.values() if m.get_enabled()]

    def __len__(self):
        return len(self._modules)
