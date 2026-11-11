"""Send some requests to the Flask app (3 good, 1 failing)."""
import requests

for item in ["book", "pen", "laptop"]:
    r = requests.get("http://localhost:8080/checkout",
                     params={"item": item}, timeout=5)
    print(r.status_code, r.json())
r = requests.get("http://localhost:8080/fail", timeout=5)
print(r.status_code, "(expected 500)")
