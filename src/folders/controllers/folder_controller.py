from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from extensions import cache
from auth.decorators.user_decorator import is_token_blacklisted
from folders.decorators.folder_decorator import is_folder_from_the_user, is_user_authorized_to_see_folders
from folders.services.folder_service import FolderService

folder_service = FolderService()

class CreateFolderResource(Resource):
    method_decorators = [jwt_required(locations=["headers"])]

    @is_token_blacklisted
    def post(self):
        """
        Example:

        POST: /folders/api/v1/create
        ```
        Application data:
        {
            "name_folder": "Name for the folder",
            "user_id": "Id from the user"
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
        data = request.get_json()
        if not data:
            return {"error", "Missing JSON in the request"}, 400
        folder_created = folder_service.create_folder(data)
        return {"status": "Created", "folder": folder_created}, 201


class GetFoldersByUserIdResource(Resource):
    method_decorators = [jwt_required(locations=["headers"])]
    
    @is_token_blacklisted
    @is_user_authorized_to_see_folders
    @cache.cached(timeout=300)
    def get(self, user_id: str):
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
        folders = folder_service.get_folders_by_user_id(user_id)
        return {"folders": folders}, 200


class FolderResource(Resource):
    method_decorators = [jwt_required(locations=["headers"])]

    @is_token_blacklisted
    @is_folder_from_the_user
    @cache.cached(timeout=300)
    def get(self, folder_id: str):
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
        data_from_folder = folder_service.detail_folder(folder_id)
        return {"data": data_from_folder}, 200

    @is_token_blacklisted
    @is_folder_from_the_user
    def put(self, folder_id: str):
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
        folder_instance_update = folder_service.update_folder(folder_id, data)
        return {"status": "Updated", "folder": folder_instance_update}, 200
    
    @is_token_blacklisted
    @is_folder_from_the_user
    def delete(self, folder_id: str):
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
        folder_delete = folder_service.delete_folder(folder_id)
        return {"status": "Deleted"}, 200