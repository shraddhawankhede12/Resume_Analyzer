import logging
import os
import time
import uuid

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, g, jsonify, request  # noqa: E402
from flask_cors import CORS  # noqa: E402

from database import database_url, db  # noqa: E402
from errors import ApiError  # noqa: E402
from logging_config import print_startup_banner, setup_logging  # noqa: E402
from routes.analyze import bp as analyze_bp  # noqa: E402
from routes.auth import bp as auth_bp  # noqa: E402
from services.llm_service import MODEL  # noqa: E402

setup_logging()
http_log = logging.getLogger("resume.http")


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url()
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB upload cap

    CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","))
    db.init_app(app)
    with app.app_context():
        db.create_all()  # creates the users table on first start

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(analyze_bp, url_prefix="/api")

    @app.before_request
    def start_request():
        g.req_id = uuid.uuid4().hex[:8]
        g.start = time.perf_counter()
        http_log.info("[%s] --> %s %s", g.req_id, request.method, request.path)

    @app.after_request
    def end_request(response):
        http_log.info(
            "[%s] <-- %s %s status=%s %.0fms",
            g.get("req_id", "-"), request.method, request.path, response.status_code,
            (time.perf_counter() - g.get("start", time.perf_counter())) * 1000,
        )
        return response

    @app.errorhandler(ApiError)
    def handle_api_error(err: ApiError):
        return jsonify({"detail": err.detail}), err.status_code

    @app.errorhandler(413)
    def too_large(_):
        return jsonify({"detail": "Upload too large (max 10 MB)."}), 413

    @app.errorhandler(Exception)
    def handle_unexpected(err):
        if hasattr(err, "code") and hasattr(err, "description"):  # werkzeug HTTPException
            return jsonify({"detail": err.description}), err.code
        http_log.exception("[%s] unhandled error", g.get("req_id", "-"))
        return jsonify({"detail": "Internal server error."}), 500

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "message": "Neural Engine Core Online"})

    print_startup_banner(MODEL, os.getenv("PORT", "5000"), app.config["SQLALCHEMY_DATABASE_URI"])
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
