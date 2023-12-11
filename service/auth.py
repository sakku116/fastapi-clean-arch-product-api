from repository.user import UserRepo
from fastapi import Depends


class AuthService:
    def __init__(self, user_repo: UserRepo = Depends()):
        self.user_repo = user_repo
