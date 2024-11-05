from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field, field_validator

from exceptions.folder_exception import FolderNameException

class SubFolderModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name: str
    folder_id: ObjectId = Field(alias="folder_id")

    @field_validator("name_folder")
    def valid_name_folder(cls, value):
        if len(value) == 0:
            raise FolderNameException()
        return value

    @field_validator("folder_id")
    def validate_if_folder_id_is_object_id(cls, value):
        if not ObjectId(value):
            raise ValueError("The entered ObjectID must be valid")
        return value

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }