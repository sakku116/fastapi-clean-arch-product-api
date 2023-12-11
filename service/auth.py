import logging
from datetime import datetime, timedelta

from fastapi import Depends

from config.env import Env
from exception.http import CustomHTTPExc
from repository.user import UserRepo
from utils import bcrypt as bcrypt_utils
from utils import helper

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repo: UserRepo = Depends()):
        self.user_repo = user_repo

    def login(self, username: str, password: str) -> str:
        user = self.user_repo.getByUsername(username)
        if not user:
            exc = CustomHTTPExc(
                status_code=401,
                message="Invalid username or password",
            )
            logger.error(exc)
            raise exc

        is_pw_match = bcrypt_utils.checkPassword(password, user.password)
        if not is_pw_match:
            exc = CustomHTTPExc(
                status_code=401,
                message="Invalid username or password",
            )
            logger.error(exc)
            raise exc

        jwt_payload = user.model_dump()
        jwt_payload["exp"] = datetime.now() + timedelta(hours=Env.JWT_EXP)
        jwt_payload["user_id"] = user.id
        for field in ["password", "id"]:
            try:
                del jwt_payload[field]
            except:
                pass

        encoded_jwt = helper.encodeJWT(jwt_payload, Env.JWT_SECRET)
        return encoded_jwt