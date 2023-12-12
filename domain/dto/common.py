from pydantic import BaseModel
from typing import Literal

class CommonPagination(BaseModel):
    page: int = 1
    limit: int = 10
    sort_by: str = "created_at"
    sort_order: Literal["asc", "desc"] = "desc"