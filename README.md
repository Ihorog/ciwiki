## System Node

| Field         | Description                                                                          |
|---------------|--------------------------------------------------------------------------------------|
| Node Role     | Documentation, rules, and the canonical source of truth for all Cimeika nodes.       |
| Inputs        | Change requests (PRs), documentation updates, API traces.                            |
| Outputs       | Canonical instructions, standard contracts/rules, procedural approvals.               |
| Dependencies  | All other nodes depend on ciwiki for system-wide rules and documentation.             |

## Copilot & Canon Reference

- Global rules: [ciwiki/.github/copilot-instructions.md](https://github.com/Ihorog/ciwiki/blob/main/.github/copilot-instructions.md)
- Canon updated: [ciwiki audit history](https://github.com/Ihorog/ciwiki/commits/main/.github/copilot-instructions.md)
- All functional changes must pass anti-repeat and intent review.

## Audit Log

_Last documentation update based on canon: 2026-01-17 — Copilot Stage 2 Optimization_.