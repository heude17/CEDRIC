def test_pdf_generation(auth_client, projet_id):
    resp = auth_client.get(f"/projets/{projet_id}/pdf")
    assert resp.status_code == 200
    assert resp.mimetype == "application/pdf"
    assert resp.data[:4] == b"%PDF"


def test_pdf_with_zone_and_composants(auth_client, projet_id, zone_id):
    resp = auth_client.get(f"/projets/{projet_id}/pdf")
    assert resp.status_code == 200
    assert resp.data[:4] == b"%PDF"
