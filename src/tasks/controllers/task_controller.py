from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from extensions import cache
from auth.decorators.user_decorator import token_not_in_blacklist
from folders.exceptions.folder_exception import *
from tasks.services.task_service import TaskService
from tasks.exceptions.task_exception import *

task_service = TaskService()


class CreateTaskResource(Resource):

    @jwt_required(locations=["headers"])
    @token_not_in_blacklist
    def post(self, folder_id: str):
        """
        Example:

        POST: /tasks/api/v1/<folder_id>
        ```
        Application data:
        {
            "name": "Name of the task",
            "body":  "Body of the task",
            "status": "Status of the task"
        }
        
        Successful response (Code 201 - CREATED):
        {
            "status": "Created",
            "task": {
                "name": "Name of the task",
                "body":  "Body of the task",
                "status": "Status of the task",
                "folder_id": "Id from the folder"
            }
        }

        Response with errors (Code 400 - BAD REQUEST):
        {
            "error": "Status introduced not valid."
        }
        ```
        """
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in request"}, 400
        if not folder_id:
            return {"error": "Missing ID from the folder in the URL."}, 400
        try:
            task_created = task_service.create_task(folder_id, data)
            return {"status": "Created", "task": task_created}, 201
        except FolderNotFound as error:
            return {"error": (str(error))}, 404
        except Exception as error:
            return {"error": (str(error))}, 400
        

class TaskResource(Resource):
    
    @cache.cached(timeout=300)
    @jwt_required(locations=["headers"])
    @token_not_in_blacklist
    def get(self, task_id: str):
        """
        Example:

        GET: /tasks/api/v1/<task_id>
        ```
        Successful response (Code 200 - OK):
        {
            "task": {
                "name": "Name of the task",
                "body":  "Body of the task",
                "status": "Status of the task",
                "folder_id": "Id from the folder"
            }
        }

        Response with errors (Code 400 - BAD REQUEST):
        {
            "error": "Task not exists."
        }
        ```
        """
        try:
            task_detail = task_service.detail_task(task_id)
            return {"task": task_detail}, 200
        except TaskNotExists as error:
            return {"error": (str(error))}, 404
        except Exception as error:
            return {"error": (str(error))}, 400
        
    @jwt_required(locations=["headers"])
    @token_not_in_blacklist
    def delete(self, task_id: str):
        """
        Example:

        DELETE: /tasks/api/v1/<task_id>
        ```
        Successful response (Code 200 - OK):
        {
            "status": "Deleted"
        }

        Response with errors (Code 404 - NOT FOUND):
        {
            "error": "Task not exists."
        }
        ```
        """
        try:
            task_deleted = task_service.delete_task(task_id)
            return {"status": "Deleted"}, 200
        except TaskNotExists as error:
            return {"error": (str(error))}, 404
        except Exception as error:
            return {"error": (str(error))}, 400

    @jwt_required(locations=["headers"])
    @token_not_in_blacklist
    def put(self, task_id: str):
        """
        Example:

        PUT: /tasks/api/v1/<task_id>
        ```
        Application data:
        {
            "name": "New name of the task",
            "body":  "New body of the task",
            "status": "New status of the task"
            "folder_id": "New id from the folder"
        }

        Successful response (Code 200 - OK):
        {
            "status": "Updated"
        }

        Response with errors (Code 400 - BAD REQUEST):
        {
            "error": "Task not exists."
        }
        ```
        """
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in the request"}, 200
        try:
            task_update = task_service.update_task(task_id, data)
            return {"status": "Updated"}, 200
        except TaskNotExists as error:
            return {"error": (str(error))}, 404
        except Exception as error:
            return {"error": (str(error))}, 400