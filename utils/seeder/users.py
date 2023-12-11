import time

from bson import Int64

from domain.model.user import UserModel
from repository.user import UserRepo
from utils import helper


def seedUsers(
    user_repo: UserRepo,
):
    time_now = Int64(time.time())
    user_list = [
        UserModel(
            id=helper.generateUUID(),
            username="superuser",
            password=helper.hashPassword("superuser"),
            created_at=time_now,
            updated_at=time_now,
        )
    ]

    for user in user_list:
        existing_user = user_repo.getByUsername(user.username)
        user_repo.create(user)
