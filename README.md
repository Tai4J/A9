# A8 OpenTelemetry — 執行步驟與截圖清單

需要：Python 3.9+、Docker Desktop（已啟動）。以下指令在專案根目錄執行。
Windows 請用 PowerShell，`$PWD` 改寫成 `${PWD}`，`source .venv/bin/activate` 改成 `.venv\Scripts\Activate.ps1`。

## 0. 安裝
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
opentelemetry-bootstrap -a install      # 自動安裝 Flask / logging 等 instrumentation 套件
pip list | grep opentelemetry           # 截圖 0（版本清單，放 Environment 章節）
```

## Task 1（A）— Console 輸出
```bash
cd task1
python demo_console.py
```
📸 **截圖 1**：終端機輸出，要看得到兩個 span 的 `trace_id`（相同）、`span_id`、`parent_id`（charge-card 的 parent_id = checkout 的 span_id），以及最下方的 hierarchy summary。

## Task 2（E）— Docker Collector
終端機 A：
```bash
cd task2
mkdir -p out && chmod 777 out
docker run --rm --name otelcol -p 4317:4317 \
  -v "$PWD/otel-collector-config.yaml:/etc/otelcol/config.yaml" \
  -v "$PWD/out:/out" \
  otel/opentelemetry-collector:0.164.0
```
終端機 B：
```bash
cd task2 && source ../.venv/bin/activate
python demo_otlp.py
docker ps                         # 📸 截圖 2：container 正在執行、port 4317
docker logs otelcol               # 📸 截圖 3：debug exporter 印出的 checkout / charge-card span（找跟 demo_otlp.py 印出的 trace_id 一樣的）
head -c 1500 out/telemetry.json   # 📸 截圖 4：file exporter 寫出的 JSON
```
完成後在終端機 A 按 Ctrl+C 停止 collector。

## Task 3（O）— Flask 自動儀器化 + Log/Trace 關聯
終端機 A（collector，兩條 pipeline）：
```bash
cd task3
mkdir -p out && chmod 777 out
docker run --rm --name otelcol3 -p 4317:4317 \
  -v "$PWD/otel-collector-config.yaml:/etc/otelcol/config.yaml" \
  -v "$PWD/out:/out" \
  otel/opentelemetry-collector:0.164.0
```
終端機 B（Flask app）：
```bash
cd task3 && source ../.venv/bin/activate
./run_app.sh            # Windows: .\run_app.ps1
```
📸 **截圖 5**：Flask 的 console log，每行都有 `trace_id=... span_id=...`。

終端機 C：
```bash
cd task3 && source ../.venv/bin/activate
python traffic.py
sleep 6                  # 等 batch 匯出
docker logs otelcol3 | tail -20     # 📸 截圖 6：traces 與 logs 兩條 pipeline 都有收到資料
python correlate.py out             # 📸 截圖 7：每個 trace 的 span 樹 + 同一 trace 的 log（最重要的一張）
```

## 常見問題
- `StatusCode.UNAVAILABLE` / 連不到 4317：collector 沒啟動，或 config 寫成 localhost。
- out/ 沒有檔案：沒做 `chmod 777 out`，或程式還沒 flush（等 5 秒、或先停掉 app）。
- Flask 沒產生 span：不要用 `flask --debug`，reloader 會開一個沒被 instrument 的子程序。
- `opentelemetry-instrument` 找不到：venv 沒啟用，或沒裝 opentelemetry-distro。
