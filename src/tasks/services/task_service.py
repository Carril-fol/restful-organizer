from bson import ObjectId
import json

from folders.services.folder_service import FolderService
from folders.exceptions.folder_exception import FolderNotFound

from tasks.models.task_model import TaskModel
from tasks.repositories.task_repository import TaskRepository
from tasks.exceptions.task_exception import TaskNotExists

class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()
        self.folder_service = FolderService()

    def __check_if_task_exists_by_id(self, task_id: str):
        task_exists = self.task_repository.get_task_by_id(task_id)
        return task_exists if task_exists else False
    
    def __check_if_folder_exists_by_id(self, folder_id: str):
        return self.folder_service.check_if_folder_exists_by_id(folder_id)

    def detail_task(self, task_id: str):
        task_exists = self.__check_if_task_exists_by_id(task_id)
        if not task_exists:
            raise TaskNotExists()
        task_model_dump_json = TaskModel.model_validate(task_exists).model_dump_json()
        task_format_json = json.loads(task_model_dump_json)
        return task_format_json

    def create_task(self, folder_id: str, data: dict):
        folder_exists = self.__check_if_folder_exists_by_id(folder_id)
        if not folder_exists:
            raise FolderNotFound()
        task_instance_model = TaskModel(
            name=data["name"],
            body=data["body"],
            status=data["status"],
            folder_id=ObjectId(folder_id)
        )
        task_created = self.task_repository.create_task(task_instance_model)
        task_format_json = self.detail_task(task_created)
        return task_format_json
    
    def delete_task(self, task_id: str):
        task_exists = self.__check_if_task_exists_by_id(task_id)
        if not task_exists:
            raise TaskNotExists()
        task_delete = self.task_repository.delete_task(task_id)
        return task_delete
    
    def update_task(self, task_id: str, data: dict):
        task_exists = self.__check_if_task_exists_by_id(task_id)
        if not task_exists:
            raise TaskNotExists()
        task_update = self.task_repository.update_task(task_id, data)
        return task_update