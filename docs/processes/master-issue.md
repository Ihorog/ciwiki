# Master Issue Workflow

## Що таке Master Issue?

Master Issue — це центральний issue що координує велику ініціативу, feature або epic. Він служить як:

- 📋 Центр координації для пов'язаних задач
- 🗺️ Roadmap для feature delivery
- 📊 Tracking progress
- 📝 Документація рішень та контексту

## Коли створювати Master Issue?

Створюйте Master Issue для:

- ✅ Великих features (> 2 тижні розробки)
- ✅ Cross-team initiatives
- ✅ Архітектурних змін
- ✅ Multi-phase projects
- ✅ Coordinated releases

**НЕ створюйте** для:
- ❌ Маленьких bug fixes
- ❌ Одиночних задач
- ❌ Документації updates (якщо не масштабні)

## Структура Master Issue

### Template

```markdown
# [MASTER] Feature/Initiative Name

## 🎯 Objective

Brief description of what we're building and why.

**Value Proposition**: What business value does this deliver?

**Success Criteria**: How do we know when this is done?

## 📋 Context

### Background
- Why are we doing this now?
- What problem are we solving?
- Who are the stakeholders?

### Scope
**In Scope:**
- Item 1
- Item 2

**Out of Scope:**
- Item A (defer to v2)
- Item B (separate initiative)

### Dependencies
- [ ] Dependency 1 (#123)
- [ ] Dependency 2 (#456)

## 🗓️ Timeline

- **Start Date**: 2026-01-23
- **Target Completion**: 2026-02-15
- **Milestones**:
  - [ ] Phase 1: Foundation (Week 1-2)
  - [ ] Phase 2: Core Features (Week 3-4)
  - [ ] Phase 3: Polish & Release (Week 5)

## 📊 Tasks

### Phase 1: Foundation
- [ ] #101 Setup database schema
- [ ] #102 Create API endpoints
- [ ] #103 Add authentication

### Phase 2: Core Features
- [ ] #104 Implement feature A
- [ ] #105 Implement feature B
- [ ] #106 Add validation

### Phase 3: Polish & Release
- [ ] #107 Write documentation
- [ ] #108 Add tests
- [ ] #109 Performance optimization
- [ ] #110 Security audit

## 🔗 Related Issues

**Blocks:**
- #201 - Cannot start until this is done

**Blocked By:**
- #301 - Waiting on this

**Related:**
- #401 - Similar work

## 📝 Technical Design

### Architecture Overview
```
[Diagram or description]
```

### Key Decisions
1. **Decision**: Use PostgreSQL for storage
   - **Rationale**: Better support for complex queries
   - **Alternatives Considered**: MongoDB, MySQL

2. **Decision**: JWT for authentication
   - **Rationale**: Stateless, scalable
   - **Alternatives Considered**: Sessions

### API Design
```
POST /api/v1/resource
GET  /api/v1/resource/:id
PUT  /api/v1/resource/:id
DELETE /api/v1/resource/:id
```

## 🧪 Testing Strategy

- [ ] Unit tests (>80% coverage)
- [ ] Integration tests
- [ ] E2E tests for critical paths
- [ ] Performance tests
- [ ] Security tests

## 📖 Documentation

- [ ] API documentation
- [ ] User guide
- [ ] Migration guide (if breaking changes)
- [ ] Architecture decision records (ADRs)

## 🚦 Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| External API downtime | High | Low | Add fallback mechanism |
| Database migration issues | Medium | Medium | Test on staging first |
| Performance degradation | High | Low | Load testing before release |

## ✅ Acceptance Criteria

- [ ] All sub-tasks completed
- [ ] Tests passing (>80% coverage)
- [ ] Documentation complete
- [ ] Security review passed
- [ ] Performance benchmarks met
- [ ] Stakeholder approval

## 📈 Progress

**Status**: 🟡 In Progress

**Completion**: 35% (7/20 tasks)

**Last Updated**: 2026-01-23

### Recent Updates
- 2026-01-23: Completed Phase 1 foundation work
- 2026-01-20: Started implementation
- 2026-01-15: Design approved

## 👥 Team

- **Owner**: @username
- **Tech Lead**: @username
- **Contributors**: @user1, @user2, @user3
- **Reviewers**: @reviewer1, @reviewer2

## 📞 Communication

**Slack Channel**: #project-name

**Meetings**: 
- Daily standups: 10 AM
- Weekly sync: Fridays 2 PM

## 🔄 Change Log

### 2026-01-23
- Added new sub-task for error handling (#150)
- Updated timeline due to dependency delay

### 2026-01-20
- Initial master issue created
```

## Життєвий цикл Master Issue

### 1. Planning Phase

```
Status: 🔵 Planning
```

**Дії**:
- [ ] Створити Master Issue з template
- [ ] Визначити scope та objectives
- [ ] Identify dependencies
- [ ] Create high-level timeline
- [ ] Assign owner
- [ ] Get stakeholder approval

### 2. Design Phase

```
Status: 🟣 Design
```

**Дії**:
- [ ] Technical design document
- [ ] Architecture decisions
- [ ] API design
- [ ] Database schema
- [ ] Review and approval

### 3. Implementation Phase

```
Status: 🟡 In Progress
```

**Дії**:
- [ ] Create sub-issues для кожної задачі
- [ ] Assign tasks to developers
- [ ] Daily progress updates
- [ ] Regular sync meetings
- [ ] Risk monitoring

### 4. Testing Phase

```
Status: 🟠 Testing
```

**Дії**:
- [ ] All code merged
- [ ] Tests written and passing
- [ ] Integration testing
- [ ] Performance testing
- [ ] Security review

### 5. Documentation Phase

```
Status: 📝 Documentation
```

**Дії**:
- [ ] API documentation complete
- [ ] User guides written
- [ ] Migration guides (if needed)
- [ ] Update CHANGELOG

### 6. Release Phase

```
Status: 🚀 Ready for Release
```

**Дії**:
- [ ] Stakeholder approval
- [ ] Deployment plan
- [ ] Rollback plan
- [ ] Monitor after release

### 7. Completed

```
Status: ✅ Done
```

**Дії**:
- [ ] All acceptance criteria met
- [ ] Post-mortem meeting
- [ ] Document lessons learned
- [ ] Close Master Issue

## Progress Tracking

### Checklist Updates

Регулярно оновлюйте checklist в Master Issue:

```markdown
## 📊 Tasks (35% complete)

### Phase 1: Foundation (100% ✅)
- [x] #101 Setup database schema
- [x] #102 Create API endpoints
- [x] #103 Add authentication

### Phase 2: Core Features (20% 🟡)
- [x] #104 Implement feature A
- [ ] #105 Implement feature B
- [ ] #106 Add validation

### Phase 3: Polish & Release (0% ⏳)
- [ ] #107 Write documentation
- [ ] #108 Add tests
- [ ] #109 Performance optimization
```

### Status Comments

Додавайте status updates як коментарі:

```markdown
## Update 2026-01-23

**Progress**: Completed Phase 1 ✅

**Achievements**:
- ✅ Database schema finalized
- ✅ Basic API endpoints working
- ✅ Authentication implemented

**Next Steps**:
- ⏳ Start Phase 2 core features
- ⏳ Begin performance testing setup

**Blockers**:
- 🔴 Waiting on design approval for feature B (#105)

**Risks**:
- 🟡 Timeline may slip by 2 days due to dependency delay
```

## Sub-Issues Management

### Створення Sub-Issues

Для кожної задачі в Master Issue створіть окремий issue:

**Title Format**: `[MASTER#123] Descriptive task name`

**Example**: `[MASTER#100] Setup database schema for user profiles`

**Issue Body**:
```markdown
Part of Master Issue: #100

## Task Description
Setup PostgreSQL database schema for user profile storage.

## Acceptance Criteria
- [ ] Tables created with proper indexes
- [ ] Migration scripts written
- [ ] Schema documented

## Technical Notes
- Use UUID for primary keys
- Add created_at and updated_at timestamps
- Include soft delete functionality

## Estimated Time
4 hours
```

### Linking Sub-Issues

В Master Issue:
```markdown
### Phase 1: Foundation
- [ ] #101 Setup database schema
- [ ] #102 Create API endpoints
```

В Sub-Issue:
```markdown
Part of Master Issue: #100
Depends on: #101
Blocks: #103
```

## Labels для Master Issues

Обов'язкові labels:

- `master-issue` — ідентифікує як Master Issue
- `epic` — для великих ініціатив
- Priority: `priority:high`, `priority:medium`, `priority:low`
- Status: `status:planning`, `status:in-progress`, `status:blocked`, `status:done`
- Type: `type:feature`, `type:refactor`, `type:infrastructure`

Опціональні:

- `breaking-change` — якщо містить breaking changes
- `needs-review` — чекає на review
- `needs-approval` — чекає на stakeholder approval

## Communication Best Practices

### Status Updates

**Daily** (для active Master Issues):
- Короткий коментар в Master Issue
- Update checklist progress
- Highlight blockers

**Weekly**:
- Detailed progress report
- Risk assessment update
- Timeline adjustments (if needed)

### Team Sync

**Meetings**:
- Kick-off meeting (start of initiative)
- Weekly sync (during implementation)
- Review meeting (before phases)
- Post-mortem (after completion)

**Agenda Template**:
```
1. Progress Review (5 min)
   - What's done
   - What's in progress
   - What's blocked

2. Blockers & Risks (5 min)
   - Current blockers
   - Mitigation strategies

3. Next Steps (5 min)
   - Priorities for next period
   - Task assignments

4. Q&A (5 min)
```

## Decision Documentation

### Architecture Decision Records (ADR)

Для важливих технічних рішень:

```markdown
## ADR-001: Use PostgreSQL for User Data

**Status**: Accepted

**Context**:
We need to choose a database for storing user profiles and
activity data. Requirements include ACID compliance, complex
queries, and full-text search.

**Decision**:
Use PostgreSQL as primary database.

**Consequences**:
**Positive**:
- ACID compliance
- Excellent query performance
- Rich feature set
- Strong community support

**Negative**:
- Slightly more complex setup than NoSQL
- Requires schema migrations

**Alternatives Considered**:
1. MongoDB - Rejected: Need ACID guarantees
2. MySQL - Rejected: PostgreSQL has better features
```

## Metrics & Reporting

### Key Metrics

Track в Master Issue:

```markdown
## 📊 Metrics

**Development**:
- Tasks completed: 15/42 (36%)
- PRs merged: 12
- Code coverage: 85%

**Timeline**:
- Original estimate: 4 weeks
- Current projection: 4.5 weeks
- Variance: +0.5 weeks

**Quality**:
- Bugs found: 3
- Critical issues: 0
- Tech debt items: 2
```

### Velocity Tracking

```markdown
## 📈 Velocity

**Week 1**: 8 tasks completed
**Week 2**: 10 tasks completed
**Week 3**: 7 tasks completed (slower due to testing)
**Week 4**: Projected 9 tasks

**Average**: 8.5 tasks/week
```

## Anti-Patterns

### ❌ Don't Do This

1. **Too Broad Scope**
   - Master Issue що триває 6+ months
   - Краще розділити на кілька Master Issues

2. **No Updates**
   - Master Issue без updates тижнями
   - Team не знає status

3. **Missing Context**
   - Просто список tasks без пояснень
   - Нема "why" тільки "what"

4. **Orphan Sub-Issues**
   - Sub-issues не linked до Master Issue
   - Важко tracking dependencies

5. **Ignored Blockers**
   - Blockers не документовані або escalated
   - Приводить до delays

## Закриття Master Issue

### Pre-Close Checklist

- [ ] Всі sub-issues closed або переміщені
- [ ] Acceptance criteria met
- [ ] Documentation complete
- [ ] Code deployed
- [ ] Post-mortem conducted
- [ ] Lessons learned documented

### Closing Comment

```markdown
## ✅ Master Issue Completed

**Completion Date**: 2026-02-15

**Summary**:
Successfully delivered user profile management feature with
all planned functionality.

**Metrics**:
- Duration: 4.5 weeks (0.5 weeks over estimate)
- Tasks completed: 42/42
- Final code coverage: 87%
- Zero critical bugs

**Achievements**:
✅ All acceptance criteria met
✅ Performance targets exceeded
✅ Security review passed
✅ Documentation complete

**Lessons Learned**:
See post-mortem doc: [link]

**Next Steps**:
- Monitor production metrics for 1 week
- Address any feedback in follow-up issues
- Plan v2 features in separate Master Issue

Thanks to @user1, @user2, @user3 for great work! 🎉
```

## Templates & Automation

### GitHub Issue Templates

`.github/ISSUE_TEMPLATE/master-issue.md`:

```markdown
---
name: Master Issue
about: Track large initiatives or features
title: '[MASTER] '
labels: 'master-issue, epic'
assignees: ''
---

[Use the Master Issue template from docs/processes/master-issue.md]
```

### Automation Scripts

Auto-update progress:

```javascript
// Script to calculate completion %
const issues = await github.issues.listForRepo({
  owner,
  repo,
  labels: 'master-issue'
});

issues.forEach(issue => {
  const body = issue.body;
  const total = (body.match(/\[ \]/g) || []).length +
                (body.match(/\[x\]/g) || []).length;
  const completed = (body.match(/\[x\]/g) || []).length;
  const percent = Math.round((completed / total) * 100);
  
  console.log(`Issue #${issue.number}: ${percent}% complete`);
});
```

## Додаткові ресурси

- [PR Process](./pr-process.md)
- [Commit Conventions](./commit-conventions.md)
- [Project Management Best Practices](https://github.com/github/pm)

## Приклади

- [Example Master Issue](https://github.com/Ihorog/ciwiki/issues/1) (якщо існує)

## Питання?

Створіть issue з label "master-issue" для питань про process.
