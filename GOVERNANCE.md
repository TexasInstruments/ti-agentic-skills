# Governance

- Repo maintainers (`@TexasInstruments/ti-agentic-skills-maintainers`) own structure, tooling, CI,
  the registry schema and releases of the repo itself.
- Group maintainers (`@TexasInstruments/<group>-maintainers`) own everything under their group's
  `skills/`, `shared/`, `registry/` file and any MCP server mapped to them in CODEOWNERS.
- A new group is added by a PR that adds `registry/<group>.yml`, a CODEOWNERS block and the group
  folder. Repo maintainers approve the structure; the BU owns the content.
- Releases are per group: tag `<group>/vX.Y.Z`. Breaking changes (renamed or removed skills) bump MAJOR.
- A group with no active maintainer for 6 months is marked `deprecated` in its registry.
