from datetime import datetime

from models import db


class Photo(db.Model):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey("zones.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    legende = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    zone = db.relationship("Zone", back_populates="photos")

    def to_dict(self):
        return {
            "id": self.id,
            "zone_id": self.zone_id,
            "filename": self.filename,
            "legende": self.legende,
        }

    def __repr__(self):
        return f"<Photo {self.filename}>"
