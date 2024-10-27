from bson import ObjectId

from database.db import Database
from models.task_model import TaskModel

class TaskRepository:
    def __init__(self):
        """
        Initialize the class with the following attributes

        self.__database (Database): In an instance of "Database" 
            to interact with the methods from this class.
        self.task_collection: Is an instance of a method from "Database" to 
            interact with tasks collection in the database.
        """
        self.__database = Database()
        self.task_collection = self.__database.tasks_collection()

    def get_task_by_id(self, task_id: str):
        """
        Allows returning a dictionary with the information of the task entered by id.

        Attributes:
        ----------
        task_id (str): A text string representing the ID of an task.

        Returns:
        -------
        A dictionary with the task information entered by id.
        """
        task_data_filter = {"_id": ObjectId(task_id)}
        task_found = self.task_collection.find_one(task_data_filter)
        return task_found

    def create_task(self, task_instance_model: TaskModel):
        """
        Formats the input model instance to a dictionary and inserts it into the corresponding collection of tasks.

        Attributes:
        ----------
        task_instance_model (TaskModel): An instance from "TaskModel".

        Returns:
        -------
        The id inserted in the data collection.
        """
        task_model_dump = task_instance_model.model_dump(by_alias=True)
        task_created = self.task_collection.insert_one(task_model_dump)
        return task_created.inserted_id
    
    def delete_task(self, task_id: str):
        """
        Allows to delete a task based on they ID.
        
        Attributes:
        ----------
        task_id (str): A text string representing the ID of an task.

        Returns:
        -------
        An instance of "DeleteResult" from PyMongo.
        """
        task_data_filter = {"_id": ObjectId(task_id)}
        task_delete = self.task_collection.delete_one(task_data_filter)
        return task_delete
    
    def update_task(self, task_id: str, new_data_task: dict):
        """
        Allows you to update an existing task.
        
        Attributes:
        ----------
        task_id (str): A text string representing the ID of an task.
        new_data_task (dict): A dictionary with the new data for the task.

        Returns:
        -------
        The ID upserted in the data collection.
        """
        task_data_filter = {"_id": ObjectId(task_id)}
        task_new_data = {
            "$set": new_data_task
        }
        task_updated = self.task_collection.update_one(task_data_filter, task_new_data)
        return task_updated.upserted_id

    async def get_tasks_by_folder_id(self, folder_id: str):
        """
        Allows you to make a query to the database to return the tasks that contain the folder_id.
        
        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Returns:
        -------
        returns dictionaries of the tasks that contain the folder_id.
        """
        task_data_filter = {"folder_id": ObjectId(folder_id)}
        tasks_founds = self.task_collection.find(task_data_filter)
        return tasks_founds
    
    async def delete_tasks_by_folder_id(self, folder_id: str):
        """
        Allows to delete tasks by they folder_id.
        
        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Returns:
        -------
        returns a instance "DeleteResult" from PyMongo 
        """
        task_data_filter = {"folder_id": ObjectId(folder_id)}
        tasks_deleted = self.task_collection.delete_many(task_data_filter)
        return tasks_deleted