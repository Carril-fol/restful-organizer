from flask_jwt_extended import get_jwt_identity
from functools import wraps

from folders.services.folder_service import FolderService
from folders.exceptions.folder_exception import FolderNotFound
from auth.services.user_service import UserService

user_service = UserService()
folder_service = FolderService()

def is_folder_from_the_user(fn):
    """
    Decorator that checks if the user is the creator of the folder.

    Attributes:
    -----------
    fn : function
        The function to be decorated.

    Returns:
    --------
    function
        The decorated function that first checks if the user id in the token 
        is equal to the user id in the folder.
    """ 
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            user_id = get_jwt_identity()["id"]
            folder_id_from_url = kwargs.get("folder_id")
            folder_exists = folder_service.detail_folder(folder_id_from_url)
            folder_creator = folder_exists.get("folder")["user_id"]
            if folder_creator != user_id:
                return {"error": "Unauthorized access to this folder"}, 403
            return fn(*args, **kwargs)
        except FolderNotFound as error:
            return {"error": (str(error))}, 404
        except Exception as error:
            return {"error": (str(error))}, 400
    return wrapper

def is_user_authorized_to_see_folders(fn):
    """
    Decorator that checks if the user id in the token is equals to the user id in the url.

    Attributes:
    -----------
    fn : function
        The function to be decorated.

    Returns:
    --------
    function
        The decorated function that first checks if the user id in the token 
        is equal to the user id in the folder.
    """ 
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            user_id_in_the_token = get_jwt_identity()["id"]
            user_id_in_the_url = kwargs.get("user_id")
            if user_id_in_the_token != user_id_in_the_url:
                return {"error": "Unauthorized access to see the folders from this user."}, 403
            return fn(*args, **kwargs)
        except Exception as error:
            return {"error": (str(error))}, 400
    return wrapper