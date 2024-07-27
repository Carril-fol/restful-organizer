import json
from bson import ObjectId

from events.repositories.event_repository import EventRepository
from events.exceptions.event_exception import EventNotFound
from events.models.event_model import EventModel, EventCreationModel


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

        Returns:
        -------
        event_created: The id inserted in the data collection.
        """
        event_instance_model = EventCreationModel(
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
        if data.get("folder_id"):
            data["folder_id"] = ObjectId(data["folder_id"])
        event_update = self.event_repository.update_event(event_id, data)
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
    
    def get_all_event_by_folder_id(self, folder_id: str):
        """
        Allows to the users see their own events created in a folder.

        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Returns:
        -------
        events_formated_json: A list with dictionaries from the events.
        """
        events_from_database = self.event_repository.get_events_by_folder_id(folder_id)
        events_formated_json = [
            json.loads(
                EventModel.model_validate(event).model_dump_json(by_alias=True)
            ) for event in events_from_database
        ]
        return events_formated_json
    
    def delete_events(self, folder_id: str):
        """
        Allows to delete all events by folder_id.

        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Returns:
        -------
        A instance from "DeleteResult".
        """
        events_deleted = self.event_repository.delete_events_by_folder_id(folder_id)
        return events_deleted 