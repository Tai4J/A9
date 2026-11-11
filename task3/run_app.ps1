# Windows PowerShell version of run_app.sh
$env:OTEL_SERVICE_NAME = "a8-shop"
$env:OTEL_RESOURCE_ATTRIBUTES = "service.version=1.0.0,deployment.environment=lab"
$env:OTEL_TRACES_EXPORTER = "otlp"
$env:OTEL_LOGS_EXPORTER = "otlp"
$env:OTEL_METRICS_EXPORTER = "none"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4317"
$env:OTEL_EXPORTER_OTLP_PROTOCOL = "grpc"
$env:OTEL_EXPORTER_OTLP_INSECURE = "true"
$env:OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED = "true"
$env:OTEL_PYTHON_LOG_CORRELATION = "true"
$env:OTEL_PYTHON_LOG_LEVEL = "info"
opentelemetry-instrument python app.py
