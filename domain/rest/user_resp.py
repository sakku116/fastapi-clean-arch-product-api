from pydantic import BaseModel
from bson import Int64
from .base import BaseModelSchema

class GetUsersResp(BaseModelSchema):
    username: str = ""
    role: str = ""
    is_active: bool = True
    last_login: int = 0

class GetUserByIdResp(BaseModelSchema):
    username: str = ""
    role: str = ""
    is_active: bool = True
    last_login: int = 0