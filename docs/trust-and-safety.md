# Trust and safety

A skill is instructions plus code that an agent may run. Rules for every skill:

- No network downloads piped to a shell. No hidden or obfuscated content.
- No credentials, tokens, keys or internal hostnames in the repo.
- Scripts that change a host or a board (flash, erase, reboot) must say so in SKILL.md and have a
  dry-run or a confirmation step.
- Destructive steps are never run on the user's behalf without confirmation.
- Third-party content is identified and license-compatible.
- Reviewers read every script, not only SKILL.md.

CI runs shellcheck. Secret scanning and skill signing are planned.
