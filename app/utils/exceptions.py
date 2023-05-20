from http.client import responses

from fastapi import Request
from loguru import logger
from starlette.responses import JSONResponse


async def my_validation_exception_handler(request, exc):
    logger.error("{} {} {}", request.method, request.url, exc.detail)
    logger.exception(exc)
    return JSONResponse(
        {"result": False, "error_type": "validation error", "error_message": str(exc)},
        status_code=422,
    )


async def my_exception_handler(request, exc):
    return JSONResponse(
        {
            "result": False,
            "error_type": responses[exc.status_code],
            "error_message": str(exc.detail),
        },
        status_code=exc.status_code,
    )


async def logging_dependency(request: Request):
    logger.debug("{} {}", request.method, request.url)
    logger.debug("Params:")
    for name, value in request.path_params.items():
        logger.debug("\t{}: {}", name, value)
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug("\t{}: {}", name, value)
