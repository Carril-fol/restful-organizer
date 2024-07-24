from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId
from typing import Optional

from events.exceptions.event_exception import EventEndDateException, EventStartDateException

class EventModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name_event: str
    folder_id: ObjectId = Field(alias="folder_id")
    localization: str
    date_created: Optional[datetime] = datetime.now()
    start_date: datetime
    end_date: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

"""
    @field_validator("start_date")
    def valid_start_date(cls, value):
        date_today = datetime.now().date()
        start_date_format_date = value.date()
        if start_date_format_date < date_today:
            raise EventStartDateException()
        return value
    
    @field_validator("end_date")
    def valid_end_date(cls, value):
        date_today = datetime.now().date()
        end_date_format_date = value.date()
        if end_date_format_date < date_today:
            raise EventEndDateException()
        return value
"""