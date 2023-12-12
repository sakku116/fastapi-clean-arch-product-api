from pydantic import BaseModel


def respBuilder(
    base_resp: BaseModel, data_schema: BaseModel, data: BaseModel or list[BaseModel]
):
    """
    build response object with base resp and transformed `input` data into `schema` object.
    basically its just simple as we doing like:
    ```
    return baseRespSchema[respSchema](data=rawDataSchema)
    ```
    but it will raise error cuz the `data` type is not same as `respSchema`.

    args:
        - base_resp: object from `domain.rest.generic_resp` module.
        - data_schema: callable object of pydantic `BaseModel` to map the input data.
        - data: object of pydantic `BaseModel` or `list[BaseModel]`.

    usage:
    ```
        from domain.rest.generic_resp import RespData
        from domain.rest.user_resp import GetUsersResp
        from domain.rest.user_req import GetUsersReq

        @router.get("/users")
        def get_users(
            query: GetUsersReq = Depends(),
        ):
            users, count = [], 0
            return respBuilder(
                base_resp=RespData(),
                data_schema=GetUsersResp,
                data=users, # can be single a object or list
            )
    ```
    """
    if hasattr(base_resp, "data"):
        if type(data) == list:
            data = [data_schema(**item.model_dump()) for item in data]
        else:
            data = data_schema(**data.model_dump())
        setattr(base_resp, "data", data)

    return base_resp


def generatePaginationNumberList(
    current_page: int = 1, amount: int = 10, data_count: int = 0
):
    page_total = int(((data_count - 1) / amount) + 1)
    if page_total <= 5:
        return [i for i in range(1, page_total + 1)]

    max_page_num_left = 2
    if current_page < 3:
        max_page_num_left = current_page - 1
    max_page_num_right = 5 - 1 - max_page_num_left
    if page_total - current_page < 3:
        max_page_num_right = page_total - current_page
        max_page_num_left = 5 - 1 - max_page_num_right

    return (
        [i for i in range(current_page - max_page_num_left, current_page)]
        + [current_page]
        + [i for i in range(current_page + 1, max_page_num_right + current_page + 1)]
    )
