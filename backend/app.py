# # from flask import Flask, jsonify, request
# # from flask_jwt_extended import JWTManager, create_access_token, jwt_required
# # from flask_mysqldb import MySQL
# # import os
# # from dotenv import load_dotenv
# # from datetime import timedelta
# # from flask_cors import CORS 
# # import json




# # load_dotenv()

# # app = Flask(__name__)


# # CORS(app, resources={
# #     r"/api/*": {
# #         "origins": ["http://localhost:5000", "http://192.168.56.1:5000", "http://localhost:xxxx"],  # ajoute les ports où tourne ton frontend web
# #         "methods": ["OPTIONS", "GET", "POST"],
# #         "allow_headers": ["Content-Type", "Authorization"]
# #     }
# # })


# # # Configuration MySQL
# # app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
# # app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
# # app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
# # app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')
# # app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# # # Configuration JWT
# # app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
# # app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
# # jwt = JWTManager(app)

# # mysql = MySQL(app)

# # # @app.route('/api/login', methods=['POST', 'OPTIONS'])
# # # def login():
# # #     if request.method == 'OPTIONS':
# # #         return _build_cors_preflight_response()  # Pour les requêtes pré-vol CORS
    
# # #     data = request.get_json()
# # #     if not data:
# # #         return jsonify({"error": "No JSON data received"}), 400
        
# # #     login_identifier = data.get('login_identifier')
# # #     password = data.get('password')

# # #     cur = mysql.connection.cursor()
    
# # #     try:
# # #         # Vérification par email ou idpersonne
# # #         cur.execute("""
# # #             SELECT idpersonne, email, roles, changepassword 
# # #             FROM user 
# # #             WHERE email = %s OR idpersonne = %s
# # #         """, (login_identifier, login_identifier))
        
# # #         user = cur.fetchone()
# # #         if user:
# # #             # Décoder roles si c'est une chaîne JSON
# # #             try:
# # #                 roles = json.loads(user['roles'])
# # #             except Exception:
# # #                 roles = []  # ou gérer le fallback

# # #             access_token = create_access_token(identity={
# # #                 'idpersonne': user['idpersonne'],
# # #                 'roles': roles,
# # #                 'changepassword': user['changepassword']
# # #             })

# # #             return jsonify({
# # #                 'token': access_token,
# # #                 'idpersonne': user['idpersonne'],
# # #                 'roles': roles,
# # #                 'changepassword': user['changepassword']
# # #             }), 200
# # #         else:
# # #             return jsonify({"message": "Identifiants invalides"}), 401
            
# # #     except Exception as e:
# # #         return jsonify({"error": str(e)}), 500
# # #     finally:
# # #         cur.close()


# # @app.route('/api/login', methods=['POST', 'OPTIONS'])
# # def login():
# #     if request.method == 'OPTIONS':
# #         return _build_cors_preflight_response()

# #     data = request.get_json()
# #     if not data:
# #         return jsonify({"error": "No JSON data received"}), 400

# #     login_identifier = data.get('login_identifier')
# #     password = data.get('password')

# #     cur = mysql.connection.cursor()
# #     try:
# #         cur.execute("""
# #             SELECT idpersonne, email, roles, changepassword 
# #             FROM user 
# #             WHERE email = %s OR idpersonne = %s
# #         """, (login_identifier, login_identifier))

# #         user = cur.fetchone()
# #         print(f"user récupéré : {user}")
# #         if user:
# #             try:
# #                 print(f"roles avant json.loads : {user['roles']}")
# #                 roles = json.loads(user['roles'])
# #                 print(f"roles après json.loads : {roles}")
# #             except Exception as e:
# #                 print(f"Erreur json.loads roles: {e}")
# #                 roles = []
# #         if user:
# #             # Décoder la chaîne JSON stockée en base
# #             try:
# #                 roles = json.loads(user['roles'])
# #             except Exception:
# #                 roles = []

# #             # TODO : vérifier le mot de passe ici !

# #             access_token = create_access_token(identity={
# #                 'idpersonne': user['idpersonne'],
# #                 'roles': roles,
# #                 'changepassword': user['changepassword']
# #             })

# #             return jsonify({
# #                 'token': access_token,
# #                 'idpersonne': user['idpersonne'],
# #                 'roles': roles,  # ici on renvoie la liste Python native
# #                 'changepassword': user['changepassword']
# #             }), 200
# #         else:
# #             return jsonify({"message": "Identifiants invalides"}), 401

# #     except Exception as e:
# #         return jsonify({"error": str(e)}), 500
# #     finally:
# #         cur.close()

# # def _build_cors_preflight_response():
# #     response = jsonify({"status": "preflight"})
# #     response.headers.add("Access-Control-Allow-Origin", "*")
# #     response.headers.add("Access-Control-Allow-Headers", "*")
# #     response.headers.add("Access-Control-Allow-Methods", "*")
# #     return response

# # if __name__ == '__main__':
# #     # app.run(host='0.0.0.0', port=5000, debug=True)
# #     app.run(host='0.0.0.0', port=5000)


# from flask import Flask, jsonify, request
# from flask_jwt_extended import JWTManager, create_access_token
# from flask_mysqldb import MySQL
# import os
# from dotenv import load_dotenv
# from datetime import timedelta
# from flask_cors import CORS
# import json

# load_dotenv()

# app = Flask(__name__)

# CORS(app, resources={
#     r"/api/*": {
#         "origins": [
#             "http://localhost:5000",
#             "http://192.168.56.1:5000",
#             "http://localhost:xxxx"  # remplace par les ports frontend
#         ],
#         "methods": ["OPTIONS", "GET", "POST"],
#         "allow_headers": ["Content-Type", "Authorization"]
#     }
# })

# # Config MySQL
# app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
# app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
# app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
# app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# # Config JWT
# app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# jwt = JWTManager(app)
# mysql = MySQL(app)

# @app.route('/api/login', methods=['POST', 'OPTIONS'])
# def login():
#     if request.method == 'OPTIONS':
#         return _build_cors_preflight_response()

#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No JSON data received"}), 400

#     login_identifier = data.get('login_identifier')
#     password = data.get('password')

#     cur = mysql.connection.cursor()
#     try:
#         cur.execute("""
#             SELECT idpersonne, email, roles, changepassword 
#             FROM user 
#             WHERE email = %s OR idpersonne = %s
#         """, (login_identifier, login_identifier))

#         user = cur.fetchone()
#         if user:
#             print("RAW roles from DB:", user['roles'], type(user['roles']))
#             # Forcer le décodage JSON ici
#             try:
#                 roles = json.loads(user['roles'])
#             except Exception as e:
#                 print("JSON decode error:", e)
#                 roles = []

#             print("DECODED roles:", roles, type(roles))

#             access_token = create_access_token(identity={
#                 'idpersonne': user['idpersonne'],
#                 'roles': roles,
#                 'changepassword': user['changepassword']
#             })

#             response = {
#                 'token': access_token,
#                 'idpersonne': user['idpersonne'],
#                 'roles': roles,  # Assure-toi que c’est bien une liste ici !
#                 'changepassword': user['changepassword']
#             }
#             print("Response JSON:", response)
#             return jsonify(response), 200
#         else:
#             return jsonify({"message": "Identifiants invalides"}), 401

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         cur.close()
# def _build_cors_preflight_response():
#     response = jsonify({"status": "preflight"})
#     response.headers.add("Access-Control-Allow-Origin", "*")
#     response.headers.add("Access-Control-Allow-Headers", "*")
#     response.headers.add("Access-Control-Allow-Methods", "*")
#     return response

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

    
    
    
    
from flask import Flask, jsonify, request
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

def parse_roles(roles_str):
    """
    Convertit la chaîne '["ROLE_PARENT"]' en liste ['ROLE_PARENT']
    Gère tous les cas possibles :
    - None → []
    - Chaîne JSON valide → liste Python
    - Chaîne mal formatée → [valeur originale]
    - Déjà une liste → retournée telle quelle
    """
    if roles_str is None:
        return []
    
    if isinstance(roles_str, list):
        return roles_str
    
    try:
        # Cas particulier: la chaîne est déjà un tableau JSON encodé
        if roles_str.startswith('["') and roles_str.endswith('"]'):
            return json.loads(roles_str)
        # Cas général pour tout JSON valide
        parsed = json.loads(roles_str)
        return parsed if isinstance(parsed, list) else [parsed]
    except (json.JSONDecodeError, TypeError):
        return [roles_str] if roles_str else []

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        response = jsonify({"status": "preflight"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    data = request.get_json()
    if not data:
        return jsonify({"error": "Aucune donnée reçue"}), 400

    login_identifier = data.get('login_identifier')
    password = data.get('password')

    cur = mysql.connection.cursor()
    try:
        cur.execute("""
            SELECT idpersonne, email, roles, changepassword 
            FROM user 
            WHERE email = %s OR idpersonne = %s
        """, (login_identifier, login_identifier))

        user = cur.fetchone()
        if not user:
            return jsonify({"message": "Identifiants invalides"}), 401

        # Conversion spéciale pour votre cas spécifique
        roles = parse_roles(user['roles'])
        print(f"Rôles parsés: {roles} (type: {type(roles)})")  # Debug

        # Création du token
        token_data = {
            'idpersonne': user['idpersonne'],
            'roles': roles,
            'changepassword': user['changepassword']
        }
        access_token = create_access_token(identity=token_data)

        # Réponse finale
        return jsonify({
            'token': access_token,
            'idpersonne': user['idpersonne'],
            'roles': roles,  # Doit être une liste
            'changepassword': user['changepassword']
        }), 200

    except Exception as e:
        print(f"Erreur: {str(e)}")
        return jsonify({"error": "Erreur serveur"}), 500
    finally:
        cur.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)