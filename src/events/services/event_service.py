import json
from bson import ObjectId

from folders.exceptions.folder_exception import *
from folders.services.folder_service import FolderService
from events.repositories.event_repository import EventRepository
from events.exceptions.event_exception import *
from events.models.event_model import EventModel


class EventService:
    def __init__(self):
        """
        Initialize the class with the following attributes

        
        self.event_repository (EventRepository): In an instance of "EventRepository" 
            to interact with the methods from this class.
        self.folder_service: (FolderService) Is an instance of "FolderService"
            to interact with the methods from this class to use.
        """
        self.event_repository = EventRepository()
        self.folder_service = FolderService()

    def __check_if_event_exists(self, event_id: str):
        """
        Allows to check if an event exists or not.

        Attributes:
        ----------
        event_id (str): A text string representing the ID of an event.

        Returns:
        -------
        If an event exists with event_id entered, return a dictionary with the event information, and if not, return False.
        """
        event_exists = self.event_repository.get_event_by_id(event_id)
        return event_exists if event_exists else False
    
    def __check_if_folder_exists(self, folder_id: str):
        """
        Allows to check if an folder exists or not

        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Returns:
        -------
        If an folder exists with folder_id entered, return a dictionary with the folder information, and if not, return False.
        """
        return self.folder_service.check_if_folder_exists_by_id(folder_id)

    def detail_event(self, event_id: str):
        """
        Allows to view an event in detail based on the ID entered.

        Attributes:
        ----------
        event_id (str): A text string representing the ID of an event.

        Exceptions:
        ----------
        EventNotFound: An exception that is returned if there is no event with the ID entered.

        Returns:
        -------
        event_format_json (json): A json that contains all the formatted information of the event.
        """
        event_exists = self.__check_if_event_exists(event_id)
        if not event_exists:
            raise EventNotFound()
        event_model_dump_json = EventModel.model_validate(event_exists).model_dump_json()
        event_format_json = json.loads(event_model_dump_json)
        return event_format_json

    def create_event(self, folder_id: str, data: dict):
        """
        Allows to create an event.

        Attributes:
        ----------
        data (dict): A dictionary with all the information about the event.

        Exceptions:
        ----------
        FolderNotFound: An exception that is returned if there is not a folder with the ID entered.

        Returns:
        -------
        event_created: The id inserted in the data collection.
        """
        folder_exists = self.__check_if_folder_exists(folder_id)
        if not folder_exists:
            raise FolderNotFound()
        event_instance_model = EventModel(
            name_event=data["name_event"],
            folder_id=ObjectId(folder_id),
            localization=data["localization"],
            start_date=data["start_date"],
            end_date=data["end_date"]
        )
        event_created = self.event_repository.create_event(event_instance_model)
        return event_created
    
    def update_event(self, event_id: str, data: dict):
        """
        Allows to update a event entered by id.

        Attributes:
        ----------
        event_id (str): A text string representing the ID of an event.
        data (dict): A dictionary with all the information about the event.

        Exceptions:
        ----------
        EventNotFound (Exception): An exception that is returned if there is no event with the ID entered.

        Returns:
        -------
        event_update: The updated event ID.
        """
        event_exists = self.__check_if_event_exists(event_id)
        if not event_exists:
            raise EventNotFound()
        data["folder_id"] = ObjectId(data["folder_id"])
        new_data_format = EventModel(**data).model_dump(exclude_unset=True)
        event_update = self.event_repository.update_event(event_id, new_data_format)
        return event_update

    def delete_event(self, event_id: str):
        """
        Allows to delete a event entered by id.

        Attributes:
        ----------
        event_id (str): A text string representing the ID of an event.

        Exceptions:
        ----------
        EventNotFound (Exception): An exception that is returned if there is no event with the ID entered.

        Returns:
        -------
        event_delete: A DeleteResult from pymongo.
        """
        event_exists = self.__check_if_event_exists(event_id)
        if not event_exists:
            raise EventNotFound()
        event_delete = self.event_repository.delete_event(event_id)
        return event_delete