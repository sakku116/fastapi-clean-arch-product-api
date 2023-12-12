from fastapi import Depends
from pymongo import ReturnDocument
from pymongo.database import Database

from config.mongodb import getMongoDB
from domain.dto import user as user_dto
from domain.model.user import UserModel
import logging

logger = logging.getLogger(__name__)

class UserRepo:
    def __init__(
        self,
        db: Database = Depends(getMongoDB),
    ):
        self.db = db
        self.coll = db[UserModel()._coll_name]

    def create(self, user: UserModel) -> UserModel:
        self.coll.insert_one(user.model_dump())
        return user

    def update(self, id: str, user: UserModel) -> UserModel or None:
        _return = self.coll.find_one_and_update(
            {"id": id},
            {"$set": user.model_dump(exclude={"id"})},
            return_document=ReturnDocument.AFTER,
        )
        return UserModel(**_return) if _return else None

    def patch(self, id: str, user: UserModel) -> UserModel or None:
        _return = self.coll.find_one_and_update(
            {"id": id},
            {"$set": user.model_dump(exclude={"id"}, exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )
        return UserModel(**_return) if _return else None

    def delete(self, id: str) -> UserModel or None:
        user = self.coll.find_one_and_delete({"id": id})
        return UserModel(**user) if user else None

    def getById(self, id: str) -> UserModel or None:
        user = self.coll.find_one({"id": id})
        return UserModel(**user) if user else None

    def getByUsername(self, username: str) -> UserModel or None:
        user = self.coll.find_one({"username": username})
        return UserModel(**user) if user else None

    def getList(
        self,
        schema: user_dto.UserGetListParam
    ) -> list[UserModel]:
        filter = {"username": {"$regex": schema.username, "$options": "i"}}
        if schema.role:
            filter["role"] = schema.role
        users = (
            self.coll.find(filter)
            .skip((schema.page - 1) * schema.limit)
            .limit(schema.limit)
            .sort(schema.sort_by, 1 if schema.sort_order == "asc" else -1)
        )
        return [UserModel(**user) for user in users]

    def count(self, role: str = "", username: str = "") -> int:
        filter = {"username": {"$regex": username, "$options": "i"}}
        if role:
            filter["role"] = role
        return self.coll.count_documents(filter)
