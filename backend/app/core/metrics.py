from opencensus.ext.azure import metrics_exporter
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.propagation import trace_context_http_header_format

from .config import APPLICATIONINSIGHTS_CONNECTION_STRING

trace_exporter = AzureExporter(connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING)
metrics_exporter = metrics_exporter.new_metrics_exporter(
    connection_string=APPLICATIONINSIGHTS_CONNECTION_STRING
)
propagator = trace_context_http_header_format.TraceContextPropagator()
