from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Flask-JWT-Extended
# https://flask-jwt-extended.readthedocs.io/en/stable/
jwt = JWTManager()

# Flask-CORS
# https://flask-cors.readthedocs.io/en/latest/
cors = CORS()