from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Flask-Caching
# https://flask-caching.readthedocs.io/en/latest/
cache = Cache()

# Flask-JWT-Extended
# https://flask-jwt-extended.readthedocs.io/en/stable/
jwt = JWTManager()

# Flask-CORS
# https://flask-cors.readthedocs.io/en/latest/
cors = CORS()