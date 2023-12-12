from pydantic import BaseModel


class PostLoginReq(BaseModel):
    username: str
    password: str


class PostRegisterReq(BaseModel):
    username: str
    password: str


class PostResetPasswordReq(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class PostCheckTokenReq(BaseModel):
    token: str

class PostRefreshTokenReq(BaseModel):
    refresh_token: str