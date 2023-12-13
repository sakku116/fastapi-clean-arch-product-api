import logging

from pymongo.database import Database

from domain.model import user
import os
import importlib
import inspect
from domain.model.base_model import MyBaseModel

logger = logging.getLogger(__name__)


def ensureIndexes(db: Database):
    logger.info("Ensuring mongodb collection indexes")

    model_filenames = os.listdir("domain/model")
    for filename in model_filenames:
        if filename.endswith(".py") and filename.removesuffix(".py") not in [
            "__init__",
            "base_model",
        ]:
            module_path = __import__(
                f"domain.model.{filename[:-3]}", fromlist=[filename[:-3]]
            )
            for member_name, member in inspect.getmembers(module_path):
                if inspect.isclass(member) and member_name.lower().endswith("model"):
                    member: MyBaseModel = member()
                    coll_name = member._coll_name
                    indexes = member._indexes
                    logger.info(f"\tEnsuring index for '{coll_name}' collection")
                    for index in indexes:
                        logger.info(f"\t\tindex: {index.model_dump()}")
                        db[coll_name].create_index(**index.model_dump())