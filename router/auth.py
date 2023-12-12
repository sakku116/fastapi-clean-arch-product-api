from fastapi import APIRouter, Depends, Form

from domain.rest import auth_resp, generic_resp
from domain.rest import auth_req
from service.auth import AuthService
from domain.model.user import UserModel
from core.dependencies import verifyTokenDependency

AuthRouter = APIRouter(
    prefix="/auth",
)


@AuthRouter.post("/login", response_model=auth_resp.AuthLoginBaseResp)
def login(
    username: str = Form(),
    password: str = Form(),
    auth_service: AuthService = Depends(),
):
    token, refresh_token = auth_service.login(username=username, password=password)
    return auth_resp.AuthLoginBaseResp(
        error=False,
        message="OK",
        access_token=token,
        refresh_token=refresh_token,
    )


@AuthRouter.post("/check-token", response_model=generic_resp.BaseResp)
def check_token(
    payload: auth_req.PostCheckTokenReq, auth_service: AuthService = Depends()
):
    auth_service.checkToken(token=payload.token.removeprefix("Bearer "))
    return generic_resp.BaseResp(
        error=False,
        message="OK",
    )


@AuthRouter.post("/refresh-token", response_model=auth_resp.AuthLoginBaseResp)
def refresh_token(
    payload: auth_req.PostRefreshTokenReq, auth_service: AuthService = Depends()
):
    token, refresh_token = auth_service.refreshToken(payload.refresh_token)
    return auth_resp.AuthLoginBaseResp(
        error=False,
        message="OK",
        access_token=token,
        refresh_token=refresh_token,
    )


@AuthRouter.post("/register", response_model=generic_resp.BaseResp)
def register(payload: auth_req.PostRegisterReq, auth_service: AuthService = Depends()):
    user = auth_service.register(username=payload.username, password=payload.password)
    return generic_resp.BaseResp(
        error=False,
        message=f"User {user.username} registered successfully",
    )


@AuthRouter.post("/reset-password", response_model=generic_resp.BaseResp)
def reset_password(
    payload: auth_req.PostResetPasswordReq,
    auth_service: AuthService = Depends(),
    current_user: UserModel = Depends(verifyTokenDependency),
):
    user = auth_service.resetPassword(
        old=payload.old_password,
        new=payload.new_password,
        confirm=payload.confirm_password,
        current_user=current_user,
    )

    return generic_resp.BaseResp(
        error=False,
        message=f"User {user.username} reset password successfully",
    )
