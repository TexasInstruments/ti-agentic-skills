# Add an SDK category

A category holds the skills for one SDK or software stack. Linux SDK is the first one
(`ti-linux-sdk-skills`). Use the same steps for each new category; no other category's files change.

Naming: the category folder is `ti-<sdk>-skills`, every skill in it is `ti-<sdk>-<topic>`.
Example for an SDK called `foo`: folder `ti-foo-sdk-skills`, skills `ti-foo-build`, `ti-foo-flash`.

## Steps

1. Copy `registry/_template.yml` to `registry/ti-<sdk>-sdk-skills.yml`. Set `name`, `category`, `description`,
   `status: planned`.
2. Create `skills/ti-<sdk>-sdk-skills/ti-<sdk>-<topic>/SKILL.md` from `template/skill-template/SKILL.md`.
   Rules are in [skill-spec.md](skill-spec.md).
3. Files several skills need: put one copy in `shared/ti-<sdk>-sdk-skills/` and list it under `shared:` in
   the registry file. Run `python3 tools/sync_shared.py` to copy it into each skill.
4. Add yourself in `.github/component-owners.yml`, for example
   `skills/ti-<sdk>-sdk-skills:` with a list of GitHub usernames (no `@`). Owners are requested as reviewers on
   PRs that touch those paths. Repo-wide reviewers stay in `.github/CODEOWNERS`.
5. Set `status: active` in the registry file.
6. Run `python3 tools/sync_shared.py && python3 tools/build.py && python3 tools/validate.py`. Commit the
   generated `.claude-plugin/marketplace.json` and `docs/CATALOG.md` with your change.
7. Open a PR. Commits need a sign-off (`git commit -s`).
8. Release with tag `ti-<sdk>-sdk-skills/v0.1.0`.

## Rules that keep it scalable

- One category per SDK. Do not create categories for single skills or temporary subsets.
- Skills are self-contained and can be installed alone.
- Every category is one Claude plugin, generated from its folder. Do not hand-edit generated files.
- A category with no skills is not published.
- Releases are per category (`<category>/vX.Y.Z`). Renaming or removing a skill is a breaking change: bump MAJOR.
- A category with no active owner for 6 months is marked `status: deprecated` in its registry.
