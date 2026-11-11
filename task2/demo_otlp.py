"""Task 2 (E): the Task 1 program, now exporting spans over OTLP/gRPC
to the OpenTelemetry Collector running in Docker (localhost:4317)."""
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

provider = TracerProvider(resource=Resource.create({"service.name": "a8-demo"}))

# Replace the console exporter with the OTLP exporter.
exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("a8.demo")

with tracer.start_as_current_span("checkout") as parent:
    parent.set_attribute("order.id", "A8-001")
    with tracer.start_as_current_span("charge-card") as child:
        child.set_attribute("payment.amount", 499)
        child.add_event("card authorized")
        print("paid")

print(f"sent trace_id={parent.get_span_context().trace_id:032x} to the collector")

# BatchSpanProcessor buffers spans; shutdown() flushes them before exit.
provider.shutdown()
