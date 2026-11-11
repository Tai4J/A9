#!/usr/bin/env bash
# Start the Flask app under the OpenTelemetry zero-code agent.
export OTEL_SERVICE_NAME=a8-shop
export OTEL_RESOURCE_ATTRIBUTES=service.version=1.0.0,deployment.environment=lab
export OTEL_TRACES_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_METRICS_EXPORTER=none
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_INSECURE=true
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true   # send logs via OTLP
export OTEL_PYTHON_LOG_CORRELATION=true                        # add trace_id to console logs
export OTEL_PYTHON_LOG_LEVEL=info
opentelemetry-instrument python app.py
