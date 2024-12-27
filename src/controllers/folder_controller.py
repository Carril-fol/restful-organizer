from flask import request, Blueprint, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.folder_service import FolderService
from exceptions.folder_exception import FolderNotFound
from decorators.folder_decorator import is_folder_from_the_user

folder_blueprint = Blueprint("folder", __name__, url_prefix="/folders/api/v1")

folder_service = FolderService()

@folder_blueprint.route("/create", methods=["POST"])
@jwt_required()
async def create_folder():
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
    token = get_jwt_identity()
    data = request.get_json()
    if not data:
        return make_response({"error", "Missing JSON in the request"}, 400)
    await folder_service.create_folder(data, token)
    return make_response({"status": "Created"}, 201)

@folder_blueprint.route("/", methods=["GET"])
@jwt_required()
async def get_folders_from_user():
    """
    Example:

    GET: /folders/api/v1/
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
    token = get_jwt_identity()
    folders = await folder_service.get_folders_from_user(token)
    return make_response({"folders": folders}, 200)

@folder_blueprint.route("/detail/<folder_id>", methods=["GET"])
@jwt_required()
@is_folder_from_the_user
async def detail_folder(folder_id: str):
    """
    Example:

    GET: /folders/api/v1/detail/<folder_id>
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
        return make_response({"data": response}, 200)
    except FolderNotFound as error:
        return make_response({"error": str(error)}, 404)
    except Exception as error:
        return make_response({"error": str(error)}, 400)

@folder_blueprint.route("/update/<folder_id>", methods=["PUT", "PATCH"])
@jwt_required()
@is_folder_from_the_user
async def update_folder(folder_id: str):
    """
    Example:

    PUT: /folders/api/v1/update/<folder_id>
    ```
    Application data:
    {
        "name_folder": "Name for the folder"
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
    try:
        token = get_jwt_identity()
        data = request.get_json()
        if not data:
            return make_response({"error": "Missing JSON in the request"}, 400)
        await folder_service.update_folder(token, folder_id, data)
        return make_response({"status": "Updated"}, 200)
    except Exception as error:
        return make_response({"error": error}, 400)

@folder_blueprint.route("/delete/<folder_id>", methods=["DELETE"])
@jwt_required()
@is_folder_from_the_user
async def delete_folder(folder_id: str):
    """
    Example:

    DELETE: /folders/api/v1/delete/<folder_id>
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
    await folder_service.delete_folder(folder_id)
    return make_response({"status": "Deleted"}, 200)
