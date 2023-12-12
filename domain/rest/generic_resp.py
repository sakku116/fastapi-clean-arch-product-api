from typing import Generic, TypeVar

from pydantic import BaseModel

from utils.resp import generatePaginationNumberList

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

    def __init__(
        self, total: int = 0, page: int = 0, limit: int = 0, show_all: bool = False
    ):
        """
        attributes will be calculated automatically by inputed __init__() args
        """
        super().__init__(
            total=total,
            current_page=0 if show_all else page,
            page_total=0 if not limit else int(((total - 1) / limit) + 1),
            page_num_list=[0]
            if show_all or not limit
            else generatePaginationNumberList(page, limit, total),
        )


class RespPaginatedData(BaseResp, Generic[M]):
    pagination_meta: PaginationMeta = PaginationMeta()
    data: list[M] = []
