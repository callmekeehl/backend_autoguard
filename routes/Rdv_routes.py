from flask import Blueprint, request, jsonify
from models import Declaration, Notification, Rdv, Police, Garage
from models.MotifRdv import MotifRdv
from models.Utilisateur import Utilisateur
from app import db

rdv_bp = Blueprint('rdv_bp', __name__)

from models.Rdv import Rdv


@rdv_bp.route('/rdvs', methods=['POST'])
def handle_rdvs():
    if request.method == 'POST':
        data = request.get_json()
        new_rdv = Rdv(
            utilisateurId=data['utilisateurId'],
            policeId=data['policeId'],
            date=data['date'],
            motif=data['motif']
        )
        db.session.add(new_rdv)
        db.session.commit()
        return jsonify({"message": "Rdv créé"}), 201


@rdv_bp.route('/rdvs', methods=['GET'])
def get_rdvs():
    rdvs = Rdv.query.all()
    return jsonify([r.to_dict() for r in rdvs])


@rdv_bp.route('/rdvs/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_rdv(id):
    rdv = Rdv.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(rdv.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        rdv.utilisateurId = data['utilisateurId']
        rdv.policeId = data['policeId']
        rdv.date = data['date']
        rdv.motif = data['motif']
        db.session.commit()
        return jsonify({"message": "Rdv mis à jour"})

    if request.method == 'DELETE':
        db.session.delete(rdv)
        db.session.commit()
        return jsonify({"message": "Rdv supprimé"})

@rdv_bp.route('/utilisateurs/<int:id>', methods=['GET'])
def get_utilisateur(id):
    utilisateur = Utilisateur.query.get_or_404(id)
    return jsonify({
        'nom': utilisateur.nom,
        'prenom': utilisateur.prenom,
        'utilisateurId': utilisateur.id
        })

@rdv_bp.route('/motifs', methods=['GET'])
def get_motifs():
    motifs = MotifRdv.query.all()
    return jsonify([m.to_dict() for m in motifs])

@rdv_bp.route('/rdvs/accept/<int:motifId>', methods=['PUT'])
def accepter_rdv(motifId):
    motif = MotifRdv.query.get_or_404(motifId)

    # Création du rendez-vous à partir du motif accepté
    nouveau_rdv = Rdv(
        utilisateurId=motif.utilisateurId,
        motif=motif.motifDescription,
        date=motif.date
    )
    db.session.add(nouveau_rdv)

    # Envoyer une notification à l'utilisateur
    utilisateur = Utilisateur.query.get(motif.utilisateurId)
    if utilisateur:
        nouvelle_notification = Notification(
            utilisateurId=utilisateur.id,
            message="Votre rendez-vous a été accepté."
        )
        db.session.add(nouvelle_notification)

    # Supprimer l'entrée dans MotifRdv
    db.session.delete(motif)
    db.session.commit()

    return jsonify({"message": "Rendez-vous accepté et notification envoyée."}), 200

@rdv_bp.route('/rdvs/reject/<int:motifId>', methods=['PUT'])
def rejeter_rdv(motifId):
    motif = MotifRdv.query.get_or_404(motifId)
    data = request.get_json()
    raison_rejet = data.get('raison')

    # Envoyer une notification avec la raison du rejet
    utilisateur = Utilisateur.query.get(motif.utilisateurId)
    if utilisateur:
        nouvelle_notification = Notification(
            utilisateurId=utilisateur.id,
            message=f"Votre rendez-vous a été rejeté : {raison_rejet}"
        )
        db.session.add(nouvelle_notification)

    # Supprimer l'entrée dans MotifRdv
    db.session.delete(motif)
    db.session.commit()

    return jsonify({"message": "Rendez-vous rejeté et notification envoyée."}), 200
