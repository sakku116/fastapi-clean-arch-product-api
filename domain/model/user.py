from . import base_model

COLL = "users"


class UserModel(base_model.MyBaseModel):
    _coll_name = "users"
    _indexes = [
        base_model._MyBaseModel_Index(
            keys=[("id", 1)],
            unique=True
        ),
        base_model._MyBaseModel_Index(
            keys=[("username", -1)],
            unique=True
        )
    ]

    username: str = ""
    password: str = ""
