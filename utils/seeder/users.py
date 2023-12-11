import time

from bson import Int64

from domain.model.user import UserModel
from repository.user import UserRepo
from utils import bcrypt as bcrypt_utils, helper


def seedUsers(
    user_repo: UserRepo,
):
    time_now = Int64(time.time())
    user_list = [
        UserModel(
            id=helper.generateUUID(),
            username="superuser",
            password=bcrypt_utils.hashPassword("superuser"),
            created_at=time_now,
            updated_at=time_now,
        )
    ]

    for user in user_list:
        existing_user = user_repo.getByUsername(user.username)
        if existing_user:
            user_repo.delete(existing_user.id)
        user_repo.create(user)
