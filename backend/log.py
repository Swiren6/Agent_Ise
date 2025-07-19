from flask import Flask, jsonify, request, Response
from flask_jwt_extended import JWTManager, create_access_token
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import timedelta
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5000", "http://192.168.56.1:5000"],
        "methods": ["OPTIONS", "GET", "POST"],
        "allow_headers": ["Content-Type", "Authorization"]
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

def parse_roles(raw_roles):
    """Parse les rôles avec logging complet"""
    app.logger.info(f"Raw roles received: {raw_roles} (type: {type(raw_roles)})")
    
    if raw_roles is None:
        app.logger.info("Roles is None, returning empty list")
        return []
    
    if isinstance(raw_roles, list):
        app.logger.info(f"Already a list: {raw_roles}")
        return raw_roles
    
    try:
        # Cas spécial pour le format ["ROLE_X"]
        if isinstance(raw_roles, str) and raw_roles.startswith('["') and raw_roles.endswith('"]'):
            parsed = json.loads(raw_roles)
            app.logger.info(f"Parsed special format: {parsed}")
            return parsed
        
        # Essai de parsing JSON standard
        if isinstance(raw_roles, str):
            parsed = json.loads(raw_roles)
            app.logger.info(f"JSON parsed successfully: {parsed}")
            return parsed if isinstance(parsed, list) else [parsed]
        
    except json.JSONDecodeError as e:
        app.logger.warning(f"JSON decode failed: {str(e)}. Returning as list")
        return [raw_roles] if raw_roles else []
    
    app.logger.info(f"Fallback to single item list: {raw_roles}")
    return [raw_roles] if raw_roles else []

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    app.logger.info("\n" + "="*50)
    app.logger.info("New login request received")
    
    if request.method == 'OPTIONS':
        app.logger.info("Handling OPTIONS preflight request")
        response = jsonify({"status": "preflight"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    try:
        data = request.get_json()
        app.logger.info(f"Request data: {data}")
        
        if not data:
            app.logger.error("No JSON data received")
            return jsonify({"error": "No data received"}), 400

        login_identifier = data.get('login_identifier')
        password = data.get('password')
        app.logger.info(f"Login attempt for: {login_identifier}")

        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT idpersonne, email, roles, changepassword 
            FROM user 
            WHERE email = %s OR idpersonne = %s
        """, (login_identifier, login_identifier))

        user = cur.fetchone()
        app.logger.info(f"DB user data: {user}")

        if not user:
            app.logger.warning(f"User not found: {login_identifier}")
            return jsonify({"message": "Invalid credentials"}), 401

        # Log avant parsing
        app.logger.info(f"Raw roles from DB: {user['roles']} (type: {type(user['roles'])})")
        
        roles = parse_roles(user['roles'])
        app.logger.info(f"Parsed roles: {roles} (type: {type(roles)})")

        # Création du token
        token_data = {
            'idpersonne': user['idpersonne'],
            'roles': roles,
            'changepassword': user['changepassword']
        }
        app.logger.info(f"Token data: {token_data}")

        access_token = create_access_token(identity=token_data)
        app.logger.info("Access token created successfully")

        # Construction réponse
        response_data = {
            'token': access_token,
            'idpersonne': user['idpersonne'],
            'roles': roles,
            'changepassword': user['changepassword']
        }
        app.logger.info(f"Final response data: {response_data}")

        # Sérialisation manuelle
        response_json = json.dumps(response_data, ensure_ascii=False)
        app.logger.info(f"Serialized JSON: {response_json}")

        return Response(
            response=response_json,
            status=200,
            mimetype='application/json'
        )

    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"error": "Server error"}), 500
    finally:
        if 'cur' in locals():
            cur.close()
        app.logger.info("Request processing complete\n" + "="*50)

if __name__ == '__main__':
    # Configuration des logs
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    app.logger.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True)