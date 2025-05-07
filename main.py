import atexit
import logging.config
import logging.handlers
from contextlib import asynccontextmanager
from typing import AsyncContextManager

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from api import api_router
from core.config import uvicorn_options
from core.logger import listener, LOGGING_CONFIG

logger = logging.getLogger('root')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[None]:
    logging.config.dictConfig(LOGGING_CONFIG)
    try:
        listener.start()
        atexit.register(listener.stop)
        yield
    finally:
        listener.stop()


app = FastAPI(lifespan=lifespan, docs_url='/api/openapi')
app.include_router(api_router)


@app.exception_handler(Exception)
async def exception(request: Request, exc: Exception):
    logger.error(f'{request.url} | Error in application: {exc}')
    return JSONResponse(
        status_code=500,
        content={'message': exc})


@app.exception_handler(HTTPException)
async def exception(request: Request, exc: HTTPException):
    logger.error(f'{request.url} | Error in application: {exc}')
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': exc.detail})


@app.get('/')
async def root():
    return {'message': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run('main:app', **uvicorn_options)
