from bson import ObjectId
from database.db import Database
from events.models.event_model import EventModel, EventCreationModel

class EventRepository:
    def __init__(self):
        """
        Initialize the class with the following attributes

        self.__database (Database): In an instance of "Database" 
            to interact with the methods from this class.
        self.event_collection: Is an instance of a method from "Database"
            ti ubteract with events collection in the database.
        """
        self.__database = Database()
        self.event_collection = self.__database.events_collection()
    
    def create_event(self, event_creation_instance_model: EventCreationModel):
        """
        Formats the input model instance to a dictionary and inserts it into the corresponding collection of events.

        Attributes:
        ----------
        event_creation_instance_model (EventCreationModel): An instance from "EventCreationModel".

        Returns:
        -------
        The id inserted in the data collection
        """
        event_model_dump = event_creation_instance_model.model_dump(by_alias=True)
        event_inserted = self.event_collection.insert_one(event_model_dump)
        return event_inserted.inserted_id
    
    def get_event_by_id(self, event_id: str) -> dict:
        """
        Allows returning a dictionary with the information of the event entered by id.

        Attributes:
        ----------
        event_id (str): A text string representing the ID of an event.

        Returns:
        -------
        A dictionary with the event information entered by id.
        """
        event_filter_dict = {"_id": ObjectId(event_id)}
        event_found = self.event_collection.find_one(event_filter_dict)
        return event_found
    
    def update_event(self, event_id: str, data: dict):
        """
        Allows you to update an existing event in the event collection.
        
        Attributes:
        ----------
        event_id (str): A text string representing the ID of an event.
        data (dict): A dictionary with the new data for the event.

        Returns:
        -------
        The id inserted in the data collection.
        """
        event_filter_dict = {"_id": ObjectId(event_id)}
        event_new_data_dict = {
            "$set": data
        }
        event_updated = self.event_collection.update_one(event_filter_dict, event_new_data_dict)
        return event_updated.upserted_id
    
    def delete_event(self, event_id: str):
        """
        Allows to delete a event based on they ID.
        
        Attributes:
        ----------
        event_id (str): A text string representing the ID of an event.

        Returns:
        -------
        The id inserted in the data collection.
        """
        event_filter_dict = {"_id": ObjectId(event_id)}
        event_delete = self.event_collection.delete_one(event_filter_dict)
        return event_delete

    def get_events_by_folder_id(self, folder_id: str):
        """
        Allows you to make a query to the database to return the events that contain the folder_id.
        
        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Returns:
        -------
        returns dictionaries of the events that contain the folder_id.
        """
        event_filter_dict = {"folder_id": ObjectId(folder_id)}
        events = self.event_collection.find(event_filter_dict)
        return events
    
    def delete_events_by_folder_id(self, folder_id: str):
        """
        Allows to delete events by they folder_id.
        
        Attributes:
        ----------
        folder_id (str): A text string representing the ID of an folder.

        Returns:
        -------
        returns a instance "DeleteResult" from PyMongo 
        """
        event_data_filter = {"folder_id": ObjectId(folder_id)}
        events_deleted = self.event_collection.delete_many(event_data_filter)
        return events_deleted