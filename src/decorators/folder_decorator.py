from bson import ObjectId
from flask_jwt_extended import get_jwt_identity
from functools import wraps

from services.folder_service import FolderService
from services.user_service import UserService

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
    async def async_wrapper(*args, **kwargs):
        user_data_from_token = get_jwt_identity()
        user = user_service.get_user_id_requeted(user_data_from_token)

        folder_id = kwargs.get("folder_id")
        folder = folder_service.check_if_folder_exists_by_id(folder_id)
        folder_creator = folder.get("user_id")
        if folder_creator != ObjectId(user):
            return {"error": "Unauthorized access to this folder"}, 403
        return await fn(*args, **kwargs)
    return async_wrapper

