#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Texas Instruments Incorporated
# Smoke test a running HTTP MCP server: initialize, list tools, and optionally
# search for and read the latest AM62X release notes on software-dl.ti.com.
# Usage: smoke-test.sh [URL]   (default http://127.0.0.1:7471/mcp)
# Set SMOKE_CALL_TOOLS=1 to also call the tools (needs internet access).
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

if [ "${SMOKE_CALL_TOOLS:-0}" = 1 ]; then
    call() {
        curl -sS --max-time 120 "${hdr[@]}" -H "mcp-session-id: $sid" \
            -d "{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":$1}" "$url"
    }
    out=$(call '{"name":"ti_processor_sdk_docs_search","arguments":{"query":"release notes","device":"AM62X","os":"linux","version":"latest","max_results":3}}')
    page=$(echo "$out" | grep -oE '[A-Za-z0-9_/.-]+\.html' | head -1 || true)
    [ -n "$page" ] || { echo "search returned no pages:"; echo "$out"; exit 1; }
    echo "search OK: $page"
    out=$(call "{\"name\":\"ti_processor_sdk_docs_read\",\"arguments\":{\"path\":\"$page\",\"device\":\"AM62X\",\"os\":\"linux\",\"version\":\"latest\"}}")
    echo "$out" | grep -q '"isError":false' && echo "$out" | grep -qi 'release' && [ "${#out}" -gt 500 ] || { echo "read failed or too short:"; echo "$out" | head -c 600; exit 1; }
    echo "read OK"
fi
echo "smoke test OK"
