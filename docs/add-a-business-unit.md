# Add a business unit or product group

Example: Zephyr.

2. Copy `registry/_template.yml` to `registry/ti-zephyr-skills.yml`; set `group`, `owners`, `status: planned`.
3. Add your paths and GitHub usernames to `.github/component-owners.yml`, for example
   `skills/ti-zephyr-skills:` with a list of usernames (no `@`). Owners are requested as reviewers on PRs
   touching those paths. Repo-wide default reviewers stay in `.github/CODEOWNERS`.
4. Create `skills/ti-zephyr-skills/<ti-zephyr-first-skill>/SKILL.md` from `template/skill-template/`.
5. Set `status: active`, run `python3 tools/build.py && python3 tools/validate.py`, open a PR.
6. Optional bundles: add them under `bundles:` in your registry file; the build generates a plugin per bundle.
7. Release with tag `ti-zephyr-skills/v0.1.0`.

Your group's code never needs edits to other groups' files.
