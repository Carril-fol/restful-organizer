import json
from bson import ObjectId

from repositories.folder_repository import FolderRepository
from entities.folder_model import FolderModel
from exceptions.folder_exception import FolderNotFound
from services.task_service import TaskService

class FolderService:
    def __init__(self):
        """
        Initialize the class with the following attributes.

        self.folder_repository: An instance of "FolderRepository" to 
            interact with its methods.
        self.task_service: An instance of "TaskService" to handle operations 
            related to tasks.
        """
        self.folder_repository = FolderRepository()
        self.task_service = TaskService()

    def _get_user_id_requested(self, user_data: dict):
        """
        Extracts the user ID from the provided user data.

        Attributes:
        ----------
        user_data (dict): A dictionary containing user information.

        Returns:
        -------
        str: The user ID extracted from the dictionary.
        """
        return user_data.get("id")
    
    def _list_of_folders_in_format_json(self, folders):
        """
        Converts a list of folder instances into JSON format.

        Attributes:
        ----------
        folders (list): A list of folder instances.

        Returns:
        -------
        list: A list of JSON objects representing the folders.
        """
        return [
            json.loads(
                FolderModel.model_validate(folder).model_dump_json(by_alias=True)
            ) for folder in folders
        ]
    
    def _folder_in_format_json(self, folder_instance):
        """
        Converts a single folder instance into JSON format.

        Attributes:
        ----------
        folder_instance (FolderModel): An instance of the FolderModel.

        Returns:
        -------
        dict: A JSON representation of the folder instance.
        """
        return json.loads(
            FolderModel.model_validate(folder_instance).model_dump_json(by_alias=True)
        )
    
    def _format_data_in_model(self, data: dict, user):
        """
        Formats raw folder data into a FolderModel instance.

        Attributes:
        ----------
        data (dict): A dictionary with folder information.
        user (str): The user ID associated with the folder.

        Returns:
        -------
        FolderModel: An instance of the FolderModel with the provided data.
        """
        return FolderModel(
            name_folder=data.get("name_folder"),
            user_id=ObjectId(user)
        )
        
    def check_if_folder_exists_by_id(self, folder_id: str) -> FolderModel | bool:
        """
        Checks if a folder exists by its ID.

        Attributes:
        ----------
        folder_id (str): A text string representing the folder ID.

        Returns:
        -------
        FolderModel | bool: A FolderModel instance if the folder exists, 
        otherwise False.
        """
        folder_instance = self.folder_repository.get_folder_by_id(folder_id)
        return folder_instance if folder_instance else False
    
    async def create_folder(self, data: dict, token: dict):
        """
        Creates a new folder.

        Attributes:
        ----------
        data (dict): A dictionary with folder information.
        token (dict): A dictionary with user token information.

        Returns:
        -------
        dict: The created folder's information.
        """
        user = self._get_user_id_requested(token)
        folder_model = self._format_data_in_model(data, user)
        return self.folder_repository.create_folder(folder_model)
    
    async def detail_folder(self, folder_id: str):
        """
        Retrieves details of a folder by its ID, including its tasks.

        Attributes:
        ----------
        folder_id (str): A text string representing the folder ID.

        Exceptions:
        ----------
        FolderNotFound: Raised if the folder does not exist.

        Returns:
        -------
        dict: A dictionary containing the folder and its tasks.
        """
        folder_instance = self.check_if_folder_exists_by_id(folder_id)
        if not folder_instance:
            raise FolderNotFound()
        folder_json = self._folder_in_format_json(folder_instance)
        tasks_json = await self.task_service.get_all_task_by_folder_id(folder_id)
        return {"folder": folder_json, "tasks": tasks_json}
    
    async def get_folders_from_user(self, user_data_from_token: dict):
        """
        Retrieves all folders associated with a user.

        Attributes:
        ----------
        user_data_from_token (dict): A dictionary containing user token information.

        Returns:
        -------
        list: A list of folders in JSON format.
        """
        user_id = self._get_user_id_requested(user_data_from_token)
        folders = await self.folder_repository.get_folders_by_user_id(user_id)
        return self._list_of_folders_in_format_json(folders)
    
    async def update_folder(self, token: dict, folder_id: str, data: dict):
        """
        Updates an existing folder.

        Attributes:
        ----------
        token (dict): A dictionary with user token information.
        folder_id (str): A text string representing the folder ID.
        data (dict): A dictionary with updated folder information.

        Exceptions:
        ----------
        FolderNotFound: Raised if the folder does not exist.

        Returns:
        -------
        dict: The updated folder's information.
        """
        user = self._get_user_id_requested(token)
        if not self.check_if_folder_exists_by_id(folder_id):
            raise FolderNotFound()
        data["user_id"] = ObjectId(user)
        return await self.folder_repository.update_folder(folder_id, data)
    
    async def delete_folder(self, folder_id: str):
        """
        Deletes a folder by its ID, including all related tasks.

        Attributes:
        ----------
        folder_id (str): A text string representing the folder ID.

        Exceptions:
        ----------
        FolderNotFound: Raised if the folder does not exist.

        Returns:
        -------
        dict: Information about the deletion result.
        """
        if not self.check_if_folder_exists_by_id(folder_id):
            raise FolderNotFound()
        await self.task_service.delete_tasks(folder_id)
        return await self.folder_repository.delete_folder(folder_id)
