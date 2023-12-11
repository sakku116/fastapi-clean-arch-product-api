from pydantic import BaseModel
from bson import Int64

class _MyBaseModel_Index(BaseModel):
    """
    this attributes is same as pymongo.collection.Collection.create_index() args
    """

    keys: list = []
    unique: bool = False

class MyBaseModel(BaseModel):
    _coll_name: str = ""
    _indexes: list[_MyBaseModel_Index] = [
        _MyBaseModel_Index(
            keys=[("id", 1)],
            unique=True
        )
    ]

    id: str = ""
    created_at: Int64 = Int64(0)
    updated_at: Int64 = Int64(0)

    class Config:
        arbitrary_types_allowed = True