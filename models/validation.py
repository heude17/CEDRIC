from datetime import datetime

from models import db


class Validation(db.Model):
    __tablename__ = "validations"

    id = db.Column(db.Integer, primary_key=True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projets.id"), nullable=False)
    nom_signataire = db.Column(db.String(120), nullable=False)
    email_signataire = db.Column(db.String(120))
    commentaire = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    projet = db.relationship("Projet", back_populates="validations")

    def to_dict(self):
        return {
            "id": self.id,
            "projet_id": self.projet_id,
            "nom_signataire": self.nom_signataire,
            "email_signataire": self.email_signataire,
            "commentaire": self.commentaire,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Validation {self.nom_signataire} pour projet {self.projet_id}>"
