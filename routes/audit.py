from flask import Blueprint, flash, redirect, render_template, url_for

from forms.audit_forms import ComposantForm, ZoneForm
from models import db
from models.composant import Composant
from models.projet import Projet
from models.zone import Zone
from routes.auth import require_login
from services.uploads import remove_zone_files

bp = Blueprint("audit", __name__, url_prefix="/projets")
bp.before_request(require_login)


@bp.route("/<int:projet_id>")
def projet_detail(projet_id):
    projet = Projet.query.get_or_404(projet_id)
    return render_template("audit/projet_detail.html", projet=projet)


@bp.route("/<int:projet_id>/zones/nouvelle", methods=["GET", "POST"])
def nouvelle_zone(projet_id):
    projet = Projet.query.get_or_404(projet_id)
    form = ZoneForm()

    if form.validate_on_submit():
        zone = Zone(
            projet_id=projet.id,
            nom=form.nom.data,
            type_piece=form.type_piece.data,
            surface_m2=form.surface_m2.data,
            notes=form.notes.data,
        )
        zone.composants = [_composant_from_form(cf.form) for cf in form.composants.entries]
        db.session.add(zone)
        db.session.commit()
        flash(f"Pièce « {zone.nom} » enregistrée avec {len(zone.composants)} composant(s).", "success")
        return redirect(url_for("audit.zone_detail", zone_id=zone.id))

    return render_template(
        "audit/nouvelle_zone.html",
        form=form,
        projet=projet,
        zone=None,
        composant_template=ComposantForm(prefix="composants-__INDEX__-"),
    )


@bp.route("/zones/<int:zone_id>")
def zone_detail(zone_id):
    zone = Zone.query.get_or_404(zone_id)
    return render_template("audit/zone_detail.html", zone=zone)


@bp.route("/zones/<int:zone_id>/modifier", methods=["GET", "POST"])
def modifier_zone(zone_id):
    zone = Zone.query.get_or_404(zone_id)
    form = ZoneForm(obj=zone)

    if form.validate_on_submit():
        zone.nom = form.nom.data
        zone.type_piece = form.type_piece.data
        zone.surface_m2 = form.surface_m2.data
        zone.notes = form.notes.data
        zone.composants = [_composant_from_form(cf.form) for cf in form.composants.entries]
        db.session.commit()
        flash(f"Pièce « {zone.nom} » mise à jour.", "success")
        return redirect(url_for("audit.zone_detail", zone_id=zone.id))

    return render_template(
        "audit/nouvelle_zone.html",
        form=form,
        projet=zone.projet,
        zone=zone,
        composant_template=ComposantForm(prefix="composants-__INDEX__-"),
    )


@bp.route("/zones/<int:zone_id>/supprimer", methods=["POST"])
def supprimer_zone(zone_id):
    zone = Zone.query.get_or_404(zone_id)
    projet_id = zone.projet_id
    nom = zone.nom

    remove_zone_files(zone.id)

    db.session.delete(zone)
    db.session.commit()
    flash(f"Pièce « {nom} » supprimée.", "success")
    return redirect(url_for("audit.projet_detail", projet_id=projet_id))


def _composant_from_form(composant_form):
    return Composant(
        type_composant=composant_form.type_composant.data,
        type_interrupteur=composant_form.type_interrupteur.data,
        presence_neutre=composant_form.presence_neutre.data,
        besoin_motorisation=composant_form.besoin_motorisation.data,
        quantite=composant_form.quantite.data,
        notes=composant_form.notes.data,
    )
