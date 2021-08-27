from fastapi import Request, Response
from loguru import logger
from opencensus.trace.samplers import AlwaysOnSampler
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer

from .http import HTTP_HOST, HTTP_METHOD, HTTP_PATH, HTTP_STATUS_CODE, HTTP_URL
from .metrics import propagator, trace_exporter

tracer = Tracer(
    sampler=AlwaysOnSampler(),
    exporter=trace_exporter,
    propagator=propagator,
)


async def pre(request: Request):
    try:
        tracer.span_context = propagator.from_headers(request.headers)
    except Exception:  # noqa
        logger.error("Failed to trace request", exc_info=True)
        return

    try:
        span = tracer.start_span()
        span.span_kind = SpanKind.SERVER
        span.name = "[{}]{}".format(request.method, request.url)
        tracer.add_attribute_to_current_span(HTTP_HOST, request.url.hostname)
        tracer.add_attribute_to_current_span(HTTP_METHOD, request.method)
        tracer.add_attribute_to_current_span(HTTP_PATH, request.url.path)
        tracer.add_attribute_to_current_span(HTTP_URL, str(request.url))

    except Exception:  # noqa
        logger.error("Failed to trace request", exc_info=True)
        return


async def post(response: Response):
    try:
        tracer.add_attribute_to_current_span(
            HTTP_STATUS_CODE, response.status_code  # noqa
        )
        response.headers.append("TRACE-ID", tracer.span_context.trace_id)
    except Exception:  # noqa
        logger.error("Failed to trace response", exc_info=True)
        return
    finally:
        tracer.end_span()
