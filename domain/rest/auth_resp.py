from pydantic import BaseModel

class AuthLoginBaseResp(BaseModel):
    error: bool = False
    message: str = "OK"
    error_detail: str = ""
    access_token: str = ""
    refresh_token: str = ""