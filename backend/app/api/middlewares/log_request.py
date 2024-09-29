import json
from functools import partial
import logging

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint


logger = logging.getLogger("app.api.middlewares.log_request")

class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # body = await request.body()
        # if body:
        #     logger.info(f"\"{
        #         request.method
        #         + " "
        #         + request.url.path
        #     }\" - {
        #         body
        #         .replace(b"\n", b"")
        #         .replace(b" ", b"")
        #     }")
        #
        #     # Create a new request object with the original body
        #     request = Request(request.scope, receive=async_partial(receive_with_body, body))

        response = await call_next(request)
        return response


async def receive_with_body(body: bytes, receive):
    async def inner():
        return {'type': 'http.request', 'body': body, 'more_body': False}
    return inner


def async_partial(func, *args, **kwargs):
    async def wrapper(*args, **kwargs):
        return await func(*args, **kwargs)
    return partial(wrapper, *args, **kwargs)
