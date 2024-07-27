import cherrypy as server
from flask import Flask
from flask_restful import Api

from utils.extensions import cache, jwt, api
from settings import SERVER_SOCKET_HOST, SERVER_SOCKET_PORT
from auth.controllers.user_controller import *
from auth.controllers.token_controller import RefreshTokenResource
from folders.controllers.folder_controller import *
from tasks.controllers.task_controller import *
from events.controllers.event_controller import *

# Flask
# https://flask.palletsprojects.com/en/3.0.x/
app = Flask(__name__)
app.config.from_pyfile("settings.py")

# Flask-JWT-Extended
jwt.init_app(app)

# Flask-Restful
api = Api(app)

# Flask-Caching
cache.init_app(app)

# Endpoints
# https://flask-restful.readthedocs.io/en/latest/quickstart.html#endpoints

api.add_resource(UserRegisterResource, "/users/api/v1/register")
api.add_resource(UserLoginResource, "/users/api/v1/login")
api.add_resource(UserLogoutResource, "/users/api/v1/logout")
api.add_resource(UserDetailsResource, "/users/api/v1/<user_id>")
api.add_resource(RefreshTokenResource, "/users/api/v1/refresh")

api.add_resource(CreateFolderResource, "/folders/api/v1/create")
api.add_resource(GetFoldersByUserIdResource, "/folders/api/v1/user/<user_id>")
api.add_resource(FolderResource, "/folders/api/v1/<folder_id>")

api.add_resource(CreateTaskResource, "/tasks/api/v1/<folder_id>")
api.add_resource(TaskResource, "/tasks/api/v1/<task_id>")

api.add_resource(CreateEventResource, "/events/api/v1/<folder_id>")
api.add_resource(EventResource, "/events/api/v1/<event_id>")

if __name__ == "__main__":
    server.tree.graft(app, "/")
    server.config.update(
        {
            "server.socket_host": SERVER_SOCKET_HOST,
            "server.socket_port": SERVER_SOCKET_PORT
        }
    )
    server.engine.start()
    server.engine.block()