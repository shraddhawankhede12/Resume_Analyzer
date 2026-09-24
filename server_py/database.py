import os
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_URL = "sqlite:///" + os.path.join(BASE_DIR, "resume_analyzer.db").replace("\\", "/")


def database_url() -> str:
    url = os.getenv("DATABASE_URL", DEFAULT_DB_URL)
    # Render/Heroku hand out postgres:// URLs, SQLAlchemy needs postgresql://
    return url.replace("postgres://", "postgresql://", 1) if url.startswith("postgres://") else url


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False, default="")
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_login_at = db.Column(db.DateTime, nullable=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {"id": self.id, "email": self.email, "name": self.name}
