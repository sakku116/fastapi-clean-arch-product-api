from fastapi import APIRouter, Depends

from domain.rest.auth_req import (PostCheckTokenReq, PostLoginReq, PostRegisterReq,
                              PostResetPasswordReq)
from service.auth import AuthService

AuthRouter = APIRouter(
    prefix="/auth",
)


def login(payload: PostLoginReq, auth_service: AuthService = Depends()):
    pass


def register(payload: PostRegisterReq, auth_service: AuthService = Depends()):
    pass


def check_token(payload: PostCheckTokenReq, auth_service: AuthService = Depends()):
    pass


def reset_password(
    payload: PostResetPasswordReq, auth_service: AuthService = Depends()
):
    pass
