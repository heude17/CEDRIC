from tests.conftest import TECHNICIEN_EMAIL, TECHNICIEN_PASSWORD


def test_unauthenticated_redirects_to_login(client):
    resp = client.get("/clients/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/connexion" in resp.headers["Location"]


def test_wrong_password_rejected(client):
    resp = client.post(
        "/auth/connexion", data={"email": TECHNICIEN_EMAIL, "password": "wrong"}
    )
    assert resp.status_code == 200
    assert "incorrect" in resp.get_data(as_text=True).lower()


def test_login_then_access_and_logout(client):
    resp = client.post(
        "/auth/connexion",
        data={"email": TECHNICIEN_EMAIL, "password": TECHNICIEN_PASSWORD},
        follow_redirects=True,
    )
    assert resp.status_code == 200

    resp = client.get("/clients/")
    assert resp.status_code == 200

    resp = client.post("/auth/deconnexion", follow_redirects=True)
    assert resp.status_code == 200

    resp = client.get("/clients/", follow_redirects=False)
    assert resp.status_code == 302


def test_pdf_route_requires_login(client, projet_id):
    client.post("/auth/deconnexion")
    resp = client.get(f"/projets/{projet_id}/pdf", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/connexion" in resp.headers["Location"]
