from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from folders.exceptions.folder_exception import FolderNameException

class FolderModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name_folder: str
    user_id: ObjectId = Field(alias="user_id")

    @field_validator("name_folder")
    def valid_name_folder(cls, value):
        if len(value) == 0:
            raise FolderNameException()
        return value

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }