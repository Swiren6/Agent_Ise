Structure :

backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée FastAPI
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration centralisée
│   │   └── database.py      # Connexion DB
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Modèles Pydantic
│   ├── services/
│   │   ├── __init__.py
│   │   └── sql_assistant.py # Logique métier
│   └── api/
│       ├── __init__.py
│       └── routes.py        # Endpoints API
├── requirements.txt
├── .env
└── README.md


📋 Endpoints disponibles

POST /api/v1/query - Poser une question SQL
GET /api/v1/health - Vérifier l'état du service
GET / - Page d'accueil

# =============================================================================
# Commandes pour lancer l'application
# =============================================================================

"""
# Installation
pip install -r requirements.txt

# Lancement en développement
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Lancement en production
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test de l'API
curl -X POST "http://localhost:8000/api/v1/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "Combien d'élèves sont inscrits?"}'

# Health check
curl http://localhost:8000/api/v1/health
"""