from flask import Blueprint, flash, redirect, render_template, url_for

from forms.audit_forms import ValidationForm
from models import db
from models.projet import Projet
from models.validation import Validation

bp = Blueprint("validation", __name__, url_prefix="/audit")


@bp.route("/valider/<token>", methods=["GET", "POST"])
def valider(token):
    projet = Projet.query.filter_by(token=token).first_or_404()
    form = ValidationForm()

    if form.validate_on_submit():
        validation = Validation(
            projet_id=projet.id,
            nom_signataire=form.nom_signataire.data,
            email_signataire=form.email_signataire.data,
            commentaire=form.commentaire.data,
        )
        db.session.add(validation)
        projet.statut = "termine"
        db.session.commit()
        flash("Merci, l'audit a bien été validé.", "success")
        return redirect(url_for("validation.valider", token=token))

    return render_template(
        "validation/valider.html", projet=projet, form=form, validation=projet.derniere_validation
    )
