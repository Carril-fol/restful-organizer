from bson import ObjectId
from database.db import Database
from folders.models.folder_model import FolderModel

class FolderDao(object):
    def __init__(self):
        self.__database = Database()
        self.folder_collection = self.__database.folder_collection()

    def create_folder(self, folder_instance_model: FolderModel):
        folder_data_dict = folder_instance_model.model_dump(by_alias=True)
        folder_created = self.folder_collection.insert_one(folder_data_dict)
        return folder_created.inserted_id
    
    def get_folder_by_id(self, folder_id: str):
        folder_data_dict = {"_id": ObjectId(folder_id)}
        folder_founded = self.folder_collection.find_one(folder_data_dict)
        return folder_founded
    
    def get_folders_by_user_id(self, user_id: str):
        user_data_dict = {"user_id": ObjectId(user_id)}
        folders_from_the_user = self.folder_collection.find(user_data_dict)
        return folders_from_the_user
    
    def update_folder(self, folder_id: str, folder_instance_model: FolderModel):
        folder_dict_id = {"_id": ObjectId(folder_id)}
        folder_dict_data = {
            "$set": {
                "name_folder": folder_instance_model.name_folder
            }
        }
        folder_update_instance = self.folder_collection.update_one(folder_dict_id, folder_dict_data)
        return folder_update_instance
    
    def delete_folder(self, folder_id: str):
        folder_dict_id = {"_id": ObjectId(folder_id)}
        folder_delete_instance = self.folder_collection.delete_one(folder_dict_id)
        return folder_delete_instance