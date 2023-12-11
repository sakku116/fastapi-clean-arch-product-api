from typing import TypeVar, Generic

from pydantic import BaseModel


"""
support schema detail in fastapi swaggers docs
example
@router.get("/users", response_model=RespDataWithMeta[list[dto.User]])
"""

M = TypeVar("M", bound=BaseModel)


class BaseResp(BaseModel):
    error: bool = False
    message: str = "OK"
    error_detail: str = ""


class RespData(BaseResp, Generic[M]):
    data: M = None  # support any object


class PaginationMeta(BaseModel):
    total: int = 0
    current_page: int = 0
    page_total: int = 0
    page_num_list: list[int] = [0]


class RespPaginatedData(BaseResp, Generic[M]):
    meta: PaginationMeta = PaginationMeta()
    data: list[M] = []
