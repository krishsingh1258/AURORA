import os
from flask import Flask
from flask_cors import CORS

from config import Config
from models import db
from routes.auth import auth_bp
from routes.chat import chat_bp
from routes.schemes import schemes_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable full CORS for frontend cross-origin requests
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(schemes_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return {"status": "ok"}, 200

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
