"""Task 3 (O): Flask shop service.

Contains NO OpenTelemetry setup code: the zero-code agent
(`opentelemetry-instrument`) creates the server spans, exports them,
and attaches trace_id/span_id to every log record.
We only add two custom child spans with the OTel API.
"""
import logging
import random
import time

from flask import Flask, jsonify, request
from opentelemetry import trace

app = Flask(__name__)
log = logging.getLogger("a8.shop")
log.setLevel(logging.INFO)
tracer = trace.get_tracer("a8.shop")


@app.route("/checkout")
def checkout():
    item = request.args.get("item", "book")
    log.info("checkout started for item=%s", item)

    with tracer.start_as_current_span("validate-cart") as span:
        span.set_attribute("cart.item", item)
        time.sleep(random.uniform(0.01, 0.03))  # noqa: S311 (simulated latency, not crypto)
        log.info("cart validated")

    with tracer.start_as_current_span("charge-card") as span:
        amount = 499
        span.set_attribute("payment.amount", amount)
        time.sleep(random.uniform(0.05, 0.15))  # noqa: S311 (simulated latency, not crypto)
        log.info("payment of %d TWD accepted", amount)

    return jsonify(status="paid", item=item)


@app.route("/fail")
def fail():
    log.warning("payment gateway timeout, about to fail")
    try:
        raise RuntimeError("payment gateway timeout")
    except RuntimeError:
        log.exception("checkout failed")
        raise


if __name__ == "__main__":
    # use_reloader=False: Flask's reloader starts a second process
    # that would not be instrumented.
    app.run(port=8080, debug=False, use_reloader=False)
