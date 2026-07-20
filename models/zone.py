from datetime import datetime

from models import db

TYPES_PIECE = [
    "salon",
    "chambre",
    "cuisine",
    "salle_de_bain",
    "couloir",
    "bureau",
    "exterieur",
    "autre",
]


class Zone(db.Model):
    __tablename__ = "zones"

    id = db.Column(db.Integer, primary_key=True)
    projet_id = db.Column(db.Integer, db.ForeignKey("projets.id"), nullable=False)
    nom = db.Column(db.String(120), nullable=False)
    type_piece = db.Column(db.String(30), default="autre")
    surface_m2 = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    projet = db.relationship("Projet", back_populates="zones")
    composants = db.relationship(
        "Composant", back_populates="zone", cascade="all, delete-orphan"
    )
    photos = db.relationship(
        "Photo", back_populates="zone", cascade="all, delete-orphan",
        order_by="Photo.created_at",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "projet_id": self.projet_id,
            "nom": self.nom,
            "type_piece": self.type_piece,
            "surface_m2": self.surface_m2,
            "notes": self.notes,
            "composants": [composant.to_dict() for composant in self.composants],
            "photos": [photo.to_dict() for photo in self.photos],
        }

    def __repr__(self):
        return f"<Zone {self.nom}>"
