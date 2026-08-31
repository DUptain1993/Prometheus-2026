"""
Abstract Command & Control Interface
Provides a unified API for different C2 backends (Telegram, Discord, HTTP, etc.)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from enum import Enum


class MessageType(Enum):
    """Types of messages that can be sent via C2."""
    STATUS = "status"
    DATA = "data"
    FILE = "file"
    COMMAND = "command"
    RESPONSE = "response"
    ERROR = "error"


@dataclass
class C2Message:
    """Standardized message format for C2 communication."""
    type: MessageType
    content: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__('time').time())


class C2Backend(ABC):
    """
    Abstract base class for C2 backends.
    Implement this to support different communication channels.
    """

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the C2 backend connection."""
        pass

    @abstractmethod
    def send_message(self, message: C2Message) -> bool:
        """Send a message through the C2 channel."""
        pass

    @abstractmethod
    def receive_messages(self, timeout: int = 30) -> List[C2Message]:
        """Receive messages from the C2 channel."""
        pass

    @abstractmethod
    def send_file(self, file_path: str, filename: str = None) -> bool:
        """Send a file through the C2 channel."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if the C2 connection is active."""
        pass

    @abstractmethod
    def close(self):
        """Close the C2 connection."""
        pass


class C2Manager:
    """
    Manages C2 backends and provides a unified interface.
    Supports fallback mechanisms.
    """

    def __init__(self):
        self.backends: List[C2Backend] = []
        self.primary_backend: Optional[C2Backend] = None
        self._message_handlers: Dict[MessageType, List[Callable]] = {
            msg_type: [] for msg_type in MessageType
        }

    def register_backend(self, backend: C2Backend, primary: bool = False):
        """Register a C2 backend."""
        self.backends.append(backend)
        if primary or self.primary_backend is None:
            self.primary_backend = backend

    def initialize_all(self) -> bool:
        """Initialize all registered backends."""
        success = False
        for backend in self.backends:
            try:
                if backend.initialize():
                    success = True
                    print(f"[C2] Initialized: {backend.__class__.__name__}")
            except Exception as e:
                print(f"[C2] Failed to initialize {backend.__class__.__name__}: {e}")
        return success

    def send_message(self, message: C2Message, use_primary: bool = True) -> bool:
        """Send a message using available backends."""
        if use_primary and self.primary_backend:
            try:
                return self.primary_backend.send_message(message)
            except Exception as e:
                print(f"[C2] Primary backend failed: {e}")

        # Try all backends
        for backend in self.backends:
            if backend is self.primary_backend:
                continue
            try:
                if backend.send_message(message):
                    return True
            except Exception:
                continue
        return False

    def send_file(self, file_path: str, filename: str = None) -> bool:
        """Send a file using the primary backend."""
        if self.primary_backend:
            try:
                return self.primary_backend.send_file(file_path, filename)
            except Exception as e:
                print(f"[C2] Failed to send file: {e}")
        return False

    def register_handler(self, message_type: MessageType, handler: Callable):
        """Register a message handler."""
        self._message_handlers[message_type].append(handler)

    def poll_messages(self, timeout: int = 5):
        """Poll for incoming messages and dispatch to handlers."""
        if self.primary_backend:
            try:
                messages = self.primary_backend.receive_messages(timeout)
                for msg in messages:
                    for handler in self._message_handlers.get(msg.type, []):
                        try:
                            handler(msg)
                        except Exception as e:
                            print(f"[C2] Handler error: {e}")
            except Exception as e:
                print(f"[C2] Poll error: {e}")

    def close_all(self):
        """Close all backends."""
        for backend in self.backends:
            try:
                backend.close()
            except Exception:
                pass
