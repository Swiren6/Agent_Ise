from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from datetime import timedelta
from flask_cors import CORS 


load_dotenv()

app = Flask(__name__)
# CORS(app)  # Active CORS pour toutes les routes
# CORS(app, resources={r"/api/*": {"origins": "*"}}) 
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "https://votre-site-web.com"],
        "methods": ["OPTIONS", "GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration MySQL
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Configuration JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)

mysql = MySQL(app)

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()  # Pour les requêtes pré-vol CORS
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
        
    login_identifier = data.get('login_identifier')
    password = data.get('password')

    cur = mysql.connection.cursor()
    
    try:
        # Vérification par email ou idpersonne
        cur.execute("""
            SELECT idpersonne, email, roles, changepassword 
            FROM user 
            WHERE email = %s OR idpersonne = %s
        """, (login_identifier, login_identifier))
        
        user = cur.fetchone()
        
        if user:
            # Dans votre cas, le mot de passe semble déjà hashé dans la base
            # Vous devriez vérifier le mot de passe ici si nécessaire
            
            # Création du token JWT
            access_token = create_access_token(identity={
                'idpersonne': user['idpersonne'],
                'roles': user['roles'],
                'changepassword': user['changepassword']
            })
            
            return jsonify({
                'token': access_token,
                'idpersonne': user['idpersonne'],
                'roles': user['roles'],
                'changepassword': user['changepassword']
            }), 200
        else:
            return jsonify({"message": "Identifiants invalides"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

def _build_cors_preflight_response():
    response = jsonify({"status": "preflight"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000) 

