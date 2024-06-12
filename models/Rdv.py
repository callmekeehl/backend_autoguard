from app import db
from models import Utilisateur
from models import Police


class Rdv(db.Model):
    rdvId = db.Column(db.Integer, primary_key=True)
    utilisateurId = db.Column(db.Integer, db.ForeignKey('utilisateur.utilisateurId'), nullable=False)
    policeId = db.Column(db.Integer, db.ForeignKey('police.policeId'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    motif = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            "rdvId": self.rdvId,
            "utilisateurId": self.utilisateurId,
            "policeId": self.policeId,
            "date": self.date,
            "motif": self.motif,
        }