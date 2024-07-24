from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from events.services.event_service import EventService
from events.exceptions.event_exception import EventNotFound
from folders.services.folder_service import FolderService
from folders.exceptions.folder_exception import FolderNotFound

event_service = EventService()
folder_service = FolderService()

def is_event_from_the_user(fn):
    """
    Decorator that checks if the user id in the token is equal to the user id in the folder where the event is.

    Attributes:
    -----------
    fn : function
        The function to be decorated.

    Returns:
    --------
    function
        The decorated function that first checks if the user id in the token
        is equal to the user id in the folder where the event is.
    """ 
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt = verify_jwt_in_request(locations=["headers"])
            user_id = get_jwt_identity()["id"]
            event_id = kwargs.get("event_id")
            event_exists = event_service.detail_event(event_id)
            folder_id_from_the_event = event_exists["folder_id"]
            folder_instance = folder_service.detail_folder(folder_id_from_the_event)
            folder_creator = folder_instance.get("folder")["user_id"]
            if folder_creator != user_id:
                return {"error": "Unauthorized access to this event"}, 403
            return fn(*args, **kwargs)
        except Exception as error:
            return {"error": (str(error))}, 400
    return wrapper