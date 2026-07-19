from datetime import datetime

from models import db

STATUTS_PROJET = ["brouillon", "en_cours", "termine"]


class Projet(db.Model):
    __tablename__ = "projets"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), nullable=False)
    nom = db.Column(db.String(120), nullable=False)
    adresse_chantier = db.Column(db.String(255))
    statut = db.Column(db.String(20), default="brouillon")
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship("Client", back_populates="projets")
    zones = db.relationship(
        "Zone", back_populates="projet", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client_id,
            "nom": self.nom,
            "adresse_chantier": self.adresse_chantier,
            "statut": self.statut,
            "notes": self.notes,
            "zones": [zone.to_dict() for zone in self.zones],
        }

    def __repr__(self):
        return f"<Projet {self.nom}>"
