from asgi import start_server
from utils.extensions import app

from controllers.user_controller import auth_blueprint
from controllers.folder_controller import folder_blueprint
from controllers.task_controller import task_blueprint

# Config
app.config.from_pyfile("../settings.py")

# Endpoints
app.register_blueprint(auth_blueprint)
app.register_blueprint(folder_blueprint)
app.register_blueprint(task_blueprint)  

if __name__ == "__main__":
    start_server(app)