# Governance

- Repo maintainers (listed in `.github/CODEOWNERS`, initially `@jeevantelukula`) own structure, tooling, CI,
  the registry schema and releases of the repo itself.
- Component owners (listed in `.github/component-owners.yml`) are requested as reviewers on PRs that
  touch their paths: a group, a single skill, `shared/`, `registry/` or an MCP server.
- A new group is added by a PR that adds `registry/<group>.yml`, owners for its paths in `component-owners.yml`, and the group
  folder. Repo maintainers approve the structure; the BU owns the content.
- Releases are per group: tag `<group>/vX.Y.Z`. Breaking changes (renamed or removed skills) bump MAJOR.
- A group with no active maintainer for 6 months is marked `deprecated` in its registry.

## Contact

Conduct and governance concerns: open a private security advisory on this repository, or contact the repo maintainers team. TODO(admin): add a monitored shared mailbox here.
