import os

from flask import Flask, redirect, render_template, url_for
from flask_login import LoginManager
from flask_wtf import CSRFProtect

from config import Config
from models import db

csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.connexion"
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
login_manager.login_message_category = "error"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from models.technicien import Technicien

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Technicien, int(user_id))

    from routes.audit import bp as audit_bp
    from routes.auth import bp as auth_bp
    from routes.clients import bp as clients_bp
    from routes.pdf import bp as pdf_bp
    from routes.photos import bp as photos_bp
    from routes.projets import bp as projets_bp
    from routes.validation import bp as validation_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(projets_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(photos_bp)
    app.register_blueprint(validation_bp)

    @app.route("/")
    def index():
        return redirect(url_for("clients.liste"))

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    with app.app_context():
        db.create_all()
        _ensure_default_technicien(app)

    return app


def _ensure_default_technicien(app):
    from models.technicien import Technicien

    if Technicien.query.count() > 0:
        return
    technicien = Technicien(nom="Technicien", email=app.config["TECHNICIEN_EMAIL"])
    technicien.set_password(app.config["TECHNICIEN_PASSWORD"])
    db.session.add(technicien)
    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
