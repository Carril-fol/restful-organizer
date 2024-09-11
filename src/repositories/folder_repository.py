from bson import ObjectId

from database.db import Database
from models.folder_model import FolderModel

class FolderRepository(object):
    def __init__(self):
        self._database = Database()
        self.folder_collection = self._database.folder_collection()

    def create_folder(self, folder_instance_model: FolderModel):
        folder_model_dump = folder_instance_model.model_dump(by_alias=True)
        folder_created = self.folder_collection.insert_one(folder_model_dump)
        return folder_created.inserted_id
    
    def get_folder_by_id(self, folder_id: str):
        folder_data_dict = {"_id": ObjectId(folder_id)}
        folder_founded = self.folder_collection.find_one(folder_data_dict)
        return folder_founded
    
    async def get_folders_by_user_id(self, user_id: str):
        user_data_dict = {"user_id": ObjectId(user_id)}
        folders_from_the_user = self.folder_collection.find(user_data_dict)
        return folders_from_the_user
    
    async def update_folder(self, folder_id: str, data: dict):
        folder_dict_id = {"_id": ObjectId(folder_id)}
        folder_dict_data = {
            "$set": data
        }
        folder_update_instance = self.folder_collection.update_one(folder_dict_id, folder_dict_data)
        return folder_update_instance
    
    def delete_folder(self, folder_id: str):
        folder_dict_id = {"_id": ObjectId(folder_id)}
        folder_delete_instance = self.folder_collection.delete_one(folder_dict_id)
        return folder_delete_instance