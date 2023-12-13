from . import base_model


class ProductModel(base_model.MyBaseModel):
    _coll_name = "products"

    name: str = ""
    description: str = ""
    price: float = 0
    id_category: str = ""



