from fastapi import Request
from fastapi.responses import JSONResponse

from exception.http import CustomHTTPExc
from domain.rest import generic_resp


async def customHttpExceptionHandler(request: Request, exc: CustomHTTPExc):
    return JSONResponse(
        status_code=exc.status_code,
        content=generic_resp.BaseResp(
            error=True, message=exc.message, data=None, error_detail=exc.detail
        ).model_dump(),
    )

async def defaultHttpExceptionHandler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=generic_resp.BaseResp(
            error=True,
            message="something went wrong",
            error_detail=str(exc),
        ).model_dump(),
    )
