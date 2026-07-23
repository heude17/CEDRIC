import base64
import io

from PIL import Image

from models import db
from models.projet import Projet
from models.validation import Validation


def _signature_data_uri():
    buf = io.BytesIO()
    Image.new("RGBA", (300, 100), (0, 0, 0, 0)).save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def _token(app, projet_id):
    with app.app_context():
        return db.session.get(Projet, projet_id).token


def test_validation_page_accessible_without_login(client, auth_client, app, projet_id):
    token = _token(app, projet_id)
    client.post("/auth/deconnexion")
    resp = client.get(f"/audit/valider/{token}")
    assert resp.status_code == 200


def test_validation_requires_signature(client, app, projet_id):
    token = _token(app, projet_id)
    resp = client.post(
        f"/audit/valider/{token}",
        data={"nom_signataire": "Jean", "confirmation": "y", "signature": ""},
    )
    assert resp.status_code == 200
    assert "signature" in resp.get_data(as_text=True).lower()

    with app.app_context():
        assert Validation.query.count() == 0


def test_validation_success_sets_statut_termine(client, app, projet_id):
    token = _token(app, projet_id)
    resp = client.post(
        f"/audit/valider/{token}",
        data={
            "nom_signataire": "Jean Dupont",
            "confirmation": "y",
            "signature": _signature_data_uri(),
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    with app.app_context():
        projet = db.session.get(Projet, projet_id)
        assert projet.statut == "termine"
        validation = Validation.query.first()
        assert validation.nom_signataire == "Jean Dupont"
        assert validation.signature.startswith("data:image/png;base64,")
