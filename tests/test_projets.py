from models.projet import Projet


def test_create_projet(auth_client, client_id, app):
    resp = auth_client.post(
        f"/clients/{client_id}/projets/nouveau",
        data={"nom": "Villa X", "adresse_chantier": "2 rue du Chantier"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "Villa X" in resp.get_data(as_text=True)

    with app.app_context():
        projet = Projet.query.first()
        assert projet.statut == "brouillon"
        assert projet.token  # généré automatiquement


def test_edit_projet(auth_client, client_id, projet_id, app):
    resp = auth_client.post(
        f"/clients/{client_id}/projets/{projet_id}/modifier",
        data={"nom": "Villa Renovee"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "Villa Renovee" in resp.get_data(as_text=True)


def test_delete_projet_cascades_zones(auth_client, client_id, projet_id, zone_id, app):
    resp = auth_client.post(
        f"/clients/{client_id}/projets/{projet_id}/supprimer", follow_redirects=True
    )
    assert resp.status_code == 200

    with app.app_context():
        from models.zone import Zone

        assert Projet.query.count() == 0
        assert Zone.query.count() == 0
