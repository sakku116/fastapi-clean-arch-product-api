from pydantic import BaseModel
from bson import Int64

class BaseModelSchema(BaseModel):
    id: str = ""
    created_at: int = 0
    updated_at: int = 0
    class Config:
        arbitrary_types_allowed = True
