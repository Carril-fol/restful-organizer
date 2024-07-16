from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, Field

class FolderModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name_folder: str
    user_id: ObjectId = Field(alias="user_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }