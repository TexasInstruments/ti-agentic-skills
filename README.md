# ti-agentic-skills

Agent Skills for Texas Instruments products and software. Install them into a coding agent
(Claude Code, Codex, Cursor and others that support the [Agent Skills](https://agentskills.io)
format; the plugin marketplace manifest is Claude Code only for now) to run TI-specific workflows: SDK setup, builds, bring-up, debug and deployment.

One repository for all of TI. Each business unit owns a group folder under `skills/`.

| Group | Folder | Status |
|---|---|---|
| Linux SDK (Sitara MPU) | `skills/ti-linux-sdk-skills/` | active (18 skills) |
| MCU+ SDK | `skills/ti-mcu-plus-sdk-skills/` | planned |

The generated [catalog](docs/CATALOG.md) lists every skill.

## Install

Every skill is self-contained, so you can install one skill, one group, or a mix.

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
tools/install.sh --group ti-linux-sdk-skills            # whole group -> ./.claude/skills
tools/install.sh --skill ti-linux-<skill> --dest ~/.claude/skills
```

Claude Code plugin marketplace: the repo ships `.claude-plugin/marketplace.json` with one plugin
per group and one per bundle. Add it with `/plugin marketplace add TexasInstruments/ti-agentic-skills`,
then `/plugin install <group>@ti-agentic-skills`.

Verification status: `skills/<group>/<skill>` discovery and `--skill` selection with `npx skills`
were tested. The plugin marketplace route and wildcard selection are not yet tested.
See [docs/install.md](docs/install.md).

## Repository layout

```
skills/<group>/<skill>/SKILL.md   the skills (self-contained: scripts/, references/, assets/)
shared/<group>/                   sources of files vendored into several skills
registry/<group>.yml              group metadata, owners, bundles, shared-file map
mcp/<server>/                     MCP servers the skills call (Linux skills use mcp/processor-sdk-docs)
tools/                            validate, build, sync_shared, install
docs/                             spec, install, governance helpers
```

## Add a business unit or a skill

See [docs/add-a-business-unit.md](docs/add-a-business-unit.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

Skills execute with your agent's permissions. Read [docs/trust-and-safety.md](docs/trust-and-safety.md)
and review a skill before installing it. Report issues per [SECURITY.md](SECURITY.md).

## License

BSD-3-Clause. See [LICENSE](LICENSE).

TODO(legal): confirm the license choice and copyright wording with TI legal before the first public release.
TODO(admin): create the GitHub teams named in `.github/CODEOWNERS`.
