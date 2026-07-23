import pytest

from app import _ensure_default_technicien, create_app
from config import Config
from models import db as _db

TECHNICIEN_EMAIL = "tech@test.fr"
TECHNICIEN_PASSWORD = "secret123"


def _make_test_config(upload_dir):
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        WTF_CSRF_ENABLED = False
        SECRET_KEY = "test-secret-key"
        TECHNICIEN_EMAIL = TECHNICIEN_EMAIL
        TECHNICIEN_PASSWORD = TECHNICIEN_PASSWORD
        UPLOAD_FOLDER = str(upload_dir)

    return TestConfig


@pytest.fixture
def app(tmp_path):
    config_class = _make_test_config(tmp_path / "uploads")
    application = create_app(config_class)

    with application.app_context():
        _db.create_all()
        _ensure_default_technicien(application)
        yield application
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    client.post(
        "/auth/connexion",
        data={"email": TECHNICIEN_EMAIL, "password": TECHNICIEN_PASSWORD},
    )
    return client


@pytest.fixture
def client_id(auth_client):
    auth_client.post("/clients/nouveau", data={"nom": "Client Test"})
    return 1


@pytest.fixture
def projet_id(auth_client, client_id):
    auth_client.post(
        f"/clients/{client_id}/projets/nouveau",
        data={"nom": "Projet Test", "adresse_chantier": "1 rue du Test"},
    )
    return 1


@pytest.fixture
def zone_id(auth_client, projet_id):
    auth_client.post(
        f"/projets/{projet_id}/zones/nouvelle",
        data={
            "nom": "Salon",
            "type_piece": "salon",
            "surface_m2": "20",
            "composants-0-type_composant": "prise",
            "composants-0-quantite": "1",
        },
    )
    return 1
