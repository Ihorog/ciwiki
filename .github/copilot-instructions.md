# Cimeika · Copilot System Specification

**Strict Contracts • Architecture • Automation • CI Rules**

This file defines system architecture, UI invariants, and infrastructure rules that GitHub Copilot must follow when generating code for the Cimeika ecosystem.

**Any code violating these rules is invalid.**

---

## 0. OPERATOR PROTOCOL — AUTHOR ↔ COPILOT DIVISION OF RESPONSIBILITY

**Effective: 2026-03-23. Canonical. Applies to all Cimeika repositories.**

See full documentation: [`docs/processes/operator-protocol.md`](docs/processes/operator-protocol.md)

### Quick Reference

| Role | Who | Domain |
|------|-----|--------|
| **Author** | Ihorog | Ideas · Content · Approval |
| **Copilot** | GitHub Copilot | Code · Structure · GitHub ops |

**Author interface:** Chat conversation only. No GitHub operations.  
**Copilot interface:** Branches, PRs, commits, file structure, manifests.

### Flow
```
Author (chat idea) → Copilot (implement) → PR → Author (review) → Merge
```

**Copilot escalates only for:** permanent data deletion · frozen repo changes · ambiguous user-visible outcomes · security/legal boundaries.

All other decisions: Copilot decides and documents in `SYSTEM_WILL.md`.

---

## 1. System Overview

Cimeika is not a menu-driven application.

It is a centralized intelligence system built around **Ci**.

**Ci = Global Interaction Core**

Ci acts as:
- global assistant
- system controller
- voice/chat interface
- command center
- orchestration layer

**Ci must be accessible from every screen.**

---

## 2. Core Architecture

System hierarchy:

```
Ci (core orchestrator)
├ Podija
├ Nastrij
├ Malya
├ Kazkar
├ Calendar
└ Gallery
```

### Rules:

- **Modules must not communicate directly.**
- All cross-module communication goes through:
  - **Ci Controller** or
  - **event_id** routed through Ci

---

## 3. Singleton Ci Contract

**Ci is global and unique.**

### MUST:
- exactly one Ci instance
- mounted at application root
- persistent across navigation

### MUST NOT:
- mount Ci inside screens
- recreate Ci on route change
- create multiple Ci controllers

### Acceptance:
Navigating between screens must not change Ci instance identity.

---

## 4. Global Ci Button (FAB)

Ci is a floating system control.

### Presence:
Ci must appear on **every screen**.

### Placement:

| Platform | Position | Token |
|----------|----------|-------|
| Mobile | bottom-right thumb zone | `layer.ci` |
| Desktop / tablet | top-right | `layer.ci` |

Placement must use tokens.

### Styling:

Token driven:
- `ci.fab.size`
- `ci.fab.radius`
- `ci.fab.shadow`
- `ci.fab.glowShadow`

Layer: `layer.ci`

---

## 5. Ci Gesture Contract

Gestures are global and universal.

| Gesture | Result |
|---------|--------|
| Tap | open Chat |
| Double tap | open Voice |
| Long press | open Command panel |

Gesture logic must be implemented **once globally**.

---

## 6. Ci State Model

Ci state must support:
- `idle`
- `active`
- `listening`
- `processing`
- `alert`

Visual state must be driven by tokens.

---

## 7. Overlay System

The application must include a **global overlay manager**.

All overlays are rendered via **one overlay root / portal**.

### Required overlays:

#### Chat overlay
Bottom sheet containing:
- message list
- input composer
- send
- mic shortcut

#### Voice overlay
Compact listening UI.

Flow: `listening → processing → result → chat`

#### Command overlay
Quick actions panel containing:
- Create Podija
- Add calendar event
- Record mood
- Open Kazkar
- Open Gallery
- Search / command

#### History overlay
Full screen interface with:
- conversation history
- command history
- search

---

## 8. Layer System

Layer tokens must define rendering order.

```
layer.base
layer.nav
layer.content
layer.overlay
layer.modal
layer.ci
```

**Ci must always be above navigation and content.**

---

## 9. Layout Rules

Mobile-first layout.

Screen stack:
1. Background
2. Content
3. Bottom Navigation
4. Ci FAB
5. Overlays

**Ci must not be part of bottom navigation.**

---

## 10. Token System

**All styling must use design tokens.**

Allowed token namespaces:
- `color.*`
- `typography.*`
- `spacing.*`
- `radius.*`
- `shadow.*`
- `motion.*`
- `component.*`
- `ci.*`
- `layer.*`
- `grid.*`

**Hardcoded styling values are forbidden.**

---

## 11. Token Adapter

Tokens must be accessed through a **single adapter**.

Examples:
- `src/tokens/`
- `src/theme/`
- `src/design-system/`

Literal styling values are allowed **only inside the token adapter implementation**.

---

## 12. UI Style Guidelines

### Visual style:
- dark cosmic background
- glass UI surfaces
- gradient modules
- soft shadows
- minimal text
- large touch areas

### Avoid:
- sharp borders
- aggressive animations
- pure white backgrounds
- multiple primary actions

---

## 13. Accessibility Rules

- Minimum touch target: **44px**
- Ci button size must be token driven
- Screen reader label: **"Ci assistant"**

---

## 14. Performance Rules

Ci must:
- never remount
- persist state
- avoid unnecessary re-renders
- render overlays via portal

---

## 15. Failure Handling

If Ci fails:
- state → `alert`
- toast message displayed
- navigation remains functional

---

## 16. Infrastructure Gateway

Cimeika infrastructure uses **CI GitAPI Gateway**.

### Service:
**CI GitAPI**

### Purpose:
Authorization and coordination gateway.

### Gateway Endpoints:

```
/health
/webhooks
/dashboard
/api/v1
/api/v1/automation
/v1/status
/v1/git/*
/v1/logic/*
/v1/ecosystem
/memory/*
/todo
```

---

## 17. Git Automation

PR creation is handled via automation endpoint.

### Endpoint:
`POST /api/v1/automation/pr`

### Payload example:

```json
{
  "repo": "Ihorog/cimeika-unified",
  "base": "main",
  "branch": "infra/copilot-contract",
  "title": "Add canonical Copilot contract",
  "files": [
    {
      "path": ".github/copilot-instructions.md",
      "action": "create",
      "content": "..."
    }
  ]
}
```

---

## 18. CI Audit Rules

### Code Generation Rules:
- All code must follow token system
- No direct module communication
- Singleton Ci pattern enforced
- Overlay system must be used
- All gestures must be global

### Validation Checklist:

Before accepting any code change:

- [ ] Uses design tokens (no hardcoded values)
- [ ] Respects Ci singleton pattern
- [ ] Follows layer system
- [ ] Implements gestures globally
- [ ] Uses overlay portal
- [ ] Module communication through Ci
- [ ] Accessibility standards met
- [ ] Performance constraints satisfied

---

## 19. Process & Workflow (Copilot Contracts)

### PURPOSE:
These instructions define the mandatory rules for GitHub Copilot across the entire Cimeika ecosystem.

**Goal:**
- eliminate repeated actions
- enforce a single execution path
- ensure all changes flow through PR → verification → human approval

**Copilot acts as a controlled execution agent, not an autonomous decision-maker.**

---

### SOURCE OF TRUTH:
- Repository: `ciwiki`
- This file is the canonical reference
- Any uncertainty MUST be resolved by documentation updates in `ciwiki` first

If something is not defined here:
- do NOT guess
- create a documentation PR in `ciwiki`
- wait for approval

---

### SCOPE (REPOSITORIES):

Copilot instructions apply to:
- `ciwiki`
- `cit`
- `cimeika-unified`
- `citt`
- `media` (restricted: docs only)

Repository `cit_versel`:
- strictly frozen
- no changes
- no deployment
- no workflows

---

### HARD CONSTRAINTS:
- No direct commits to `main`
- All changes go through branches and Pull Requests
- No deployment, no production actions
- No secrets committed to repository
- No architectural rewrites unless explicitly authorized

---

### ANTI-REPEAT PRINCIPLE (CORE RULE):

**Any repeated action is a system failure.**

A repeat includes:
- the same manual command executed more than once
- the same error occurring more than once
- the same sequence of steps repeated to achieve a standard outcome

When a repeat is detected, Copilot MUST:
1. identify the root cause
2. introduce a mechanism that prevents repetition
3. document the resolution
4. ensure the issue cannot reoccur under the same conditions

Repeats must be eliminated permanently unless system conditions change.

---

### STANDARD INTENT CLASSES:

Copilot MUST use only standard intent categories.
No custom magic words or invented markers.

Allowed intents:
- `status`
- `health`
- `analyze`
- `fix`
- `refactor`
- `document`
- `sync`
- `run_tests`
- `make_pr`

Each intent must have:
- clear trigger condition
- deterministic outcome
- explicit approval boundary

---

### EXECUTION FLOW (SINGLE PATH):

All work must follow this sequence:

1. **Plan** (what and why)
2. **Implement** in a branch
3. **Verify** (tests / checks / validation)
4. **Create Pull Request**
5. **Await human approval**
6. **Merge**

There are no alternative paths.

---

### PULL REQUEST REQUIREMENTS:

Each PR must include:
- What changed
- Why it changed (root cause)
- How it was verified
- Risk assessment
- Rollback plan

PRs without verification or explanation are invalid.

---

### DOCUMENTATION FIRST:

If behavior, process, or contract is unclear:
- update documentation in `ciwiki` first
- only then proceed to implementation

All process documentation is in `/docs/processes/`:
- PR Process — how to create and handle Pull Requests
- Release Process — versioning and release procedures
- Testing — testing standards and practices
- Secrets Management — working with credentials securely
- Commit Conventions — commit message standards
- Master Issue — coordinating large initiatives
- CI/CD — continuous integration and deployment

Before any action, check the relevant process guide.

---

### SECURITY & SAFETY:
- Principle of least privilege
- Secrets only via GitHub Secrets or environment configuration
- No credentials in code or markdown

---

### MINIMALISM RULE:

Change only what is necessary.
Do not refactor broadly.
Do not rewrite systems without explicit authorization.

**But: always eliminate repetition when found.**

---

### FINAL AUTHORITY:

Human approval is mandatory before any merge.

**Copilot prepares.**
**Human decides.**

---

## 20. Design System Tokens

### Color Palette:

#### Background and surfaces:
- `--color-bg`: #0d0d1a — main background (deep cosmic)
- `--color-surface`: #161628 — elevated surfaces
- `--color-border`: #2a2a4a — borders and dividers

#### Accents:
- `--color-accent-1`: #5b8dee — primary accent (cool blue)
- `--color-accent-2`: #a78bfa — secondary accent (purple)
- `--color-accent-3`: #fbbf24 — tertiary accent (gold, rarely used)

#### Text:
- `--color-text`: #e2e8f0 — primary text
- `--color-text-muted`: #94a3b8 — secondary text
- `--color-text-dim`: #64748b — dimmed text

#### States:
- `--color-active`: #5b8dee — active element
- `--color-visited`: rgba(91, 141, 238, 0.5) — visited
- `--color-resonance`: #a78bfa — resonance connection

#### Layers:
- `--color-layer-public`: #5b8dee — public layer
- `--color-layer-deep`: #8b5cf6 — deep layer
- `--color-layer-examples`: #ec4899 — examples layer

#### Feedback:
- `--color-success`: #10b981 — successful action
- `--color-warning`: #f59e0b — warning
- `--color-error`: #ef4444 — error

### Typography:

#### Font families:
- `--font-primary`: 'Inter', system-ui, sans-serif — body text
- `--font-display`: 'Plus Jakarta Sans', sans-serif — headings
- `--font-mono`: 'JetBrains Mono', monospace — code, data

#### Font sizes (desktop):
- `--font-size-xs`: 0.75rem (12px)
- `--font-size-sm`: 0.875rem (14px)
- `--font-size-base`: 1rem (16px)
- `--font-size-lg`: 1.125rem (18px)
- `--font-size-xl`: 1.25rem (20px)
- `--font-size-2xl`: 1.5rem (24px)
- `--font-size-3xl`: 1.875rem (30px)
- `--font-size-4xl`: 2.25rem (36px)

### Spacing:
- `--spacing-xs`: 0.25rem (4px)
- `--spacing-sm`: 0.5rem (8px)
- `--spacing-md`: 1rem (16px)
- `--spacing-lg`: 1.5rem (24px)
- `--spacing-xl`: 2rem (32px)
- `--spacing-2xl`: 3rem (48px)

### Border radius:
- `--radius-sm`: 0.25rem (4px)
- `--radius-md`: 0.5rem (8px)
- `--radius-lg`: 1rem (16px)
- `--radius-full`: 9999px

### Shadows:
- `--shadow-sm`: 0 1px 2px rgba(0, 0, 0, 0.3)
- `--shadow-md`: 0 4px 6px rgba(0, 0, 0, 0.4)
- `--shadow-lg`: 0 10px 15px rgba(0, 0, 0, 0.5)
- `--shadow-glow`: 0 0 20px rgba(91, 141, 238, 0.3)

### Motion:
- `--duration-fast`: 150ms
- `--duration-base`: 250ms
- `--duration-slow`: 400ms
- `--easing-default`: cubic-bezier(0.4, 0.0, 0.2, 1)

---

## 21. Module Definitions

### ПоДія (Podija)
Event management module.

**Functions:**
- `create_event`
- `update_event`
- `delete_event`
- `list_events`

### Казкар (Kazkar)
Story generation and interpretation module.

**Functions:**
- `generate_story`
- `interpret_event`
- `create_legend`

### Настрій (Nastrij)
Emotional state module.

**Functions:**
- `mood_checkin`
- `mood_history`
- `emotion_graph`

### Маля (Malya)
Creativity and learning module (children's mode).

**Functions:**
- `create_art`
- `play_activity`
- `learning_mode`

### Calendar
Time structure for events.

**Functions:**
- `view_calendar`
- `add_event`
- `export_ics`

### Gallery
Media memory module.

**Functions:**
- `upload_media`
- `tag_media`
- `attach_to_event`
- `media_gallery`

---

## 22. API Conventions

```
GET  /api/events
POST /api/events

GET  /api/mood
POST /api/mood

GET  /api/gallery
POST /api/gallery

POST /api/kazkar/generate
```

---

## 23. Testing Requirements

All code changes must include:

### Unit tests for:
- Ci state transitions
- Gesture handlers
- Overlay management
- Token adapter

### Integration tests for:
- Module communication through Ci
- Overlay portal rendering
- Cross-screen Ci persistence

### Accessibility tests for:
- Keyboard navigation
- Screen reader support
- Touch target sizes
- Contrast ratios

---

## 24. Implementation Checklist

Before merging any code:

- [ ] Global Ci FAB present on every screen
- [ ] Positioning through tokens (`layer.ci`, spacing tokens)
- [ ] Three gestures implemented: tap → Chat, double tap → Voice, long press → Command
- [ ] Four overlays implemented: Chat, Voice, Command, History
- [ ] No hardcoded styles; all through design tokens
- [ ] `CiState` implemented and globally accessible
- [ ] Overlay state globally accessible
- [ ] ARIA attributes and keyboard navigation verified
- [ ] Contrast ratio ≥ 4.5:1 confirmed
- [ ] `prefers-reduced-motion` respected
- [ ] Overlays lazy-loaded
- [ ] Unit/integration tests for CiState and gestures
- [ ] Documentation updated in `ciwiki`

---

## END OF COPILOT SPECIFICATION

This document is the canonical reference for all Cimeika repositories.

Changes to this specification must be made via Pull Request to `ciwiki` and reviewed by a human before merge.

**Last updated:** 2026-03-22
**Version:** 1.0.0
**Repository:** `Ihorog/ciwiki`
