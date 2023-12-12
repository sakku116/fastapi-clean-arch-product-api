import logging
from datetime import datetime, timedelta

from fastapi import Depends
from jwt import exceptions as jwt_exceptions

from config.env import Env
from core.exceptions.http import CustomHTTPExc
from domain.model.user import UserModel
from repository.user import UserRepo
from utils import bcrypt as bcrypt_utils
from utils import helper
from utils import jwt as jwt_utils

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, user_repo: UserRepo = Depends()):
        self.user_repo = user_repo

    def login(self, username: str, password: str) -> tuple[str, str]:
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
        jwt_payload["user_id"] = user.id
        jwt_payload["exp"] = datetime.now() + timedelta(hours=Env.JWT_EXP)
        for field in ["password", "id"]:
            try:
                del jwt_payload[field]
            except:
                pass

        token = jwt_utils.encodeToken(jwt_payload, Env.JWT_SECRET)

        # refresh token
        jwt_payload["exp"] = datetime.now() + timedelta(hours=Env.JWT_REFRESH_EXP)
        refresh_token = jwt_utils.encodeToken(jwt_payload, Env.JWT_REFRESH_SECRET)

        return token, refresh_token

    def checkToken(self, token: str) -> UserModel:
        token = token.removeprefix("Bearer ")

        claims = {}
        user_id = ""
        try:
            claims = jwt_utils.decodeToken(token, Env.JWT_SECRET)
            user_id = claims["user_id"]
        except jwt_exceptions.ExpiredSignatureError as e:
            exc = CustomHTTPExc(
                status_code=401,
                message="Token expired",
            )
            logger.error(exc)
            raise exc
        except Exception as e:
            exc = CustomHTTPExc(
                status_code=401,
                message="Invalid token",
            )

        user = self.user_repo.getById(id=user_id)
        if not user:
            exc = CustomHTTPExc(
                status_code=401,
                message="Invalid token",
            )
            logger.error(exc)
            raise exc

        return user

    def refreshToken(self, refresh_token: str) -> tuple[str, str]:
        claims = {}
        user_id = ""
        try:
            claims = jwt_utils.decodeToken(refresh_token, Env.JWT_REFRESH_SECRET)
            user_id = claims["user_id"]
        except jwt_exceptions.ExpiredSignatureError as e:
            exc = CustomHTTPExc(
                status_code=401,
                message="Token expired",
            )
            logger.error(exc)
            raise exc
        except Exception as e:
            exc = CustomHTTPExc(
                status_code=401,
                message="Invalid token",
            )

        user = self.user_repo.getById(id=user_id)
        if not user:
            exc = CustomHTTPExc(
                status_code=401,
                message="Invalid token",
            )
            logger.error(exc)
            raise exc

        jwt_payload = user.model_dump()
        jwt_payload["user_id"] = user.id
        jwt_payload["exp"] = datetime.now() + timedelta(hours=Env.JWT_EXP)
        for field in ["password", "id"]:
            try:
                del jwt_payload[field]
            except:
                pass
        token = jwt_utils.encodeToken(jwt_payload, Env.JWT_SECRET)

        # refresh token
        jwt_payload["exp"] = datetime.now() + timedelta(hours=Env.JWT_REFRESH_EXP)
        refresh_token = jwt_utils.encodeToken(jwt_payload, Env.JWT_REFRESH_SECRET)

        return token, refresh_token

    def register(self, username: str, password: str) -> UserModel:
        # validate password
        if " " in password:
            exc = CustomHTTPExc(
                status_code=400,
                message="Password cannot contain spaces",
            )
            logger.error(exc)
            raise exc

        user = self.user_repo.getByUsername(username)
        if user:
            exc = CustomHTTPExc(
                status_code=400,
                message="Username already exists",
            )
            logger.error(exc)
            raise exc

        hashed_pw = bcrypt_utils.hashPassword(password)
        time_now = helper.generateTimeNowEpoch()
        user = self.user_repo.create(
            UserModel(
                id=helper.generateUUID(),
                username=username,
                password=hashed_pw,
                created_at=time_now,
                updated_at=time_now,
            )
        )

        return user

    def resetPassword(
        self, old: str, new: str, confirm: str, current_user: UserModel
    ) -> UserModel:
        if new != confirm:
            exc = CustomHTTPExc(
                status_code=400,
                message="New password and confirm password not match",
            )
            logger.error(exc)
            raise exc

        user = self.user_repo.getById(id=current_user.id)
        is_pw_match = bcrypt_utils.checkPassword(old, user.password)
        if not is_pw_match:
            exc = CustomHTTPExc(
                status_code=401,
                message="Password incorrect",
            )
            logger.error(exc)
            raise exc

        hashed_pw = bcrypt_utils.hashPassword(new)
        time_now = helper.generateTimeNowEpoch()
        user = self.user_repo.patch(
            id=current_user.id,
            user=UserModel(
                password=hashed_pw,
                updated_at=time_now,
            ),
        )

        return user
