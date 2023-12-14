from fastapi import APIRouter, Depends

from core.dependencies import adminOnly
from domain.model.user import UserModel
from domain.rest import generic_resp, user_req, user_resp
from service.user import UserService
from utils.resp import respBuilder

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

    return generic_resp.RespPaginatedData[user_resp.GetUsersResp](
        pagination_meta=generic_resp.PaginationMeta(
            total=user_count, page=query.page, limit=query.limit
        ),
        data=[user.model_dump() for user in user_list],
    )


@UserRouter.get(
    "/{id}", response_model=generic_resp.RespData[user_resp.GetUserByIdResp]
)
def get_user_by_id(
    id: str,
    user_service: UserService = Depends(),
):
    user = user_service.getById(id)
    return generic_resp.RespData[user_resp.GetUserByIdResp](
        data=user.model_dump(),
    )


@UserRouter.post("", response_model=generic_resp.RespData[user_resp.PostCreateUserResp])
def create_user(
    payload: user_req.PostCreateUserReq,
    user_service: UserService = Depends(),
    current_user: UserModel = Depends(adminOnly),
):
    user = user_service.createUser(schema=payload, curr_user_id=current_user.id)
    return generic_resp.RespData[user_resp.PostCreateUserResp](
        data=user.model_dump(),
    )


@UserRouter.patch(
    "/{id}", response_model=generic_resp.RespData[user_resp.PatchUserResp]
)
def patch_user(
    id: str,
    payload: user_req.PatchUserReq,
    user_service: UserService = Depends(),
    current_user: UserModel = Depends(adminOnly),
):
    user = user_service.patchUser(id=id, schema=payload, curr_user_id=current_user.id)
    return generic_resp.RespData[user_resp.PatchUserResp](
        data=user.model_dump(),
    )

@UserRouter.delete("/{id}", response_model=generic_resp.BaseResp)
def delete_user(id: str, user_service: UserService = Depends()):
    deleted_user = user_service.deleteUser(id=id)
    return generic_resp.BaseResp(
        message=f"User {deleted_user.username} deleted successfully",
    )
