from flask_jwt_extended import get_jwt
from flask import request
from functools import wraps

from folders.services.folder_service import FolderService
from auth.services.user_service import UserService
from auth.services.token_service import TokenService

user_service = UserService()
folder_service = FolderService()

def folder_is_from_the_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # TODO: seguir con el decorator
            get_dict_user_data = get_jwt().get("sub")
            get_user_id = get_dict_user_data["id"]
            
            folder_id = request.args.get("folder_id")
            folder_exists = folder_service.get_folder_by_id(folder_id)
            print(folder_exists)
        except Exception as error:
            return {"error": (str(error))}, 400
    return wrapper