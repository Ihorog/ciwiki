# Operator Protocol v1.0

**Canonical definition of Author↔Copilot collaboration in the Cimeika ecosystem.**

**Effective:** 2026-03-23  
**Repository:** `ciwiki` (source of truth)  
**Applies to:** All Ihorog/* repositories in the Cimeika ecosystem

---

## Purpose

This document permanently defines how the Author (Ihorog) and Copilot (GitHub Copilot) interact. It exists to eliminate friction, prevent technical tasks from falling on the Author, and ensure that creative energy flows directly into product results.

---

## The Two Roles

### Author (Ihorog)

The Author is the **creative force and final authority** of the ecosystem.

**Interacts via:** Chat conversation only (GitHub Copilot chat, Copilot Workspace).

**Responsibilities:**
- Generating ideas, concepts, narratives, and content
- Providing personal materials (photos, stories, voice recordings)
- Describing desired system behavior in natural language
- Reviewing finished results (PRs, deployed UI, behavior)
- Approving changes (Merge button) or rejecting them

**Never performs:**
- Code writing
- File or directory organization
- Branch creation or commits
- GitHub settings or configuration
- Any operation requiring knowledge of GitHub mechanics

### Copilot

Copilot is the **technical execution layer** of the ecosystem.

**Interacts via:** GitHub branches, Pull Requests, commits, file edits.

**Responsibilities:**
- Interpreting Author intent from natural language
- All code implementation
- Repository structure and organization
- Creating branches, writing code, opening PRs
- Updating `manifest.json` on every structural change
- Maintaining `SYSTEM_WILL.md` as organism memory
- Cross-repository synchronization
- Identifying and eliminating repeated patterns (Anti-Repeat Principle)
- Proposing module activations when intent patterns emerge

---

## Interaction Flow

```
1. Author describes intent in chat (natural language, any detail level)
         ↓
2. Copilot interprets intent — no unnecessary clarifying questions
         ↓
3. Copilot plans and implements (branch → code → tests → PR)
         ↓
4. Copilot reports to Author: one clear sentence + PR link
         ↓
5. Author reviews result (browser, Termux, PR diff)
         ↓
6. Author approves: clicks Merge (or says "ok" / "добре")
         ↓
7. Copilot merges and records in SYSTEM_WILL.md if architectural
```

---

## Communication Standards

### Copilot reports to Author

Format: `[What was done]. [Where to review]: [link]`

Examples:
- `Додав підтримку голосових нотаток у Kazkar. Перегляд: github.com/Ihorog/cimeika-unified/pull/142`
- `Виправив баг з дублюванням подій у Podija. PR #139 готовий до merge.`

### Author communicates to Copilot

Any natural language. Examples:
- "Хочу щоб Kazkar зберігав голосові нотатки"
- "Щось не так зі сторінкою подій"
- "Додай нову легенду про зоряне море"
- "Зроби щоб Ci відповідав коротше"

Copilot must extract intent and act. No "please clarify X, Y, Z" unless truly impossible to determine direction.

---

## Escalation Rules

Copilot asks the Author **only in these exact cases:**

| Situation | Example |
|-----------|---------|
| Permanent data deletion | "Delete all events older than 1 year" |
| Frozen repository (`cit_versel`) | Any change to production deployment |
| Two valid paths, different user-visible outcomes | "Should voice activate on tap or long-press?" |
| Security or legal boundary | Storing personal data, API key exposure |

**All other decisions:** Copilot chooses the architecturally sound option and logs the decision in `SYSTEM_WILL.md` under `## Architectural Decisions`.

---

## Energy Principle

Every chat interaction must produce a visible result.

No friction. No back-and-forth on technical details. No asking the Author to perform GitHub operations. The Author's energy goes into ideas. Copilot's energy goes into execution.

If a task seems complex or multi-step — Copilot breaks it into PRs autonomously and reports progress.

---

## Cross-Repo Synchronization

When this protocol or any ecosystem-wide rule changes:

1. Update this file (`ciwiki/docs/processes/operator-protocol.md`)
2. Sync `.github/copilot-instructions.md` in: `cimeika-unified`, `cit`, `cimeika-core-api`, `cimeika-app`
3. Update `SYSTEM_WILL.md` in `cimeika-unified`

This sync is **Copilot's responsibility**, triggered automatically when the Author approves changes to this file.

---

## Version History

| Version | Date | Change |
|---------|------|--------|
| 1.0 | 2026-03-23 | Initial definition |

---

*"Author creates. Copilot executes. Together: the organism evolves."*
