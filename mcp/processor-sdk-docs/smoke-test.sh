#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Texas Instruments Incorporated
# Smoke test a running HTTP MCP server: initialize, then list tools.
# Usage: smoke-test.sh [URL]   (default http://127.0.0.1:7471/mcp)
set -euo pipefail

url="${1:-http://127.0.0.1:7471/mcp}"
hdr=(-H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream')

for _ in $(seq 1 60); do
    curl -s -o /dev/null "$url" && break
    sleep 1
done

init='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"smoke","version":"0"}}}'
resp=$(curl -sS -D - "${hdr[@]}" -d "$init" "$url")
echo "$resp" | grep -q '"serverInfo"' || { echo "initialize failed:"; echo "$resp"; exit 1; }
sid=$(echo "$resp" | tr -d '\r' | awk -F': ' 'tolower($1)=="mcp-session-id"{print $2}')

curl -sS -o /dev/null "${hdr[@]}" -H "mcp-session-id: $sid" \
    -d '{"jsonrpc":"2.0","method":"notifications/initialized"}' "$url"
tools=$(curl -sS "${hdr[@]}" -H "mcp-session-id: $sid" \
    -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' "$url")
for t in ti_processor_sdk_docs_list_variants ti_processor_sdk_docs_search ti_processor_sdk_docs_read; do
    echo "$tools" | grep -q "$t" || { echo "missing tool: $t"; echo "$tools"; exit 1; }
done
echo "smoke test OK"
