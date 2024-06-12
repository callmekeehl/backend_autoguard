from flask import Blueprint

# Importation des blueprints de chaque fichier de routes
from routes.Utilisateur_routes import utilisateur_bp
from routes.Notification_routes import notification_bp
from routes.Declaration_routes import declaration_bp
from routes.Police_routes import police_bp
from routes.Garage_routes import garage_bp
from routes.Admin_routes import admin_bp
from routes.Rdv_routes import rdv_bp
from routes.Auth_routes import auth_bp


# Création d'un blueprint principal pour l'application
main = Blueprint('main', __name__)


# Enregistrement de tous les blueprints
def register_blueprints(app):
    app.register_blueprint(utilisateur_bp, url_prefix='/api')
    app.register_blueprint(notification_bp, url_prefix='/api')
    app.register_blueprint(declaration_bp, url_prefix='/api')
    app.register_blueprint(police_bp, url_prefix='/api')
    app.register_blueprint(garage_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
    app.register_blueprint(rdv_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
