# app.py
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from Email_send import mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://justkeehl:justkeehl2003@localhost/backend_shema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'justkeehl'  # Changez cela pour une clé sécurisée


# Importation des modèles
from models import Utilisateur, Notification, Declaration, Police, Garage, Admin

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login' 

# Configuration de la fonction de chargement de l'utilisateur
@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))

# Configuration de Flask-Mail dans votre fichier principal Flask
app.config['MAIL_SERVER'] = 'smtp.yourserver.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'justkeehl@gmail.com'
app.config['MAIL_PASSWORD'] = 'REBECCALIEBEN2003'
mail.init_app(app)



# Enregistrement des blueprints
from routes import register_blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)