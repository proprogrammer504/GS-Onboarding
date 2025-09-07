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
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method
        time_start = datetime.now()
        request_body = None
        params = None

        try:
            if request.method == "POST":
                request_body = await request.json()
        except Exception as e:
            logger.info(f"Exception: {e}")

        if request_body:
            params = request_body["params"]

        logger.info(f"Request URL: {request.url}")
        logger.info(f"Request method: {request.method}")
        logger.info(f"Request params: {params}")
        logger.info(f"Time of call: {time_start}")

        try:
            response = await call_next(request)
        except Exception as e:
            response = Response("Internal Server Error", status_code=500)
            logger.info(f"Exception {e}")
            return response

        time_end = datetime.now()
        time_diff = time_end - time_start
        time_diff_ms = time_diff.total_seconds() * 1000
        response_header = response.headers
        response_body = {"data": None}

        try:
            response_body_bytes = [chunk async for chunk in response.body_iterator]
            response_body = b''.join(response_body_bytes).decode("utf-8")
        except Exception as e:
            logger.info(f"Exception {e}")

        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Body: {response_body}")
        logger.info(f"Response header: {response_header}")
        logger.info(f"Length of call (ms): {time_diff_ms}")

        return Response(content=response_body, status_code=response.status_code,
                        headers=dict(response.headers), media_type=response.media_type)
