"""Task 1 (A): OpenTelemetry SDK with console output.

Creates a parent span ("checkout") and a child span ("charge-card")
and prints both spans to the console as JSON.
"""
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter

# 1. Tracer provider: the SDK object that creates spans.
#    The Resource describes *who* produces the telemetry.
provider = TracerProvider(resource=Resource.create({"service.name": "a8-demo"}))

# 2. Span processor + exporter: SimpleSpanProcessor hands every finished
#    span to the ConsoleSpanExporter immediately, which prints it as JSON.
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("a8.demo")

with tracer.start_as_current_span("checkout") as parent:            # parent span
    parent.set_attribute("order.id", "A8-001")
    with tracer.start_as_current_span("charge-card") as child:      # child span
        child.set_attribute("payment.amount", 499)
        child.add_event("card authorized")
        print("paid")

# Short summary so the hierarchy is easy to see in the screenshot.
p, c = parent.get_span_context(), child.get_span_context()
print("\n=== Span hierarchy summary ===")
print(f"trace_id      : {p.trace_id:032x}  (shared by both spans)")
print(f"checkout      : span_id={p.span_id:016x}  parent=None (root)")
print(f"└─ charge-card: span_id={c.span_id:016x}  parent={child.parent.span_id:016x}")

provider.shutdown()
