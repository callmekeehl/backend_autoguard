from flask import Blueprint, request, jsonify
from models import Declaration, Notification, Rdv, Police, Garage
from models.Utilisateur import Utilisateur
from app import db

notification_bp = Blueprint('notification_bp', __name__)

from models.Notification import Notification

@notification_bp.route('/notifications', methods=['GET', 'POST'])
def handle_notifications():
    if request.method == 'POST':
        data = request.get_json()
        new_notification = Notification(
            utilisateurId=data['utilisateurId'],
            message=data['message'],
            dateEnvoi=data['dateEnvoi'],
            lu=data['lu']
        )
        db.session.add(new_notification)
        db.session.commit()
        return jsonify({"message": "Notification créée"}), 201

    if request.method == 'GET':
        notifications = Notification.query.all()
        return jsonify([n.to_dict() for n in notifications])

@notification_bp.route('/notifications/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_notification(id):
    notification = Notification.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify(notification.to_dict())

    if request.method == 'PUT':
        data = request.get_json()
        notification.utilisateurId = data['utilisateurId']
        notification.message = data['message']
        notification.dateEnvoi = data['dateEnvoi']
        notification.lu = data['lu']
        db.session.commit()
        return jsonify({"message": "Notification mise à jour"})

    if request.method == 'DELETE':
        db.session.delete(notification)
        db.session.commit()
        return jsonify({"message": "Notification supprimée"})