from fastapi import Depends
from repository.product import ProductRepo

class ProductService:
    def __init__(self, product_repo: ProductRepo = Depends()):
        self.product_repo = product_repo