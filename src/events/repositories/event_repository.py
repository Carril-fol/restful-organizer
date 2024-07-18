from bson import ObjectId
from database.db import Database
from events.models.event_model import EventModel

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
    
    def create_event(self, event_instance_model: EventModel):
        """
        Formats the input model instance to a dictionary and inserts it into the corresponding collection of events.

        Attributes:
        ----------
        event_instance_model (EventModel): An instance from "EventModel".

        Returns:
        -------
        The id inserted in the data collection
        """
        event_model_dump = event_instance_model.model_dump(by_alias=True)
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
        event_id (dtr): A text string representing the ID of an event.
        data (dict): A dictionary with the new data for the event.

        Returns:
        -------
        The id inserted in the data collection.
        """
        event_filter_dict = {"_id": ObjectId(event_id)}
        event_new_data_dict = {"$set": data}
        event_updated = self.event_collection.update_one(event_filter_dict, event_new_data_dict)
        return event_updated.upserted_id
    
    def delete_event(self, event_id: str):
        event_filter_dict = {"_id": ObjectId(event_id)}
        event_delete = self.event_collection.delete_one(event_filter_dict)
        return event_delete
