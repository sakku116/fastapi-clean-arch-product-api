import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from domain.model.user import UserModel

from core.exceptions.http import CustomHTTPExc
from service.auth import AuthService

logger = logging.getLogger(__name__)
reusable_token = OAuth2PasswordBearer("/auth/login")


async def verifyToken(
    auth_service: AuthService = Depends(), token=Depends(reusable_token)
):
    current_user = auth_service.checkToken(token=token)
    return current_user

async def adminOnly(
    user: UserModel = Depends(verifyToken),
):
    """
    depends on verifyToken()
    """
    if user.role != "admin":
        raise CustomHTTPExc(
            status_code=403,
            message="You don't have permission to access this resource",
        )
    return user