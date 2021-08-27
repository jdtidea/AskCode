from httpx import AsyncClient, Request, Response
from loguru import logger
from opencensus.trace import attributes_helper

HTTP_HOST = attributes_helper.COMMON_ATTRIBUTES["HTTP_HOST"]
HTTP_METHOD = attributes_helper.COMMON_ATTRIBUTES["HTTP_METHOD"]
HTTP_PATH = attributes_helper.COMMON_ATTRIBUTES["HTTP_PATH"]
HTTP_ROUTE = attributes_helper.COMMON_ATTRIBUTES["HTTP_ROUTE"]
HTTP_URL = attributes_helper.COMMON_ATTRIBUTES["HTTP_URL"]
HTTP_STATUS_CODE = attributes_helper.COMMON_ATTRIBUTES["HTTP_STATUS_CODE"]
HTTP_RESPONSE_SIZE = attributes_helper.COMMON_ATTRIBUTES["HTTP_RESPONSE_SIZE"]
REQUEST_TIME = "http.response_time_ms"
ERROR = "error"


async def log_request(request: Request):
    # logger.debug(str(request.url), request.method)
    pass


async def log_response(response: Response):
    url = str(response.request.url)
    dimensions = {
        "custom_dimensions": {
            HTTP_METHOD: response.request.method,
            HTTP_URL: url,
            HTTP_STATUS_CODE: response.status_code,
            HTTP_RESPONSE_SIZE: response.num_bytes_downloaded,
            REQUEST_TIME: response.elapsed.microseconds,
            ERROR: response.is_error,
        }
    }
    logger.bind(**dimensions).info(url)


def async_client() -> AsyncClient:
    return AsyncClient(
        event_hooks={"request": [log_request], "response": [log_response]},
    )


# TODO: Replace this usage once publicly accessibly domains with a valid certs exist
def insecure_async_client() -> AsyncClient:
    return AsyncClient(
        event_hooks={"request": [log_request], "response": [log_response]}, verify=False
    )
