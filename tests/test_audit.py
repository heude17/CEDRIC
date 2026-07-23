import re

from models import db
from models.zone import Zone


def test_create_zone_with_composants(auth_client, projet_id, app):
    resp = auth_client.post(
        f"/projets/{projet_id}/zones/nouvelle",
        data={
            "nom": "Cuisine",
            "type_piece": "cuisine",
            "surface_m2": "12",
            "composants-0-type_composant": "interrupteur",
            "composants-0-type_interrupteur": "va_et_vient",
            "composants-0-presence_neutre": "y",
            "composants-0-quantite": "2",
            "composants-1-type_composant": "volet_roulant",
            "composants-1-besoin_motorisation": "y",
            "composants-1-quantite": "1",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    with app.app_context():
        zone = Zone.query.first()
        assert zone.nom == "Cuisine"
        assert len(zone.composants) == 2
        types = {c.type_composant for c in zone.composants}
        assert types == {"interrupteur", "volet_roulant"}


def test_edit_zone_replaces_composants(auth_client, zone_id, app):
    resp = auth_client.post(
        f"/projets/zones/{zone_id}/modifier",
        data={
            "nom": "Salon Renove",
            "type_piece": "salon",
            "surface_m2": "22",
            "composants-0-type_composant": "eclairage",
            "composants-0-quantite": "3",
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200

    with app.app_context():
        zone = db.session.get(Zone, zone_id)
        assert zone.nom == "Salon Renove"
        assert len(zone.composants) == 1
        assert zone.composants[0].type_composant == "eclairage"


def test_delete_zone(auth_client, zone_id, app):
    resp = auth_client.post(f"/projets/zones/{zone_id}/supprimer", follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        assert Zone.query.count() == 0


def test_dynamic_composant_template_uses_dashed_field_names(auth_client, projet_id):
    """Régression : le template JS d'ajout de composant doit générer des noms de
    champs 'composants-N-xxx' (avec tirets), sinon les composants ajoutés via le
    bouton "+ Ajouter un composant" ne sont jamais rattachés à la pièce."""
    resp = auth_client.get(f"/projets/{projet_id}/zones/nouvelle")
    html = resp.get_data(as_text=True)

    template_match = re.search(
        r'<template id="composant-template">(.*?)</template>', html, re.DOTALL
    )
    assert template_match, "template#composant-template introuvable dans la page"
    template_html = template_match.group(1)

    assert 'name="composants-__INDEX__-type_composant"' in template_html
    assert 'name="composants-__INDEX__-quantite"' in template_html
    # jamais de concaténation sans tiret
    assert "__INDEX__quantite" not in template_html
    assert "__INDEX__type_composant" not in template_html
