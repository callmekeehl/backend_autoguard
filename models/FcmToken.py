from app import db

class FcmToken(db.Model):
    __tablename__ = 'fcm_tokens'

    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, nullable=False)
    fcm_token = db.Column(db.Text, nullable=False)
    date_ajout = db.Column(db.DateTime, default=db.func.now())
