import json
from bson import ObjectId

from repositories.folder_repository import FolderRepository
from models.folder_model import FolderModel
from exceptions.folder_exception import FolderNotFound
from services.event_service import EventService
from services.task_service import TaskService

class FolderService:
    def __init__(self):
        self.folder_repository = FolderRepository()
        self.task_service = TaskService()
        self.event_service = EventService()

    def _get_user_id_requested(self, user_data: dict):
        user_id = user_data.get("id")
        return user_id
    
    def _list_of_folders_in_format_json(self, folders):
        list_of_folders = [
            json.loads(
                FolderModel.model_validate(folder).model_dump_json(by_alias=True)
            ) for folder in folders
        ]
        return list_of_folders
    
    def _folder_in_format_json(self, folder_instance):
        response_json = json.loads(
            FolderModel.model_validate(folder_instance).model_dump_json(by_alias=True)
        )
        return response_json
    
    def _format_data_in_model(self, data: dict, user):
        folder = FolderModel(
            name_folder=data.get("name_folder"),
            user_id=ObjectId(user)
        )
        return folder
        
    def check_if_folder_exists_by_id(self, folder_id: str) -> FolderModel | bool:
        folder_instance = self.folder_repository.get_folder_by_id(folder_id)
        return folder_instance if folder_instance else False
    
    def create_folder(self, data: dict, user_data_in_token: dict):
        user = self._get_user_id_requested(user_data_in_token)
        folder_model = self._format_data_in_model(data, user)
        folder_created = self.folder_repository.create_folder(folder_model)
        return folder_created
    
    async def detail_folder(self, folder_id: str):
        folder_instance = self.check_if_folder_exists_by_id(folder_id)
        if not folder_instance:
            raise FolderNotFound()
        folder_json = self._folder_in_format_json(folder_instance)
        tasks_json = await self.task_service.get_all_task_by_folder_id(folder_id)
        events_json = await self.event_service.get_all_event_by_folder_id(folder_id)
        data_folder = {
            "folder": folder_json,
            "tasks": tasks_json,
            "events": events_json
        }
        return data_folder
    
    async def get_folders_from_user(self, user_data_from_token: dict):
        user_id = self._get_user_id_requested(user_data_from_token)
        folders = await self.folder_repository.get_folders_by_user_id(user_id)
        list_of_folders = self._list_of_folders_in_format_json(folders)
        return list_of_folders
    
    async def update_folder(self, user_data_from_token: dict, folder_id: str, data: dict):
        user = self._get_user_id_requested(user_data_from_token)
        folder = self.check_if_folder_exists_by_id(folder_id)
        if not folder:
            raise FolderNotFound()
        folder_with_new_data = self._format_data_in_model(data, user)
        folder_updated = await self.folder_repository.update_folder(folder_id, folder_with_new_data)
        return folder_updated
    
    async def delete_folder(self, folder_id: str):
        folder = self.check_if_folder_exists_by_id(folder_id)
        if not folder:
            raise FolderNotFound()
        tasks_deleted = await self.event_service.delete_events(folder_id)
        events_deleted = await self.task_service.delete_tasks(folder_id)
        folder_deleted = await self.folder_repository.delete_folder(folder_id)
        return folder_deleted