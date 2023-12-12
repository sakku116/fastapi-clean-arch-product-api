from pydantic import BaseModel
from .common import CommonPagination

class UserGetListParam(CommonPagination):
    role: str = ""
    username: str = ""