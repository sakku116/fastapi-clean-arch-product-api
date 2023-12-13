from pydantic import BaseModel
from bson import Int64
from .base import BaseModelSchema


class BaseUserResp(BaseModel):
    username: str = ""
    role: str = ""
    is_active: bool = True
    last_login: int = 0


class GetUsersResp(BaseUserResp, BaseModelSchema):
    pass


class GetUserByIdResp(BaseUserResp, BaseModelSchema):
    pass


class PostCreateUserResp(BaseUserResp, BaseModelSchema):
    pass

class PatchUserResp(BaseUserResp, BaseModelSchema):
    pass
