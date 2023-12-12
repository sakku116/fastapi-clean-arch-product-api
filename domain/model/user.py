from typing import Literal

from bson import Int64

from . import base_model


class UserModel(base_model.MyBaseModel):
    _coll_name = "users"
    _indexes = [
        base_model._MyBaseModel_Index(keys=[("id", 1)], unique=True),
        base_model._MyBaseModel_Index(keys=[("username", -1)], unique=True),
    ]

    username: str = ""
    password: str = ""
    role: Literal["admin", "user"] = "user"
    is_active: bool = True
    last_login: Int64 = Int64(0)
