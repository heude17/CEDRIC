import os
import uuid

from flask import Blueprint, current_app, flash, redirect, request, url_for
from werkzeug.utils import secure_filename

from models import db
from models.photo import Photo
from models.zone import Zone
from routes.auth import require_login
from services.uploads import zone_upload_folder

bp = Blueprint("photos", __name__, url_prefix="/projets/zones")
bp.before_request(require_login)


def _extension_allowed(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_PHOTO_EXTENSIONS"]
    )


@bp.route("/<int:zone_id>/photos", methods=["POST"])
def ajouter(zone_id):
    zone = Zone.query.get_or_404(zone_id)
    fichiers = [f for f in request.files.getlist("photos") if f and f.filename]

    if not fichiers:
        flash("Aucune photo sélectionnée.", "error")
        return redirect(url_for("audit.zone_detail", zone_id=zone.id))

    zone_folder = zone_upload_folder(zone.id)
    os.makedirs(zone_folder, exist_ok=True)

    ajoutees = 0
    for fichier in fichiers:
        if not _extension_allowed(fichier.filename):
            continue
        extension = fichier.filename.rsplit(".", 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{extension}"
        fichier.save(os.path.join(zone_folder, secure_filename(filename)))
        db.session.add(Photo(zone_id=zone.id, filename=filename))
        ajoutees += 1

    if ajoutees:
        db.session.commit()
        flash(f"{ajoutees} photo(s) ajoutée(s).", "success")
    else:
        flash("Format non supporté (utilisez JPG, PNG ou WEBP).", "error")

    return redirect(url_for("audit.zone_detail", zone_id=zone.id))


@bp.route("/photos/<int:photo_id>/supprimer", methods=["POST"])
def supprimer(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    zone_id = photo.zone_id

    chemin = os.path.join(zone_upload_folder(zone_id), photo.filename)
    if os.path.exists(chemin):
        os.remove(chemin)

    db.session.delete(photo)
    db.session.commit()
    flash("Photo supprimée.", "success")
    return redirect(url_for("audit.zone_detail", zone_id=zone_id))
