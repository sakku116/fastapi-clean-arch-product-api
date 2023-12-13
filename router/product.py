
from fastapi import APIRouter, Depends

from core.dependencies import verifyToken
from domain.rest import generic_resp
from service.product import ProductService

ProductRouter = APIRouter(
    prefix="/products", tags=["Product"], dependencies=[verifyToken]
)


@ProductRouter.get("")
def get_products(
    product_service: ProductService = Depends(),
):
    pass


@ProductRouter.get("/{id}")
def get_product_by_id(id: str, product_service: ProductService = Depends()):
    pass


@ProductRouter.post("")
def create_product(product_service: ProductService = Depends()):
    pass


@ProductRouter.patch("/{id}")
def patch_product(id: str, product_service: ProductService = Depends()):
    pass


@ProductRouter.delete("/{id}")
def delete_product(id: str, product_service: ProductService = Depends()):
    pass
