from flask import Flask

from asgi import start_server
from utils.extensions import cache, jwt

from controllers.user_controller import auth_blueprint
from controllers.folder_controller import folder_blueprint
from controllers.task_controller import task_blueprint

# Flask
# https://flask.palletsprojects.com/en/3.0.x/
app = Flask(__name__)
app.config.from_pyfile("settings.py")

# Flask-JWT-Extended
jwt.init_app(app)

# Flask-Caching
cache.init_app(app)

# Endpoints
app.register_blueprint(auth_blueprint)
app.register_blueprint(folder_blueprint)
app.register_blueprint(task_blueprint)

if __name__ == "__main__":
    #start_server(app)
    app.run("localhost", 8000, True)