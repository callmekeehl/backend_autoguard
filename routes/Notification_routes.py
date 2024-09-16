from flask import Blueprint, jsonify, request
from models import Notification
from app import db

notification_bp = Blueprint('notification_bp', __name__)

@notification_bp.route('/notifications/<int:utilisateurId>', methods=['GET'])
def get_notifications_by_user(utilisateurId):
    notifications = Notification.query.filter_by(utilisateurId=utilisateurId).all()
    return jsonify([n.to_dict() for n in notifications])

@notification_bp.route('/notifications/<int:notificationId>/mark-as-read', methods=['PUT'])
def mark_notification_as_read(notificationId):
    notification = Notification.query.get_or_404(notificationId)
    notification.lu = 1
    db.session.commit()
    return jsonify({"message": "Notification marquée comme lue"})
