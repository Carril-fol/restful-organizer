from flask import request, Blueprint, make_response
from flask_jwt_extended import jwt_required

from services.task_service import TaskService
from decorators.folder_decorator import is_folder_from_the_user
from decorators.task_decorator import is_task_from_the_user

# Blueprint
task_blueprint = Blueprint("task", __name__, url_prefix="/tasks/api/v1")

# Services
task_service = TaskService()

@task_blueprint.route("/create/<folder_id>", methods=["POST"])
@jwt_required()
@is_folder_from_the_user
async def create_task(folder_id: str):
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
        "status": "Created"
    }

    Response with errors (Code 400 - BAD REQUEST):
    {
        "error": "Status introduced not valid."
    }
    ```
    """
    data = request.get_json()
    if not data:
        return make_response({"error": "Missing JSON in request"}, 400)
    if not folder_id:
        return make_response({"error": "Missing ID from the folder in the URL."}, 400)
    try:
        await task_service.create_task(folder_id, data)
        return make_response({"status": "Created"}, 201)
    except Exception as error:
        return make_response({"error": error}, 400)

@task_blueprint.route("/delete/<task_id>", methods=["DELETE"])
@jwt_required()
@is_task_from_the_user
async def delete_task(task_id: str):
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
    try:
        await task_service.delete_task(task_id)
        return make_response({"status": "Deleted"}, 200)
    except Exception as error:
        return make_response({"error": error}, 400)

@task_blueprint.route("/update/<task_id>", methods=["PUT", "PATCH"])
@jwt_required()
@is_task_from_the_user
async def update_task(task_id: str):
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
        return make_response({"error": "Missing JSON in the request"}, 200)
    await task_service.update_task(task_id, data)
    return make_response({"status": "Updated"}, 200)

@task_blueprint.route("/get/<folder_id>", methods=["GET"])
@jwt_required()
async def get_all_tasks_from_folder(folder_id: str):
    if not folder_id:
        return make_response({"error": "Missing Folder ID in the URL"}, 400)
    tasks = await task_service.get_all_task_by_folder_id(folder_id)
    return make_response({"tasks": tasks}, 200)