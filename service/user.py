from fastapi import Depends
from repository.user import UserRepo


class UserService:
    def __init__(
        self,
        user_repo: UserRepo = Depends(),
    ):
        self.user_repo = user_repo
