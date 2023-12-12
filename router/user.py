from fastapi import APIRouter, Depends

from core.dependencies import adminOnly
from domain.rest import user_req
from service.user import UserService
from domain.rest import generic_resp, user_resp
from utils.resp import respBuilder
from domain.model.user import UserModel

UserRouter = APIRouter(
    prefix="/users",
    tags=["User"],
    dependencies=[Depends(adminOnly)],
)


@UserRouter.get(
    "", response_model=generic_resp.RespPaginatedData[user_resp.GetUsersResp]
)
def get_users(
    query: user_req.GetUsersReq = Depends(),
    user_service: UserService = Depends(),
):
    user_list, user_count = user_service.get_list(schema=query)
    return respBuilder(
        base_resp=generic_resp.RespPaginatedData(
            pagination_meta=generic_resp.PaginationMeta(
                total=user_count, page=query.page, limit=query.limit
            ),
        ),
        data_schema=user_resp.GetUsersResp,
        data=user_list,
    )


@UserRouter.get(
    "/{id}", response_model=generic_resp.RespData[user_resp.GetUserByIdResp]
)
def get_user_by_id(
    id: str,
    user_service: UserService = Depends(),
):
    user = user_service.getById(id)
    return respBuilder(
        base_resp=generic_resp.RespData(),
        data_schema=user_resp.GetUserByIdResp,
        data=user,
    )
