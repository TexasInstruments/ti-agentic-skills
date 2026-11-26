# Contributing

1. Fork or branch. Work inside your category folder: `skills/<category>/<skill>/`.
2. Start from `template/skill-template/SKILL.md`. Read [docs/skill-spec.md](docs/skill-spec.md).
3. Run before pushing:
   ```bash
   python3 tools/sync_shared.py && python3 tools/build.py && python3 tools/validate.py
   ```
4. Sign off every commit (Developer Certificate of Origin, https://developercertificate.org): `git commit -s`.
5. Open a PR. Repo-wide reviewers come from CODEOWNERS; component owners for the paths you touch are
   requested automatically (`.github/component-owners.yml`). Add yourself for the area you maintain.

Rules that CI enforces: name equals directory and carries the category prefix, description at most
1024 characters, SKILL.md at most 500 lines, no link or script path leaving the skill folder, no
duplicate names, vendored copies match `shared/`, generated files are current.

Test skills with a real agent against the real tool or hardware. Do not document commands you have
not run.
