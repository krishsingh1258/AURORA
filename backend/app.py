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

    # allow the Vite dev server (and production frontend) to call this API
    CORS(app, resources={r"/api/*": {"origins": "*"}})

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
    with app.app_context():
        db.create_all()  # creates tables if they don't exist yet
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)