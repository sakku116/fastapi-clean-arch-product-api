from pydantic import BaseModel
from bson import Int64


class MyBaseModel(BaseModel):
    _id: str = ""
    created_at: Int64 = 0
    updated_at: Int64 = 0
