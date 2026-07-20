import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'audit.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "zones")
    ALLOWED_PHOTO_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # 20 Mo par requête (plusieurs photos)

    TECHNICIEN_EMAIL = os.environ.get("TECHNICIEN_EMAIL", "technicien@exemple.fr")
    TECHNICIEN_PASSWORD = os.environ.get("TECHNICIEN_PASSWORD", "changez-moi")
