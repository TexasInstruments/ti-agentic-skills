# Instructions for agents working on this repo

- Skills live in `skills/<group>/<skill>/SKILL.md`. Read `docs/skill-spec.md` first.
- Never hand-edit generated files: `.claude-plugin/marketplace.json`, `docs/CATALOG.md`,
  and vendored copies listed under `shared:` in `registry/<group>.yml`.
- Edit shared sources under `shared/<group>/`, then run `python3 tools/sync_shared.py`.
- After any change run: `python3 tools/sync_shared.py && python3 tools/build.py && python3 tools/validate.py`.
- Every skill must be self-contained: no links or script paths that leave its folder, and no
  hard dependency on a sibling skill.
- Commits need a DCO sign-off: `git commit -s`.
