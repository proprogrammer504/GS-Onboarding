from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime

from backend.utils.logging import logger

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middle are to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method
        time_start = datetime.now()
        try:
            body = await request.json()
        except Exception:
            body = None

        if body:
            params = body["params"]
        else:
            params = None

        logger.info(f"Request params: {params}")
        logger.info(f"Time of call: {time_start}")

        response = await call_next(request)

        time_end = datetime.now()
        time_diff = time_end - time_start
        time_diff_ms = time_diff.total_seconds() * 1000

        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Length of call (ms): {time_diff_ms}")
        return response
