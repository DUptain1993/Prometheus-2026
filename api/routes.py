from flask import Flask, request, jsonify, send_file
import os
import json
import logging
from pathlib import Path

from core.engine import Engine


class PrometheusAPI:
    """REST API for the Prometheus Offensive Framework."""

    def __init__(self, engine: Engine):
        self.engine = engine
        self.app = Flask(__name__)
        self.logger = logging.getLogger(__name__)

        self._register_routes()

    def _register_routes(self):
        """Register all API routes."""

        @self.app.route("/api/status", methods=["GET"])
        def status():
            """Check the API status."""
            return jsonify({
                "status": "online",
                "version": self.engine.config.get("version", "1.0.0"),
                "modules_loaded": len(self.engine.get_available_modules())
            })

        @self.app.route("/api/modules", methods=["GET"])
        def list_modules():
            """List all available modules."""
            return jsonify(self.engine.get_available_modules())

        @self.app.route("/api/modules/<module_id>/enable", methods=["POST"])
        def enable_module(module_id):
            """Enable a module."""
            data = request.json
            enabled = data.get("enabled", True)
            self.engine.enable_module(module_id, enabled)
            return jsonify({"status": "ok", "module": module_id, "enabled": enabled})

        @self.app.route("/api/config", methods=["GET", "POST"])
        def config():
            """Get or set configuration."""
            if request.method == "GET":
                return jsonify(self.engine.config)
            else:
                data = request.json
                self.engine.config.update(data)
                self.engine.save_config()
                return jsonify({"status": "ok"})

        @self.app.route("/api/build", methods=["POST"])
        def build():
            """Trigger a build."""
            data = request.json or {}
            if "webhook" in data:
                self.engine.set_webhook(data["webhook"])
            if "output" in data:
                self.engine.set_output_path(data["output"])
            if "type" in data:
                self.engine.set_payload_type(data["type"])
            
            success = self.engine.build()
            if success:
                output_path = self.engine.config["output_path"]
                if os.path.exists(output_path):
                    return send_file(output_path, as_attachment=True)
                return jsonify({"status": "success", "message": "Build completed"})
            else:
                return jsonify({"status": "error", "message": "Build failed"}), 500

        @self.app.route("/api/webhook", methods=["POST"])
        def webhook():
            """Set the webhook URL."""
            data = request.json
            if "url" not in data:
                return jsonify({"error": "url required"}), 400
            self.engine.set_webhook(data["url"])
            return jsonify({"status": "ok"})

    def run(self, host="0.0.0.0", port=5000):
        """Run the API server."""
        self.app.run(host=host, port=port, debug=False)
