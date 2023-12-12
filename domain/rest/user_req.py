from .common import CommonReq
from typing import Literal

class GetUsersReq(CommonReq):
    role: Literal["all", "user", "admin"] = "all"
    username: str = ""
    sort_by: Literal["created_at", "username"] = "created_at"