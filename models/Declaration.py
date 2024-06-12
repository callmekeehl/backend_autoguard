from app import db
from models import Utilisateur


class Declaration(db.Model):
    declarationId = db.Column(db.Integer, primary_key=True)
    utilisateurId = db.Column(db.Integer, db.ForeignKey('utilisateur.utilisateurId'), nullable=False)
    nomProprio = db.Column(db.String(100), nullable=False)
    prenomProprio = db.Column(db.String(100), nullable=False)
    telephoneProprio = db.Column(db.String(20), nullable=False)
    lieuLong = db.Column(db.String(100), nullable=False)
    lieuLat = db.Column(db.String(100), nullable=False)
    photoCarteGrise = db.Column(db.String(100), nullable=True)
    numChassis = db.Column(db.String(100), nullable=False)
    numPlaque = db.Column(db.String(100), nullable=False)
    marque = db.Column(db.String(100), nullable=False)
    modele = db.Column(db.String(100), nullable=False)
    dateHeure = db.Column(db.DateTime, nullable=False)
    statut = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "declarationId": self.declarationId,
            "utilisateurId": self.utilisateurId,
            "nomProprio": self.nomProprio,
            "prenomProprio": self.prenomProprio,
            "telephoneProprio": self.telephoneProprio,
            "lieuLong": self.lieuLong,
            "lieuLat": self.lieuLat,
            "photoCarteGrise": self.photoCarteGrise,
            "numChassis": self.numChassis,
            "numPlaque": self.numPlaque,
            "marque": self.marque,
            "modele": self.modele,
            "dateHeure": self.dateHeure,
            "statut": self.statut
        }