from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from forms.audit_forms import LoginForm
from models.technicien import Technicien

bp = Blueprint("auth", __name__, url_prefix="/auth")


def require_login():
    """À enregistrer via bp.before_request sur les blueprints internes (non publics)."""
    if not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()


@bp.route("/connexion", methods=["GET", "POST"])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for("clients.liste"))

    form = LoginForm()
    if form.validate_on_submit():
        technicien = Technicien.query.filter_by(email=form.email.data.strip().lower()).first()
        if technicien and technicien.check_password(form.password.data):
            login_user(technicien)
            next_url = request.args.get("next")
            return redirect(next_url or url_for("clients.liste"))
        flash("Email ou mot de passe incorrect.", "error")

    return render_template("auth/connexion.html", form=form)


@bp.route("/deconnexion", methods=["POST"])
@login_required
def deconnexion():
    logout_user()
    flash("Vous avez été déconnecté.", "success")
    return redirect(url_for("auth.connexion"))
