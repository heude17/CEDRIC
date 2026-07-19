from flask import Blueprint, abort, flash, redirect, render_template, url_for

from forms.audit_forms import ProjetForm
from models import db
from models.client import Client
from models.projet import Projet

bp = Blueprint("projets", __name__, url_prefix="/clients/<int:client_id>/projets")


@bp.route("/nouveau", methods=["GET", "POST"])
def nouveau(client_id):
    client = Client.query.get_or_404(client_id)
    form = ProjetForm()
    if form.validate_on_submit():
        projet = Projet(
            client_id=client.id,
            nom=form.nom.data,
            adresse_chantier=form.adresse_chantier.data,
            notes=form.notes.data,
        )
        db.session.add(projet)
        db.session.commit()
        flash(f"Projet « {projet.nom} » créé.", "success")
        return redirect(url_for("audit.projet_detail", projet_id=projet.id))
    return render_template("projets/form.html", form=form, client=client)


@bp.route("/<int:projet_id>")
def detail(client_id, projet_id):
    projet = Projet.query.get_or_404(projet_id)
    if projet.client_id != client_id:
        abort(404)
    return redirect(url_for("audit.projet_detail", projet_id=projet.id))
