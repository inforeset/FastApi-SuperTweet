import logging

from fastapi import FastAPI, exceptions

from app.routers import user_route, media_route, tweet_route
from app.utils.database import engine, Base
from app.utils.exceptions import my_validation_exception_handler, my_exception_handler

app = FastAPI()
app.add_exception_handler(
    exceptions.RequestValidationError, handler=my_validation_exception_handler
)
app.add_exception_handler(
    exceptions.HTTPException, handler=my_exception_handler
)
app.include_router(user_route.router, prefix='/api', tags=['users'])
app.include_router(media_route.router, prefix='/api', tags=['medias'])
app.include_router(tweet_route.router, prefix='/api', tags=['tweets'])


@app.on_event("startup")
async def startup():
    ...
    # logger = logging.getLogger(__name__)
    # logging.config.dictConfig(dictLogConfig)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
