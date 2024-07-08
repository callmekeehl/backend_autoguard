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

    def to_dict(self):
        utilisateur_data = super().to_dict()
        utilisateur_data.update({
            'policeId': self.policeId,
            'nomDepartement': self.nomDepartement,
            'adresseDepartement': self.adresseDepartement
        })
        return utilisateur_data