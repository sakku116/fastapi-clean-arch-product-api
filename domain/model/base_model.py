from pydantic import BaseModel
from bson import Int64


class _MyBaseModel_Index(BaseModel):
    """
    this attributes is same as pymongo.collection.Collection.create_index() args
    """

    keys: list = []
    unique: bool = False


class MyBaseModel(BaseModel):
    """
    id field already indexed by default, but it need to be indexed manually if you set the _indexes field.
    """
    _coll_name: str = ""
    _indexes: list[_MyBaseModel_Index] = [
        _MyBaseModel_Index(keys=[("id", 1)], unique=True)
    ]

    id: str = ""
    created_at: Int64 = Int64(0)
    updated_at: Int64 = Int64(0)
    created_by: str = ""
    updated_by: str = ""

    class Config:
        arbitrary_types_allowed = True
