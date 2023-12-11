from fastapi import Depends
from pymongo import ReturnDocument
from pymongo.database import Database

from config.mongodb import getMongoDB
from domain.model.user import UserModel


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

    def update(self, _id: str, user: UserModel) -> UserModel or None:
        _return = self.coll.find_one_and_update(
            {"_id": _id},
            {"$set": user.model_dump(exclude={"_id"})},
            return_document=ReturnDocument.AFTER,
        )
        return UserModel(**_return) if _return else None

    def patch(self, _id: str, user: UserModel) -> UserModel or None:
        _return = self.coll.find_one_and_update(
            {"_id": _id},
            {"$set": user.model_dump(exclude={"_id"}, exclude_unset=True)},
            return_document=ReturnDocument.AFTER,
        )
        return UserModel(**_return) if _return else None

    def delete(self, _id: str) -> UserModel or None:
        user = self.coll.find_one_and_delete({"_id": _id})
        return UserModel(**user) if user else None

    def getById(self, _id: str) -> UserModel or None:
        user = self.coll.find_one({"_id": _id})
        return UserModel(**user) if user else None

    def getByUsername(self, username: str) -> UserModel or None:
        user = self.coll.find_one({"username": username})
        return UserModel(**user) if user else None

    def getList(
        self,
        username: str = "",
        page: int = 1,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> list[UserModel]:
        users = (
            self.coll.find(username)
            .skip((page - 1) * limit)
            .limit(limit)
            .sort(sort_by, 1 if sort_order == "asc" else -1)
        )
        return [UserModel(**user) for user in users]
