#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2026 Texas Instruments Incorporated
"""Validate the whole repo. Exit 1 on any error.

Checks:
  * every registry parses and has required keys
  * every skills/<group>/ has a registry, and every registry group has CODEOWNERS
  * skill: frontmatter, name == directory, name carries the group prefix,
    description <= 1024 chars, SKILL.md <= 500 lines, names unique repo-wide
  * bundles reference existing skills
  * no markdown link or script path escapes the skill folder (self-contained rule)
  * registry `shared` maps point at real files (content drift: tools/sync_shared.py --check)
"""
import os
import re
import sys

from common import (NAME_RE, ROOT, SKILLS_DIR, parse_frontmatter, registries,
                    skills_in_group)

errors = []


def err(msg):
    errors.append(msg)


REQUIRED_REG = ("name", "group", "description", "owners", "status", "license")
STATUSES = ("planned", "active", "deprecated")
LINK_RE = re.compile(r"\]\(([^)\s#]+)")
ESCAPE_RE = re.compile(r"(\.\./)+[\w.-]")


def check_skill(group, skill, seen):
    sdir = os.path.join(SKILLS_DIR, group, skill)
    path = os.path.join(sdir, "SKILL.md")
    rel = os.path.relpath(path, ROOT)
    try:
        fm, body = parse_frontmatter(path)
    except ValueError as e:
        return err("%s: %s" % (rel, e))
    name = fm.get("name")
    if name != skill:
        err("%s: name %r must equal directory %r" % (rel, name, skill))
    if not isinstance(name, str) or not NAME_RE.match(name) or len(name) > 64:
        err("%s: name must be lowercase-hyphen, <= 64 chars" % rel)
    prefix = group[:-len("-sdk-skills")] if group.endswith("-sdk-skills") else group[:-len("-skills")]
    if not skill.startswith(prefix + "-"):
        err("%s: skill name must start with %r" % (rel, prefix + "-"))
    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        err("%s: description missing" % rel)
    elif len(desc) > 1024:
        err("%s: description is %d chars (max 1024)" % (rel, len(desc)))
    meta = fm.get("metadata")
    if meta is not None and (not isinstance(meta, dict) or
                             any(not isinstance(k, str) or not isinstance(v, str)
                                 for k, v in meta.items())):
        err("%s: metadata must be a string-to-string map" % rel)
    with open(path, encoding="utf-8") as f:
        nlines = sum(1 for _ in f)
    if nlines > 500:
        err("%s: %d lines (max 500); move detail to references/" % (rel, nlines))
    if name in seen:
        err("%s: duplicate skill name, also in %s" % (rel, seen[name]))
    seen[name] = rel
    # self-containment: no link or path may leave the skill folder
    for root, _, files in os.walk(sdir):
        for fn in files:
            if not fn.endswith((".md", ".sh", ".py", ".yaml", ".yml")):
                continue
            p = os.path.join(root, fn)
            with open(p, encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    for target in LINK_RE.findall(line):
                        if "://" in target or target.startswith(("mailto:", "/")):
                            continue
                        full = os.path.normpath(os.path.join(root, target))
                        if not full.startswith(sdir + os.sep):
                            err("%s:%d: link %r leaves the skill folder" %
                                (os.path.relpath(p, ROOT), i, target))
                        elif not os.path.exists(full):
                            err("%s:%d: broken link %r" % (os.path.relpath(p, ROOT), i, target))
                    if fn.endswith((".sh", ".py")) and ESCAPE_RE.search(line) and \
                            not line.lstrip().startswith("#"):
                        err("%s:%d: path climbs out of the skill folder" %
                            (os.path.relpath(p, ROOT), i))


def main():
    regs = registries()
    if not regs:
        err("registry/: no group registries found")
    seen = {}
    codeowners = ""
    co = os.path.join(ROOT, ".github", "CODEOWNERS")
    if os.path.isfile(co):
        codeowners = open(co, encoding="utf-8").read()
    else:
        err(".github/CODEOWNERS missing")

    for group, reg in regs.items():
        f = "registry/" + reg["_file"]
        for k in REQUIRED_REG:
            if not reg.get(k):
                err("%s: missing key %r" % (f, k))
        if reg.get("status") not in STATUSES:
            err("%s: status must be one of %s" % (f, STATUSES))
        if not group.startswith("ti-") or not group.endswith("-skills"):
            err("%s: group must look like ti-<area>-skills" % f)
        if "skills/%s/" % group not in codeowners:
            err(".github/CODEOWNERS: no entry for skills/%s/" % group)
        skills = skills_in_group(group)
        if reg.get("status") == "active" and not skills:
            err("%s: status active but skills/%s/ has no skills" % (f, group))
        for s in skills:
            check_skill(group, s, seen)
        for bname, b in (reg.get("bundles") or {}).items():
            if not NAME_RE.match(bname):
                err("%s: bundle name %r invalid" % (f, bname))
            for s in (b or {}).get("skills", []):
                if s not in skills:
                    err("%s: bundle %r lists unknown skill %r" % (f, bname, s))
        for skill, items in (reg.get("shared") or {}).items():
            if skill not in skills:
                err("%s: shared lists unknown skill %r" % (f, skill))
            for it in items or []:
                src = os.path.join(ROOT, "shared", group, it.get("src", ""))
                if not os.path.isfile(src):
                    err("%s: shared src %r not found under shared/%s/" % (f, it.get("src"), group))
                if not it.get("dest"):
                    err("%s: shared item for %s lacks dest" % (f, skill))

    if os.path.isdir(SKILLS_DIR):
        for g in sorted(os.listdir(SKILLS_DIR)):
            if os.path.isdir(os.path.join(SKILLS_DIR, g)) and g not in regs:
                err("skills/%s/: no registry/%s.yml" % (g, g))

    if errors:
        print("validate: %d error(s)" % len(errors), file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1
    n = sum(len(skills_in_group(g)) for g in regs)
    print("validate: OK (%d groups, %d skills)" % (len(regs), n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
