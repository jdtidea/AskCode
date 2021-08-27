import logging

from loguru import logger
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace import config_integration, execution_context

from .config import APPLICATIONINSIGHTS_CONNECTION_STRING

# Configures trace and span ids in logs
config_integration.trace_integrations(["logging"])


class AzureProxyHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self._handler = AzureLogHandler(
            connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING
        )

    def emit(self, record: logging.LogRecord):
        if not hasattr(record, "custom_dimensions"):
            record.custom_dimensions = {}
        tracer = execution_context.get_opencensus_tracer()
        if tracer is not None:
            record.traceId = tracer.span_context.trace_id
            record.spanId = tracer.span_context.span_id
        if hasattr(record, "extra"):
            record.custom_dimensions = {
                **record.custom_dimensions,
                **record.extra.get("custom_dimensions", {}),
            }

        self._handler.emit(record)


def initialize_logger():
    # TODO: Fine-grained logging levels from remote config
    # loggers = ("uvicorn.asgi", "uvicorn.access", "uvicorn", "fastapi", "app.core.http")
    # Root logger
    logging.getLogger().handlers = [AzureProxyHandler()]
    # Add opencensus traces to logs
    logger.add(AzureProxyHandler())
