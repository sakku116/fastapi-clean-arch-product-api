import logging
import time

from bson import Int64

from config.env import Env
from domain.model.user import UserModel
from repository.user import UserRepo
from utils import bcrypt as bcrypt_utils
from utils import helper

logger = logging.getLogger(__name__)


def seedUsers(
    user_repo: UserRepo,
):
    logging.info("seeding users")
    time_now = Int64(time.time())
    user_list = [
        UserModel(
            id=helper.generateUUID(),
            username=Env.INITIAL_USERNAME,
            password=bcrypt_utils.hashPassword(Env.INITIAL_PASSWORD),
            role="admin",
            is_active=True,
            created_at=time_now,
            updated_at=time_now,
        )
    ]

    for user in user_list:
        logger.info(f"\tseeding user: {user.username}")
        existing_user = user_repo.getByUsername(user.username)
        if existing_user:
            logger.info(f"\tuser {user.username} already exists")
            continue
        user_repo.create(user)
