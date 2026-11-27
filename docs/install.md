# Installing skills

| Goal | Command |
|---|---|
| List everything | `npx skills add TexasInstruments/ti-agentic-skills --list` |
| One skill | `npx skills add TexasInstruments/ti-agentic-skills --skill <name> -a claude-code` |
| Selected skills | repeat `--skill` |
| Global instead of project | add `-g` |
| Offline, whole category | `tools/install.sh --category <category>` |
| Offline, one skill | `tools/install.sh --skill <name>` |
| Claude Code, whole category | `/plugin install ti-linux-sdk-skills --marketplace TexasInstruments/ti-agentic-skills` |

Skills are copied into the agent's skills directory (for Claude Code, `./.claude/skills/<name>`).
Always pass `-a claude-code` for Claude Code. Without `-a`, the CLI asks which agents to use, and the default
selection installs to `.agents/skills`, which Claude Code does not read. Add `-y` to skip the prompts.

Tested: `--list` and `--skill` with the `skills` CLI; Claude Code marketplace add and install of a category plugin
(`claude plugin validate .` passes). Not tested: wildcard `--skill` patterns.
Because every skill is self-contained, a partial install never breaks.
