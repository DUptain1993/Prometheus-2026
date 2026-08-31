prometheus/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── main.py
├── core/
│   ├── __init__.py
│   ├── engine.py          # The heart of the framework
│   ├── crypto.py          # AES-256-GCM, key derivation, secure storage
│   ├── telemetry.py       # Usage analytics (optional, anonymous)
│   ├── orchestrator.py    # Manages payload generation pipeline
│   └── utils.py           # Cross-platform utilities
├── payload/
│   ├── __init__.py
│   ├── templates/         # Jinja2 templates for payload generation
│   │   ├── base.py.j2
│   │   ├── stealer.py.j2
│   │   ├── ransomware.py.j2
│   │   └── rat.py.j2
│   ├── compiler.py        # PyInstaller wrapper
│   └── obfuscator.py      # AST-based obfuscation
├── modules/
│   ├── __init__.py
│   ├── base.py            # Abstract Module class
│   ├── stealer/
│   │   ├── system.py
│   │   ├── browser.py
│   │   ├── discord.py
│   │   └── crypto_wallets.py
│   ├── malware/
│   │   ├── block.py
│   │   ├── persistence.py
│   │   ├── rat.py
│   │   └── ransomware.py
│   └── registry.py        # Module discovery and management
├── gui/
│   ├── __init__.py
│   ├── app.py             # Main window
│   ├── dashboard.py       # Overview panel
│   ├── module_panel.py    # Module management
│   └── settings.py        # Global configuration
├── api/                    # REST API for headless operation
│   ├── __init__.py
│   ├── routes.py
│   └── models.py
├── tests/
│   ├── unit/
│   └── integration/
├── output/
│   └── .gitkeep
├── logs/
│   └── .gitkeep
└── .dockerignore
