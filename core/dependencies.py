import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.exceptions.http import CustomHTTPExc
from service.auth import AuthService

logger = logging.getLogger(__name__)
reusable_token = OAuth2PasswordBearer("/auth/login")


async def verifyTokenDependency(
    auth_service: AuthService = Depends(), token=Depends(reusable_token)
):
    current_user = auth_service.checkToken(token=token)
    return current_user
