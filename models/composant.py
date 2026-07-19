from datetime import datetime

from models import db

TYPES_COMPOSANT = [
    "interrupteur",
    "prise",
    "eclairage",
    "volet_roulant",
    "chauffage",
    "autre",
]

TYPES_INTERRUPTEUR = [
    "simple_allumage",
    "va_et_vient",
    "poussoir",
    "variateur",
    "sans_fil",
    "non_applicable",
]


class Composant(db.Model):
    __tablename__ = "composants"

    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey("zones.id"), nullable=False)
    type_composant = db.Column(db.String(30), default="autre")
    type_interrupteur = db.Column(db.String(30), default="non_applicable")
    presence_neutre = db.Column(db.Boolean, default=False)
    besoin_motorisation = db.Column(db.Boolean, default=False)
    quantite = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    zone = db.relationship("Zone", back_populates="composants")

    def to_dict(self):
        return {
            "id": self.id,
            "zone_id": self.zone_id,
            "type_composant": self.type_composant,
            "type_interrupteur": self.type_interrupteur,
            "presence_neutre": self.presence_neutre,
            "besoin_motorisation": self.besoin_motorisation,
            "quantite": self.quantite,
            "notes": self.notes,
        }

    def __repr__(self):
        return f"<Composant {self.type_composant} x{self.quantite}>"
