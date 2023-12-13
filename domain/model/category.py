from . import base_model


class CategoryModel(base_model.MyBaseModel):
    _coll_name = "categories"

    name: str = ""
