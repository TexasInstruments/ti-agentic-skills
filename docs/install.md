# Installing skills

| Goal | Command |
|---|---|
| List everything | `npx skills add TexasInstruments/ti-agentic-skills --list` |
| One skill | `npx skills add TexasInstruments/ti-agentic-skills --skill <name> -a claude-code` |
| Selected skills | repeat `--skill` |
| Global instead of project | add `-g` |
| Offline, whole group | `tools/install.sh --group <group>` |
| Offline, one skill | `tools/install.sh --skill <name>` |

Skills are copied into the agent's skills directory (for Claude Code, `./.claude/skills/<name>`).

Tested: `skills/<group>/<skill>` discovery, `--list`, and `--skill` selection with the `skills` CLI.
Not yet tested: Claude Code plugin marketplace install of a group plugin, and wildcard `--skill` patterns.
Because every skill is self-contained, a partial install never breaks.
