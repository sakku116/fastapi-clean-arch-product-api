from fastapi import Depends

from domain.dto import user as user_dto
from domain.model.user import UserModel
from domain.rest import user_req
from repository.user import UserRepo
import logging
from core.exceptions.http import CustomHTTPExc

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
        self,
        user_repo: UserRepo = Depends(),
    ):
        self.user_repo = user_repo

    def get_list(
        self,
        schema: user_req.GetUsersReq
    ) -> tuple[list[UserModel], int]:
        user_list = self.user_repo.getList(
            schema=user_dto.UserGetListParam(
                role=schema.role if schema.role != "all" else "",
                username=schema.username,
                page=schema.page,
                limit=schema.limit,
                sort_by=schema.sort_by,
                sort_order=schema.sort_order,
            )
        )
        user_count = self.user_repo.count(
            role=schema.role if schema.role != "all" else "",
            username=schema.username,
        )

        return user_list, user_count

    def getById(self, id: str) -> UserModel:
        user = self.user_repo.getById(id)
        if not user:
            exc = CustomHTTPExc(
                status_code=404,
                message=f"User with id {id} not found",
            )
            logger.error(exc)
            raise exc

        return user
