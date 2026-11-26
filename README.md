# ti-agentic-skills

Agent Skills for Texas Instruments products and software. Install them into a coding agent to
run TI-specific workflows: SDK setup, builds, bring-up, debug and deployment.

Works with agents that support the [Agent Skills](https://agentskills.io) format (Claude Code,
Codex, Cursor and others). The plugin marketplace manifest is Claude Code only for now.

One repository for all TI SDKs. Each SDK has its own category folder under `skills/`.

| Category | Folder | Status |
|---|---|---|
| Linux SDK (Sitara MPU) | `skills/ti-linux-sdk-skills/` | active |

The generated [catalog](docs/CATALOG.md) lists every skill.

## Install

Every skill is self-contained, so you can install one skill, one category, or a mix.

```bash
# See what is available
npx skills add TexasInstruments/ti-agentic-skills --list

# One skill
npx skills add TexasInstruments/ti-agentic-skills --skill ti-linux-<skill> -a claude-code

# Several skills
npx skills add TexasInstruments/ti-agentic-skills --skill ti-linux-<a> --skill ti-linux-<b> -a claude-code
```

Offline, from a checkout:

```bash
tools/install.sh --list
tools/install.sh --category ti-linux-sdk-skills            # whole category -> ./.claude/skills
tools/install.sh --skill ti-linux-<skill> --dest ~/.claude/skills
```

Claude Code plugin marketplace: the repo ships `.claude-plugin/marketplace.json` with one plugin
per category.

```
/plugin marketplace add TexasInstruments/ti-agentic-skills
/plugin install ti-linux-sdk-skills --marketplace TexasInstruments/ti-agentic-skills
```

See [docs/install.md](docs/install.md) for all install routes.

## Repository layout

```
skills/<category>/<skill>/SKILL.md  the skills (self-contained: scripts/, references/, assets/)
shared/<category>/                  sources of files vendored into several skills
registry/<category>.yml             category metadata, status, shared-file map
mcp/<server>/                       MCP servers the skills call (Linux: mcp/processor-sdk-docs)
tools/                              validate, build, sync_shared, install
docs/                               skill spec, install guide, onboarding, trust rules, catalog
template/skill-template/            starting point for a new skill
```

## Add a skill or an SDK category

See [docs/add-an-sdk-category.md](docs/add-an-sdk-category.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

Skills execute with your agent's permissions. Read [docs/trust-and-safety.md](docs/trust-and-safety.md)
and review a skill before installing it. Report issues per [SECURITY.md](SECURITY.md).

## License

BSD-3-Clause. See [LICENSE](LICENSE).

TODO(legal): confirm the license choice and copyright wording with TI legal before the first public release.
Owners: repo-wide reviewers are in `.github/CODEOWNERS`; per-area owners go in `.github/component-owners.yml`.
