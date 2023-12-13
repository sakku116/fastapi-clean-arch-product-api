from fastapi import Depends
from config.mongodb import getMongoDB
from pymongo.database import Database
from domain.model.product import ProductModel

class ProductRepo:
    def __init__(self, db: Database = Depends(getMongoDB)):
        self.coll = db[ProductModel()._coll_name]