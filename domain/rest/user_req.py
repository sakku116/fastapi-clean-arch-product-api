from .common import CommonReq
from typing import Literal
from pydantic import BaseModel

class GetUsersReq(CommonReq):
    role: Literal["all", "user", "admin"] = "all"
    username: str = ""
    sort_by: Literal["created_at", "username"] = "created_at"

class PostCreateUserReq(BaseModel):
    username: str
    password: str
    role: Literal["admin", "user"]