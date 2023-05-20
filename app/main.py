from fastapi import Depends, FastAPI, exceptions
from loguru import logger

from app.routers import media_route, tweet_route, user_route
from app.utils.database import engine
from app.utils.exceptions import (
    logging_dependency,
    my_exception_handler,
    my_validation_exception_handler,
)
from app.utils.logconfig import init_logger

init_logger()
app = FastAPI(debug=True)
app.add_exception_handler(
    exceptions.RequestValidationError, handler=my_validation_exception_handler
)
app.add_exception_handler(exceptions.HTTPException, handler=my_exception_handler)
app.include_router(
    user_route.router,
    prefix="/api",
    tags=["users"],
    dependencies=[Depends(logging_dependency)],
)
app.include_router(
    media_route.router,
    prefix="/api",
    tags=["medias"],
    dependencies=[Depends(logging_dependency)],
)
app.include_router(
    tweet_route.router,
    prefix="/api",
    tags=["tweets"],
    dependencies=[Depends(logging_dependency)],
)


@app.on_event("startup")
async def startup():
    logger.info("Server started")


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
