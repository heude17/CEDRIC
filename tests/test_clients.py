from models import db
from models.client import Client


def test_create_client(auth_client, app):
    resp = auth_client.post(
        "/clients/nouveau",
        data={"nom": "Dupont Jean", "email": "jean@dupont.fr", "telephone": "0600000000"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "Dupont Jean" in resp.get_data(as_text=True)

    with app.app_context():
        assert Client.query.count() == 1


def test_edit_client(auth_client, client_id, app):
    resp = auth_client.post(
        f"/clients/{client_id}/modifier",
        data={"nom": "Nouveau Nom", "email": "new@test.fr"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "Nouveau Nom" in resp.get_data(as_text=True)

    with app.app_context():
        c = db.session.get(Client, client_id)
        assert c.nom == "Nouveau Nom"


def test_delete_client_cascades(auth_client, client_id, projet_id, zone_id, app):
    resp = auth_client.post(f"/clients/{client_id}/supprimer", follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        from models.projet import Projet
        from models.zone import Zone

        assert Client.query.count() == 0
        assert Projet.query.count() == 0
        assert Zone.query.count() == 0
