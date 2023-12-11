from .base_model import MyBaseModel

COLL = "users"

class UserModel(MyBaseModel):
    _coll_name: str = "users"

    username: str = ""
    password: str = ""