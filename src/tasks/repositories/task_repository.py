from bson import ObjectId
from database.db import Database
from tasks.models.task_model import TaskModel

class TaskRepository:
    def __init__(self):
        self.__database = Database()
        self.task_collection = self.__database.tasks_collection()

    def get_task_by_id(self, task_id: str):
        task_data_filter = {"_id": ObjectId(task_id)}
        task_found = self.task_collection.find_one(task_data_filter)
        return task_found
    
    def create_task(self, task_instance_model: TaskModel):
        task_model_dump = task_instance_model.model_dump(by_alias=True)
        task_created = self.task_collection.insert_one(task_model_dump)
        return task_created.inserted_id
    
    def delete_task(self, task_id: str):
        task_data_filter = {"_id": ObjectId(task_id)}
        task_delete = self.task_collection.delete_one(task_data_filter)
        return task_delete
    
    def update_task(self, task_id: str, new_data_task: dict):
        task_data_filter = {"_id": ObjectId(task_id)}
        task_new_data = {
            "$set": {
                "name": new_data_task["name"],
                "body": new_data_task["body"],
                "status": new_data_task["status"],
                "folder_id": new_data_task["folder_id"]
            }
        }
        task_updated = self.task_collection.update_one(task_data_filter, task_new_data)
        return task_updated.upserted_id