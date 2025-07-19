from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import datetime
from dotenv import load_dotenv
import os
from flask_cors import CORS
import bcrypt

# Chargement des variables d'environnement
load_dotenv()

app = Flask(__name__)

# Configuration CORS UNIQUE (supprimez toutes les autres configurations CORS)
cors = CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Ou spécifiez vos origines ["http://localhost:54676"]
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)  # Contient soit email soit numéro
    password = db.Column(db.String(255), nullable=False)
    idpersonne = db.Column(db.Integer)
    roles = db.Column(db.String(255))
    token = db.Column(db.String(255))
    changepassword = db.Column(db.Boolean)

def check_password(hashed_password, plain_password):
    # Conversion des hashs $2y$ en $2b$ pour Python
    if hashed_password.startswith('$2y$'):
        hashed_password = '$2b$' + hashed_password[4:]
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        phone_or_email = data.get('phone_or_email')  # Peut être numéro ou "superadmin"
        password = data.get('password')

        if not phone_or_email or not password:
            return jsonify({'error': 'Identifiant et mot de passe requis'}), 400

        # Recherche par email (qui peut être un numéro ou "superadmin")
        user = User.query.filter_by(email=phone_or_email).first()

        if not user:
            return jsonify({'error': 'Identifiants incorrects'}), 401

        if not check_password(user.password, password):
            return jsonify({'error': 'Identifiants incorrects'}), 401

        # Génération du token JWT avec les rôles
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'sub': user.id,
            'email': user.email,
            'roles': eval(user.roles) if user.roles else []  # Conversion de la string en liste
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({
            'token': token,
            'user_id': user.id,
            'phone_or_email': user.email,
            'roles': eval(user.roles) if user.roles else [],
            'changepassword': bool(user.changepassword)
        })

    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Erreur de serveur'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)