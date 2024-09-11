# Imports
from flask import request, Blueprint
from flask_jwt_extended import jwt_required

from utils.extensions import cache
from services.task_service import TaskService
from decorators.user_decorator import is_token_blacklisted
from decorators.folder_decorator import is_folder_from_the_user
from decorators.task_decorator import is_task_from_the_user

# Blueprint
task_blueprint = Blueprint("task", __name__, url_prefix="/tasks/api/v1")

# Services
task_service = TaskService()

@jwt_required(locations=["headers"])
@is_token_blacklisted
@is_folder_from_the_user
@task_blueprint.route("/create", methods=["POST"])
def create_task(self, folder_id: str):
    """
    Example:

    POST: /tasks/api/v1/<folder_id>
    ```
    Application data:
    {
        "name": "Name of the task",
        "body":  "Body of the task",
        "status": "Status of the task"
    }
        
    Successful response (Code 201 - CREATED):
    {
        "status": "Created",
        "task": {
            "name": "Name of the task",
            "body":  "Body of the task",
            "status": "Status of the task",
            "folder_id": "Id from the folder"
        }
    }

    Response with errors (Code 400 - BAD REQUEST):
    {
        "error": "Status introduced not valid."
    }
    ```
    """
    data = request.get_json()
    if not data:
        return {"error": "Missing JSON in request"}, 400
    if not folder_id:
        return {"error": "Missing ID from the folder in the URL."}, 400
    task_created = task_service.create_task(folder_id, data)
    return {"status": "Created", "task": task_created}, 201
        

@jwt_required()
@is_token_blacklisted
@is_task_from_the_user
@cache.cached(timeout=300)
@task_blueprint.route("/detail/<task_id>", methods=["GET"])
def detail_task(task_id: str):
    """
    Example:

    GET: /tasks/api/v1/<task_id>
    ```
    Successful response (Code 200 - OK):
    {
        "task": {
            "name": "Name of the task",
            "body":  "Body of the task",
            "status": "Status of the task",
            "folder_id": "Id from the folder"
        }
    }

    Response with errors (Code 400 - BAD REQUEST):
    {
        "error": "Task not exists."
    }
    ```
    """
    task_detail = task_service.detail_task(task_id)
    return {"task": task_detail}, 200
    
        
@is_token_blacklisted
@is_task_from_the_user
@task_blueprint.route("/delete/<task_id>", methods=["DELETE"])
def delete_task(task_id: str):
    """
    Example:

    DELETE: /tasks/api/v1/<task_id>
    ```
    Successful response (Code 200 - OK):
    {
        "status": "Deleted"
    }

    Response with errors (Code 404 - NOT FOUND):
    {
        "error": "Task not exists."
    }
    ```
    """
    task_deleted = task_service.delete_task(task_id)
    return {"status": "Deleted"}, 200


@is_token_blacklisted
@is_task_from_the_user
@jwt_required()
@task_blueprint.route("/update/<task_id>", methods=["PUT", "PATCH"])
def update_task(task_id: str):
    """
        Example:

        PUT: /tasks/api/v1/<task_id>
        ```
        Application data:
        {
            "name": "New name of the task",
            "body":  "New body of the task",
            "status": "New status of the task"
            "folder_id": "New id from the folder"
        }

        Successful response (Code 200 - OK):
        {
            "status": "Updated"
        }

        Response with errors (Code 400 - BAD REQUEST):
        {
            "error": "Task not exists."
        }
        ```
    """
    data = request.get_json()
    if not data:
        return {"error": "Missing JSON in the request"}, 200
    task_update = task_service.update_task(task_id, data)
    return {"status": "Updated"}, 200