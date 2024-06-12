from app import db
from models.Utilisateur import Utilisateur


class Police(Utilisateur):
    __tablename__ = 'police'
    __mapper_args__ = {
        'polymorphic_identity': 'police',
    }
    policeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    utilisateurId = db.Column(db.Integer, db.ForeignKey('utilisateur.utilisateurId'), nullable=False, unique=True)
    utilisateur = db.relationship("Utilisateur", backref="police", uselist=False)
    nomDepartement = db.Column(db.String(100), nullable=False)
    adresseDepartement = db.Column(db.String(200), nullable=False)