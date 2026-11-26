# Skill specification

Based on the open Agent Skills format (https://agentskills.io/specification).

## Folder

```
skills/<category>/<skill>/
  SKILL.md        required
  scripts/        optional, executable helpers
  references/     optional, detail loaded on demand
  assets/         optional, templates and static files
```

## SKILL.md frontmatter

| Key | Rule |
|---|---|
| `name` | required, equals the directory, lowercase letters, digits, hyphens, max 64, starts with the category prefix (`ti-<sdk>-`) |
| `description` | required, max 1024 chars; say what it does and when to use it |
| `license` | required, equals the category's `license` in its registry file (`BSD-3-Clause`) |
| `metadata` | optional string-to-string map |

Body: at most 500 lines. Put long material in `references/`.

## Self-contained rule

A skill folder must work when it is the only thing installed.

- Links and script paths stay inside the skill folder.
- Needed shared files are vendored (real copies, not symlinks) by `tools/sync_shared.py`
  from `shared/<category>/`, mapped in the category's registry file.
- Mention sibling skills only as soft suggestions with a fallback ("if `ti-linux-x` is installed, use it;
  otherwise ask the user for Y").
- Scripts locate their own folder with `$(dirname "${BASH_SOURCE[0]}")` and never assume the repo layout.

## Naming

Prefix with the category short name so names stay unique when installed into one flat agent directory:
`ti-<sdk>-<topic>`, for example `ti-linux-yocto-build` in `ti-linux-sdk-skills`.
