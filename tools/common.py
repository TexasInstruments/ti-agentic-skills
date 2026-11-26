# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Texas Instruments Incorporated
"""Shared helpers for the repo tooling. Python 3.8+, needs PyYAML."""
import os
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, "skills")
REGISTRY_DIR = os.path.join(ROOT, "registry")
SHARED_DIR = os.path.join(ROOT, "shared")

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def registries():
    """Return {category: registry-dict} for every registry/<category>.yml (not _template)."""
    out = {}
    if not os.path.isdir(REGISTRY_DIR):
        return out
    for fn in sorted(os.listdir(REGISTRY_DIR)):
        if fn.endswith(".yml") and not fn.startswith("_"):
            reg = load_yaml(os.path.join(REGISTRY_DIR, fn))
            reg.setdefault("category", fn[:-4])
            reg["_file"] = fn
            out[reg["category"]] = reg
    return out


def skills_in_category(category):
    d = os.path.join(SKILLS_DIR, category)
    if not os.path.isdir(d):
        return []
    return sorted(
        s for s in os.listdir(d)
        if os.path.isfile(os.path.join(d, s, "SKILL.md"))
    )


def parse_frontmatter(path):
    """Return (frontmatter-dict, body-text). Raises ValueError on bad frontmatter."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if not m:
        raise ValueError("missing YAML frontmatter")
    fm = yaml.safe_load(m.group(1))
    if not isinstance(fm, dict):
        raise ValueError("frontmatter is not a mapping")
    return fm, m.group(2)
