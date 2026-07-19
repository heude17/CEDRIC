from flask import Blueprint, flash, redirect, render_template, url_for

from forms.audit_forms import ComposantForm, ZoneForm
from models import db
from models.projet import Projet
from models.zone import Zone

bp = Blueprint("audit", __name__, url_prefix="/projets")


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
        for composant_form in form.composants.entries:
            zone.composants.append(_composant_from_form(composant_form.form))
        db.session.add(zone)
        db.session.commit()
        flash(f"Pièce « {zone.nom} » enregistrée avec {len(zone.composants)} composant(s).", "success")
        return redirect(url_for("audit.zone_detail", zone_id=zone.id))

    composant_template = ComposantForm(prefix="composants-__INDEX__")
    return render_template(
        "audit/nouvelle_zone.html",
        form=form,
        projet=projet,
        composant_template=composant_template,
    )


@bp.route("/zones/<int:zone_id>")
def zone_detail(zone_id):
    zone = Zone.query.get_or_404(zone_id)
    return render_template("audit/zone_detail.html", zone=zone)


def _composant_from_form(composant_form):
    from models.composant import Composant

    return Composant(
        type_composant=composant_form.type_composant.data,
        type_interrupteur=composant_form.type_interrupteur.data,
        presence_neutre=composant_form.presence_neutre.data,
        besoin_motorisation=composant_form.besoin_motorisation.data,
        quantite=composant_form.quantite.data,
        notes=composant_form.notes.data,
    )
