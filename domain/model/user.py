from .base_model import MyBaseModel

COLL = "users"

class UserModel(MyBaseModel):
    username: str = ""
    password: str = ""