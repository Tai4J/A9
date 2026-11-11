"""Join exported logs with exported traces by trace_id.

Reads the collector's file exports (OTLP JSON, one object per line)
and prints, for every trace, its span tree and the log lines that
were written while that trace was active.
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

out = Path(sys.argv[1] if len(sys.argv) > 1 else "out")


def lines(path):
    if not path.exists():
        sys.exit(f"missing {path} - is the collector running and the app sending data?")
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            yield json.loads(line)


spans, logs = defaultdict(list), defaultdict(list)
for batch in lines(out / "traces.json"):
    for rs in batch.get("resourceSpans", []):
        for ss in rs.get("scopeSpans", []):
            for s in ss.get("spans", []):
                spans[s["traceId"]].append(s)
for batch in lines(out / "logs.json"):
    for rl in batch.get("resourceLogs", []):
        for sl in rl.get("scopeLogs", []):
            for r in sl.get("logRecords", []):
                if r.get("traceId"):
                    logs[r["traceId"]].append(r)


def ms(s):
    return (int(s["endTimeUnixNano"]) - int(s["startTimeUnixNano"])) / 1e6


def tree(trace_spans, parent="", depth=0):
    for s in sorted(trace_spans, key=lambda x: int(x["startTimeUnixNano"])):
        if s.get("parentSpanId", "") == parent:
            err = "  ERROR" if s.get("status", {}).get("code") == 2 else ""
            print(f"  {'   ' * depth}{'└─ ' if depth else ''}{s['name']}  "
                  f"[{s['spanId']}]  {ms(s):.1f} ms{err}")
            tree(trace_spans, s["spanId"], depth + 1)


for tid, ts in spans.items():
    print(f"\nTRACE {tid}")
    tree(ts)
    for r in sorted(logs.get(tid, []), key=lambda x: int(x["timeUnixNano"])):
        body = r.get("body", {}).get("stringValue", "")
        print(f"    log {r.get('severityText', ''):7} span={r.get('spanId', '')}  {body}")

linked = sum(len(v) for k, v in logs.items() if k in spans)
total = sum(len(v) for v in logs.values())
print(f"\n{len(spans)} traces, {total} logs with a trace_id, {linked} matched to a span tree")
