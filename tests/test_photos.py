import io
import os

from PIL import Image

from models.photo import Photo
from services.uploads import zone_upload_folder


def _jpeg_bytes():
    buf = io.BytesIO()
    Image.new("RGB", (100, 80), (10, 20, 30)).save(buf, format="JPEG")
    buf.seek(0)
    return buf


def test_upload_photo(auth_client, app, zone_id):
    resp = auth_client.post(
        f"/projets/zones/{zone_id}/photos",
        data={"photos": [(_jpeg_bytes(), "photo.jpg")]},
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert resp.status_code == 200

    with app.app_context():
        photos = Photo.query.all()
        assert len(photos) == 1
        chemin = os.path.join(zone_upload_folder(zone_id), photos[0].filename)
        assert os.path.exists(chemin)


def test_reject_invalid_extension(auth_client, app, zone_id):
    resp = auth_client.post(
        f"/projets/zones/{zone_id}/photos",
        data={"photos": [(io.BytesIO(b"not an image"), "evil.exe")]},
        content_type="multipart/form-data",
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert "non support" in resp.get_data(as_text=True).lower()

    with app.app_context():
        assert Photo.query.count() == 0


def test_delete_photo(auth_client, app, zone_id):
    auth_client.post(
        f"/projets/zones/{zone_id}/photos",
        data={"photos": [(_jpeg_bytes(), "photo.jpg")]},
        content_type="multipart/form-data",
    )
    with app.app_context():
        photo_id = Photo.query.first().id

    resp = auth_client.post(f"/projets/zones/photos/{photo_id}/supprimer", follow_redirects=True)
    assert resp.status_code == 200

    with app.app_context():
        assert Photo.query.count() == 0
