# Imports
from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils.extensions import cache
from services.folder_service import FolderService
from exceptions.folder_exception import FolderNotFound
from decorators.user_decorator import is_token_blacklisted
from decorators.folder_decorator import is_folder_from_the_user

# Blueprint
folder_blueprint = Blueprint("folder", __name__, url_prefix="/folders/api/v1")

# Service
folder_service = FolderService()

@folder_blueprint.route("/create", methods=["POST"])
@jwt_required(optional=False)
@is_token_blacklisted
def create_folder():
    """
    Example:

    POST: /folders/api/v1/create
    ```
    Application data:
    {
        "name_folder": "Name for the folder"
    }

    Successful response (Code 201 - CREATED):
    {
        "status": "Created",
        "folder": {
            "id": "Id from the folder",
            "name_folder": "Name for the folder",
            "user_id": "Id from the user"
        }
    }

    Response with error (Code 400 - BAD REQUEST):
    {
        "error": "Folder name cannot be blank."
    }
    ```
    """
    user_data_in_token = get_jwt_identity()
    data = request.get_json()
    if not data:
        return {"error", "Missing JSON in the request"}, 400
    response = folder_service.create_folder(data, user_data_in_token)
    return {"status": "Created"}, 201

@jwt_required()
@is_token_blacklisted
@cache.cached(timeout=60)
@folder_blueprint.route("/", methods=["GET"])
async def get_folders_from_user():
    """
    Example:

    GET: /folders/api/v1/<user_id>
    ```
    Successful response (Code 200 - OK):
    {
        "folders": [
            {
                "id": "Id from the folder",
                "name_folder": "Name for the folder",
                "user_id": "Id from the user"
            },
            ...
        ]
    }
    ```
    """
    user_data_from_token = get_jwt_identity()
    response = await folder_service.get_folders_from_user(user_data_from_token)
    return {"folders": response}, 200

@jwt_required()
@is_token_blacklisted
@is_folder_from_the_user
@folder_blueprint.route("/detail/<folder_id>", methods=["GET"])
async def detail_folder(folder_id: str):
    """
    Example:

    GET: /folders/api/v1/<folder_id>
    ```
    Successful response (Code 200 - OK):
    {
        "data": {
            "folder": {
                "id": "Id from the folder",
                "name_folder": "Name for the folder",
                "user_id": "Id from the user"
            },
            "tasks": [
                {
                    "name": "Name of the task",
                    "body":  "Body of the task",
                    "status": "Status of the task",
                    "folder_id": "Id from the folder"
                },
                ...
            ],
            "events": [
                {
                    "name_event": "Name for the event",
                    "folder_id": "Id from the folder",
                    "localization": "Localization from the event",
                    "start_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00",
                    "end_date": "Date in format: YYYY MM DD or YYYY-MM-DDTHH:MM:SS.MS+00:00"
                },
                ...
            ]
        }
    }

    Response with error (Code 404 - NOT FOUND):
    {
        "error": "Folder not found."
    }
    ```
    """
    try:
        response = await folder_service.detail_folder(folder_id)
        return {"data": response}, 200
    except FolderNotFound as error:
        return {"error": str(error)}, 404
    except Exception as error:
        return {"error": str(error)}, 400

@jwt_required()
@is_token_blacklisted
@is_folder_from_the_user
@folder_blueprint.route("/update/<folder_id>", methods=["POST"])
def update_folder(folder_id: str):
    """
    Example:

    PUT: /folders/api/v1/<folder_id>
    ```
    Application data:
    {
        "name_folder": "Name for the folder",
        "user_id": "Id from the user"
    }

    Successful response (Code 200 - OK):
    {
        "status": "Updated",
        "folder": {
            "id": "Id from the folder",
            "name_folder": "Name for the folder",
            "user_id": "Id from the user"
        }
    }

    Response with error (Code 400 - BAD REQUEST):
    {
        "error": "Folder name cannot be blank."
    }
    ```
    """
    data = request.get_json()
    if not data:
        return {"error": "Missing JSON in the request"}
    response = folder_service.update_folder(folder_id, data)
    return {"status": "Updated"}, 200

@jwt_required()
@is_token_blacklisted
@is_folder_from_the_user
@folder_blueprint.route("/delete/<folder_id>", methods=["DELETE"])
def delete_folder(folder_id: str):
    """
    Example:

    DELETE: /folders/api/v1/<folder_id>
    ```
    Successful response (Code 200 - OK):
    {
        "status": "Deleted"
    }

    Response with error (Code 400 - BAD REQUEST):
    {
        "error": "Folder not exists."
    }
    ```
    """
    response = folder_service.delete_folder(folder_id)
    return {"status": "Deleted"}, 200
