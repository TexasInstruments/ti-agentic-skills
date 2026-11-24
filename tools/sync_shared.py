#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Texas Instruments Incorporated
"""Vendor shared files into skills so every skill folder is self-contained.

Source of truth: shared/<group>/<src>
Mapping:         registry/<group>.yml  ->  shared: {<skill>: [{src: ..., dest: ...}]}
Result:          skills/<group>/<skill>/<dest> is a real copy (never a symlink).

  sync_shared.py          write/refresh the copies
  sync_shared.py --check  exit 1 if any copy differs (used in CI)

Edit shared/ only. Copies carry no header edits, so a plain byte comparison is exact.
"""
import filecmp
import os
import shutil
import sys

from common import ROOT, SHARED_DIR, SKILLS_DIR, registries


def pairs():
    for group, reg in registries().items():
        for skill, items in (reg.get("shared") or {}).items():
            for it in items or []:
                src = os.path.join(SHARED_DIR, group, it["src"])
                dst = os.path.join(SKILLS_DIR, group, skill, it["dest"])
                yield src, dst


def main():
    check = "--check" in sys.argv[1:]
    bad = 0
    for src, dst in pairs():
        if not os.path.isfile(src):
            print("sync_shared: missing source %s" % os.path.relpath(src, ROOT), file=sys.stderr)
            bad += 1
            continue
        same = os.path.isfile(dst) and filecmp.cmp(src, dst, shallow=False)
        if same:
            continue
        if check:
            print("sync_shared: out of date: %s (run tools/sync_shared.py)" %
                  os.path.relpath(dst, ROOT), file=sys.stderr)
            bad += 1
        else:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print("synced " + os.path.relpath(dst, ROOT))
    if bad:
        return 1
    if check:
        print("sync_shared: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
