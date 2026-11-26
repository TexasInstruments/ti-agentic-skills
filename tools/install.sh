#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Texas Instruments Incorporated
# Offline/local installer: copy skills from a checkout into an agent skills directory.
# For online installs prefer: npx skills add TexasInstruments/ti-agentic-skills --skill <name>
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: tools/install.sh [--category <category>] [--skill <name>]... [--dest <dir>] [--list]

  --category <category>  install every skill in skills/<category>/
  --skill <name>         install one skill (repeatable; may be combined with --category)
  --dest <dir>           target skills directory (default: ./.claude/skills)
  --list                 list available categories and skills, then exit

Each skill is self-contained, so any selection installs cleanly.
USAGE
}

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
dest="./.claude/skills" category="" list=0
skills=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --category) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; category=$2; shift 2 ;;
    --skill) [[ $# -ge 2 ]] || { usage >&2; exit 2; }; skills+=("$2"); shift 2 ;;
    --dest)  [[ $# -ge 2 ]] || { usage >&2; exit 2; }; dest=$2; shift 2 ;;
    --list)  list=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "install.sh: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ $list -eq 1 ]]; then
  for g in "$repo"/skills/*/; do
    echo "$(basename "$g")"
    for s in "$g"*/; do
      [[ -f "$s/SKILL.md" ]] && echo "  $(basename "$s")"
    done
  done
  exit 0
fi

[[ -n "$category" || ${#skills[@]} -gt 0 ]] || { echo "install.sh: nothing selected" >&2; usage >&2; exit 2; }

if [[ -n "$category" ]]; then
  [[ -d "$repo/skills/$category" ]] || { echo "install.sh: unknown category: $category" >&2; exit 1; }
  for s in "$repo/skills/$category"/*/; do
    [[ -f "$s/SKILL.md" ]] && skills+=("$(basename "$s")")
  done
fi

mkdir -p "$dest"
for name in "${skills[@]}"; do
  src=$(compgen -G "$repo/skills/*/$name" | head -n1 || true)
  [[ -n "$src" && -f "$src/SKILL.md" ]] || { echo "install.sh: unknown skill: $name" >&2; exit 1; }
  rm -rf "${dest:?}/$name"
  cp -r "$src" "$dest/$name"
  echo "installed $name -> $dest/$name"
done
