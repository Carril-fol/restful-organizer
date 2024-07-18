from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from extensions import cache
from auth.decorators.user_decorator import token_not_in_blacklist
from folders.decorators.folder_decorator import folder_is_from_the_user
from folders.services.folder_service import FolderService

folder_service = FolderService()

class CreateFolderResource(Resource):
    
    @jwt_required(locations=["headers"])
    @token_not_in_blacklist
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
        try:
            folder_created = folder_service.create_folder(data)
            return {"status": "Created", "folder": folder_created}, 201
        except Exception as error:
            return {"error": (str(error))}, 400
        

class GetFoldersByUserIdResource(Resource):

    @cache.cached(timeout=300)
    @jwt_required(locations=["headers"])
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
        try:
            folders = folder_service.get_folders_by_user_id(user_id)
            return {"folders": folders}, 200
        except Exception as error:
            return {"error": (str(error))}, 400


class FolderResource(Resource):
    method_decorators = [jwt_required(locations=["headers"])]

    @token_not_in_blacklist
    @folder_is_from_the_user
    def get(self, folder_id: str):
        try:
            folder = folder_service.detail_folder(folder_id)
            return {"folder": folder}, 200
        except Exception as error:
            return {"error": (str(error))}, 400

    @token_not_in_blacklist
    @folder_is_from_the_user
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
        try:
            folder_instance_update = folder_service.update_folder(folder_id, data)
            return {"status": "Updated", "folder": folder_instance_update}, 200
        except Exception as error:
            return {"error": (str(error))}, 400
    
    @token_not_in_blacklist
    @folder_is_from_the_user
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
        try:
            folder_delete = folder_service.delete_folder(folder_id)
            return {"status": "Deleted"}, 200
        except Exception as error:
            return {"error": (str(error))}, 400