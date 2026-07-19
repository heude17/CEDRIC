import os

from flask import Flask, redirect, render_template, url_for

from config import Config
from models import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    db.init_app(app)

    from routes.audit import bp as audit_bp
    from routes.clients import bp as clients_bp
    from routes.pdf import bp as pdf_bp
    from routes.projets import bp as projets_bp
    from routes.validation import bp as validation_bp

    app.register_blueprint(clients_bp)
    app.register_blueprint(projets_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(pdf_bp)
    app.register_blueprint(validation_bp)

    @app.route("/")
    def index():
        return redirect(url_for("clients.liste"))

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("404.html"), 404

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
