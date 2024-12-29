from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from bson import ObjectId

from exceptions.task_exception import StatusNotValid

class TaskModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name: str
    body: Optional[str] = None
    status: Optional[Literal["Completo", "Incompleto", "En Proceso"]]
    folder_id: ObjectId = Field(alias="folder_id")

    @field_validator("status")
    def valid_status(cls, value):
        status_list = ["Completo", "Incompleto", "En Proceso"]
        if value not in status_list:
            raise StatusNotValid()
        return value

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }