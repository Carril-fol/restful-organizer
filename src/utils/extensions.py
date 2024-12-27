import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Flask
# https://flask.palletsprojects.com/en/stable/
app = Flask(__name__)

# Flask-JWT-Extended
# https://flask-jwt-extended.readthedocs.io/en/stable/
jwt = JWTManager(app)

# Flask-CORS
# https://flask-cors.readthedocs.io/en/latest/
cors = CORS(
    app, 
    supports_credentials=True, 
    origins=["https://organizer-app-ruck.onrender.com", "http://localhost:5173"],
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "application/json"]
)