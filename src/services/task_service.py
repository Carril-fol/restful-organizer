import json
from bson import ObjectId

from entities.task_model import TaskModel
from repositories.task_repository import TaskRepository
from exceptions.task_exception import TaskNotExists

class TaskService:
    def __init__(self):
        """
        Initialize the class with the following attributes

        self.task_repository: Is an instance from "TaskRepository" to 
            interact with their methods.
        """
        self.task_repository = TaskRepository()

    def _check_if_task_exists_by_id(self, task_id: str):
        """
        Allows returning a dictionary with the information of the task entered by id..

        Attributes:
        ----------
        task_id (str): A text string representing the ID of an task.

        Returns:
        -------
        A dictionary with the task information entered by id if it exists, if not it returns a boolean value False
        """
        task_exists = self.task_repository.get_task_by_id(task_id)
        return task_exists if task_exists else False
    
    def _format_dict_in_model(self, folder_id: str, data_task: dict) -> TaskModel:
        """
        Formats the input data and creates an instance of the TaskModel.

        Attributes:
        ----------
        folder_id (str): A text string representing the ID of a folder.
        data_task (dict): A dictionary containing task information.

        Returns:
        -------
        TaskModel: An instance of the task model.
        """
        data_task["folder_id"] = ObjectId(folder_id)
        return TaskModel.model_validate(data_task)

    async def get_all_task_by_folder_id(self, folder_id: str):
        """
        Allows to see all tasks related for a folder_id.

        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Returns:
        -------
        A list of dictionaries with the task information.
        """
        tasks_from_database = await self.task_repository.get_tasks_by_folder_id(folder_id)
        return [
            json.loads(
                TaskModel.model_validate(task).model_dump_json(by_alias=True)
            ) for task in tasks_from_database
        ]

    async def detail_task(self, task_id: str):
        """
        Allows to see the information of the task by their id.

        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Exceptions:
        ----------
        TaskNotExists: An exception that is returned if the task does not exist.

        Returns:
        -------
        A dictionaries with the task information.
        """
        task_exists = self._check_if_task_exists_by_id(task_id)
        if not task_exists:
            raise TaskNotExists()
        task_model_dump_json = TaskModel.model_validate(task_exists).model_dump_json()
        return json.loads(task_model_dump_json)

    async def create_task(self, folder_id: str, data: dict):
        """
        Allows to create tasks.

        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.
        data (dict): A dictionary with the all information from the task.

        Returns:
        -------
        A dictionary with the information from the task created.
        """
        task_instance_model = self._format_dict_in_model(folder_id, data)
        return await self.task_repository.create_task(task_instance_model)
    
    async def delete_task(self, task_id: str):
        """
        Allows to delete tasks.

        Attributes:
        ----------
        task_id (str): A text string representing the ID of an task.

        Exceptions:
        ----------
        TaskNotExists: An exception that is returned if the task does not exist.

        Returns:
        -------
        An instance of "DeleteResult" from PyMongo.
        """
        if not self._check_if_task_exists_by_id(task_id):
            raise TaskNotExists()
        return await self.task_repository.delete_task(task_id)
    
    async def update_task(self, task_id: str, data: dict):
        """
        Allows to update tasks.

        Attributes:
        ----------
        task_id (str): A text string representing the ID of an task.
        data (dict): A dictionary with the information to update.

        Exceptions:
        ----------
        TaskNotExists: An exception that is returned if the task does not exist.

        Returns:
        -------
        A upserted ID from the task.
        """
        if not self._check_if_task_exists_by_id(task_id):
            raise TaskNotExists()
        return await self.task_repository.update_task(task_id, data)
    
    async def delete_tasks(self, folder_id: str):
        """
        Allows to delete all tasks by folder_id.

        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Returns:
        -------
        A instance from "DeleteResult".
        """
        return await self.task_repository.delete_tasks_by_folder_id(folder_id) 