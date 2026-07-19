from flask import Blueprint, flash, redirect, render_template, url_for

from forms.audit_forms import ClientForm
from models import db
from models.client import Client

bp = Blueprint("clients", __name__, url_prefix="/clients")


@bp.route("/")
def liste():
    clients = Client.query.order_by(Client.created_at.desc()).all()
    return render_template("clients/liste.html", clients=clients)


@bp.route("/nouveau", methods=["GET", "POST"])
def nouveau():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client(
            nom=form.nom.data,
            email=form.email.data,
            telephone=form.telephone.data,
            adresse=form.adresse.data,
            notes=form.notes.data,
        )
        db.session.add(client)
        db.session.commit()
        flash(f"Client « {client.nom} » créé.", "success")
        return redirect(url_for("clients.detail", client_id=client.id))
    return render_template("clients/form.html", form=form)


@bp.route("/<int:client_id>")
def detail(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template("clients/detail.html", client=client)
