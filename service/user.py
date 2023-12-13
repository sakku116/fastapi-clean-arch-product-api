import logging

from fastapi import Depends

from core.exceptions.http import CustomHTTPExc
from domain.dto import user as user_dto
from domain.model.user import UserModel
from domain.rest import user_req
from repository.user import UserRepo
from utils import bcrypt as bcrypt_utils
from utils import helper

logger = logging.getLogger(__name__)


class UserService:
    def __init__(
        self,
        user_repo: UserRepo = Depends(),
    ):
        self.user_repo = user_repo

    def get_list(self, schema: user_req.GetUsersReq) -> tuple[list[UserModel], int]:
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

    def createUser(
        self, schema: user_req.PostCreateUserReq, curr_user_id: str
    ) -> UserModel:
        # validate
        if " " in schema.username:
            exc = CustomHTTPExc(
                status_code=400,
                message="Username cannot contain spaces",
            )
            logger.error(exc)
            raise exc

        # validate password
        if " " in schema.password:
            exc = CustomHTTPExc(
                status_code=400,
                message="Password cannot contain spaces",
            )
            logger.error(exc)
            raise exc

        # check username existance
        existing_user = self.user_repo.getByUsername(schema.username)
        if existing_user:
            exc = CustomHTTPExc(
                status_code=400,
                message=f"Username {schema.username} already exists",
            )
            logger.error(exc)
            raise exc

        # create
        time_now = helper.generateTimeNowEpoch()
        user = self.user_repo.create(
            UserModel(
                id=helper.generateUUID(),
                username=schema.username,
                password=bcrypt_utils.hashPassword(schema.password),
                role=schema.role,
                is_active=True,
                created_at=time_now,
                updated_at=time_now,
                created_by=curr_user_id,
                updated_by=curr_user_id,
            )
        )

        return user

    def patchUser(
        self, id: str, schema: user_req.PatchUserReq, curr_user_id: str
    ) -> UserModel:
        time_now = helper.generateTimeNowEpoch()
        user_patch = UserModel(
            updated_by=curr_user_id,
            updated_at=time_now,
        )
        if schema.username != None:
            user_patch.username = schema.username
        if schema.password != None:
            user_patch.password = bcrypt_utils.hashPassword(schema.password)
        if schema.role != None:
            user_patch.role = schema.role
        if schema.is_active != None:
            user_patch.is_active = schema.is_active

        updated_user = self.user_repo.patch(id=id, user=user_patch)
        if not updated_user:
            exc = CustomHTTPExc(
                status_code=404,
                message=f"User with id {id} not found",
            )
            logger.error(exc)
            raise exc

        return updated_user
