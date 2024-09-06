from datetime import datetime
from app import db
from models import Utilisateur

class MotifRdv(db.Model):
    motifId = db.Column(db.Integer, primary_key=True)
    utilisateurId = db.Column(db.Integer, db.ForeignKey('utilisateur.utilisateurId'), nullable=False)
    motifDescription = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def to_dict(self):
        return {
            "motifId": self.motifId,
            "utilisateurId": self.utilisateurId,
            "motifDescription": self.motifDescription,
            "date": self.date.isoformat()
        }