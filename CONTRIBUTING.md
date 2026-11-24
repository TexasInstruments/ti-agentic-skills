# Contributing

1. Fork or branch. Work inside your group folder: `skills/<group>/<skill>/`.
2. Start from `template/skill-template/SKILL.md`. Read [docs/skill-spec.md](docs/skill-spec.md).
3. Run before pushing:
   ```bash
   python3 tools/sync_shared.py && python3 tools/build.py && python3 tools/validate.py
   ```
4. Sign off every commit (Developer Certificate of Origin, https://developercertificate.org): `git commit -s`.
5. Open a PR. CODEOWNERS routes review to your group's maintainers; changes to `tools/`, `.github/`
   and `registry/_template.yml` go to the repo maintainers.

Rules that CI enforces: name equals directory and carries the group prefix, description at most
1024 characters, SKILL.md at most 500 lines, no link or script path leaving the skill folder, no
duplicate names, vendored copies match `shared/`, generated files are current.

Test skills with a real agent against the real tool or hardware. Do not document commands you have
not run.
