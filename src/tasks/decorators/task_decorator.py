from flask_jwt_extended import get_jwt_identity
from functools import wraps

from tasks.services.task_service import TaskService
from tasks.exceptions.task_exception import TaskNotExists
from folders.services.folder_service import FolderService
from folders.exceptions.folder_exception import FolderNotFound

task_service = TaskService()
folder_service = FolderService()

def is_task_from_the_user(fn):
    """
    Decorator that checks if the user entered in 
        the task is the creator of the folder where the task was created.

    Atributes:
    ---------
    fn: The function to be decorated.

    Exceptions:
    ----------
    FolderNotFound: Raise a exception if the folder not exists.
    TaskNotExists: Raise a exception if the task not exists.

    Returns:
    -------
    function: The decorated function that first checks if the user id 
        in the token is equals to the user id in the folder.
    """ 
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            user_id = get_jwt_identity()["id"]
            task_id = kwargs.get("task_id")
            task_exists = task_service.detail_task(task_id)
            folder_id = task_exists["folder_id"]
            folder_exists = folder_service.detail_folder(folder_id)
            folder_creator = folder_exists.get("folder")["user_id"]
            if folder_creator != user_id:
                return {"error": "Unauthorized access to this task"}, 403
            return fn(*args, **kwargs)
        except FolderNotFound as error:
            return {"error": (str(error))}, 404
        except TaskNotExists as error:
            return {"error": (str(error))}, 404
        except Exception as error:
            return {"error": (str(error))}, 400
    return wrapper
