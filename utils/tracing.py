from openinference.instrumentation.haystack import HaystackInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

def start_tracing():
    endpoint = "http://0.0.0.0:6006/v1/traces"
    tracer_provider = trace_sdk.TracerProvider()
    tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

    HaystackInstrumentor().instrument(tracer_provider=tracer_provider)
