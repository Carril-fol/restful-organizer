from flask_jwt_extended import get_jwt
from flask import request, jsonify
from functools import wraps

from folders.services.folder_service import FolderService
from folders.exceptions.folder_exception import FolderNotFound

from auth.services.user_service import UserService
from auth.services.token_service import TokenService

user_service = UserService()
folder_service = FolderService()

def folder_is_from_the_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            jwt_data = get_jwt().get("sub")
            user_id_from_the_token = jwt_data["id"]
            folder_id_from_url = kwargs.get("folder_id")
            folder_exists = folder_service.detail_folder(folder_id_from_url)
            if folder_exists["user_id"] != user_id_from_the_token:
                return {"error": "Unauthorized access to this folder"}, 403
            return fn(*args, **kwargs) 
        except Exception as error:
            return {"error": str(error)}, 400
    return wrapper