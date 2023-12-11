import logging

from pymongo.database import Database

from domain.model import user

logger = logging.getLogger(__name__)


def ensureIndexes(db: Database):
    logger.info("Ensuring mongodb collection indexes")

    models = [user.UserModel()]
    for model in models:
        logger.info(f"\tEnsuring index for '{model._coll_name}' collection")
        for index in model._indexes:
            logger.info(f"\t\tindex: {index.model_dump()}")
            db[model._coll_name].create_index(**index.model_dump())
