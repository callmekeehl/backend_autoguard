from app import db
from models.Utilisateur import Utilisateur

class Garage(Utilisateur):
    __tablename__ = 'garage'
    __mapper_args__ = {
        'polymorphic_identity': 'garage',
    }
    garageId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utilisateurId = db.Column(db.Integer, db.ForeignKey('utilisateur.utilisateurId'), nullable=False, unique=True)
    utilisateur = db.relationship("Utilisateur", backref="garage", uselist=False)
    nomGarage = db.Column(db.String(100), nullable=False)
    adresseGarage = db.Column(db.String(200), nullable=False)