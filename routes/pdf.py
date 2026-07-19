import re

from flask import Blueprint, send_file

from models.projet import Projet
from services.pdf_generator import generate_projet_pdf

bp = Blueprint("pdf", __name__, url_prefix="/projets")


def _slugify(value):
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE).strip().lower()
    return re.sub(r"[\s-]+", "-", value) or "audit"


@bp.route("/<int:projet_id>/pdf")
def projet_pdf(projet_id):
    projet = Projet.query.get_or_404(projet_id)
    buffer = generate_projet_pdf(projet)
    filename = f"audit-{_slugify(projet.nom)}.pdf"
    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename,
    )
