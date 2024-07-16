from bson import ObjectId
import json

from folders.repositories.folder_repository import FolderDao
from folders.models.folder_model import FolderModel
from folders.exceptions.folder_exception import FolderNotFound

class FolderService:
    def __init__(self):
        self.folder_dao = FolderDao()

    def __check_if_folder_exists_by_id(self, folder_id: str):
        folder_instance = self.folder_dao.get_folder_by_id(folder_id)
        return folder_instance if folder_instance else False

    def get_folder_by_id(self, folder_id: str):
        folder_exists = self.__check_if_folder_exists_by_id(folder_id)
        if not folder_exists:
            raise FolderNotFound()
        folder_model_dump_json = FolderModel.model_validate(folder_exists).model_dump_json()
        folder_format_json = json.loads(folder_model_dump_json)
        return folder_format_json
    
    def get_folders_by_user_id(self, user_id: str):
        folders = self.folder_dao.get_folders_by_user_id(user_id)
        list_of_folders = [json.loads(FolderModel.model_validate(folder).model_dump_json(by_alias=True)) for folder in folders]
        return list_of_folders

    def create_folder(self, data: dict):
        folder_instance_model = FolderModel(
            name_folder=data["name_folder"],
            user_id=ObjectId(data["user_id"])
        )
        folder_created = self.folder_dao.create_folder(folder_instance_model)
        folder_format_json = self.get_folder_by_id(folder_created)
        return folder_format_json
    
    def update_folder(self, folder_id: str, data: dict):
        folder_instance_model = FolderModel(
            name_folder=data["name_folder"]
        )
        folder_updated = self.folder_dao.update_folder(folder_id, folder_instance_model)
        folder_format_json = self.get_folder_by_id(folder_id)
        return folder_format_json
    
    def delete_folder(self, folder_id: str):
        folder_found = self.__check_if_folder_exists_by_id(folder_id)
        if not folder_found:
            raise FolderNotFound()
        folder_instance_delete = self.folder_dao.delete_folder(folder_id)
        return folder_instance_delete