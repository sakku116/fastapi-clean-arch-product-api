from . import base_model


class OrderModel(base_model.MyBaseModel):
    _coll_name = "orders"

    quantity: int = 0
    id_product: str = ""
    id_user: str = ""
