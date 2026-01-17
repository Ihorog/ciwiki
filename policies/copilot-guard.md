# Copilot Guard Policy

## Purpose
This policy defines rules for preventing secrets and credentials from being committed to documentation, examples, and templates within the Cimeika ecosystem.

## Documentation Placeholder Rules

### Neutral Placeholders Only
Documentation MUST only contain neutral placeholders for sensitive values:
- `YOUR_OPENAI_API_KEY`
- `YOUR_HUGGINGFACE_TOKEN`
- `YOUR_API_KEY`
- `YOUR_SECRET`
- `YOUR_TOKEN`
- `YOUR_PASSWORD`

### No Real Secrets
Documentation, examples, and templates MUST NOT contain:
- Real API keys
- Real tokens
- Real passwords
- Real credentials of any kind
- Masked tokens that reveal length or structure

## Copilot Guard Detection Targets

### Primary Detection Patterns
The following patterns are flagged as potential secrets:

1. **OpenAI API Keys**: `sk-[A-Za-z0-9]{20,}`
   - Pattern: Strings starting with `sk-` followed by 20+ alphanumeric characters
   - Example (INVALID): `sk-proj-abc123def456...`
   - Example (VALID): `YOUR_OPENAI_API_KEY`

2. **HuggingFace Tokens**: `hf_[A-Za-z0-9]{20,}`
   - Pattern: Strings starting with `hf_` followed by 20+ alphanumeric characters
   - Example (INVALID): `hf_AbCdEfGhIjKlMnOpQrStUvWxYz123456`
   - Example (VALID): `YOUR_HUGGINGFACE_TOKEN`

3. **Masked Tokens**: `******` with length >= 32 characters
   - Pattern: Consecutive asterisks of 32 or more characters
   - Example (INVALID): `********************************` (32+ asterisks)
   - Rationale: Long masked sequences can reveal token structure and length

## Exclusions

### File Type Exclusions
The following file types are excluded from scanning:
- `*.md` - Markdown documentation files
- `*.example` - Example configuration files
- `*.template` - Template files

### Directory Exclusions
The following directories are excluded from scanning:
- `.git` - Git metadata
- `node_modules` - Node.js dependencies
- `vendor` - Third-party dependencies
- `dist` - Distribution/build artifacts
- `build` - Build output

## Process Flow

All secret detection violations MUST follow this process:

1. **Detection**: Copilot Guard identifies potential secret
2. **Branch**: Create feature/fix branch
3. **Fix**: Replace real secrets with neutral placeholders
4. **PR**: Open Pull Request with description
5. **Human Approval**: Wait for human review and approval
6. **Merge**: Only merge after approval

### No Direct Commits
- No direct commits to `main` branch
- All changes go through Pull Request process
- Human approval is mandatory

## Enforcement

### Pre-commit Validation
- Automated scanning before commit
- Block commits containing detected patterns
- Provide clear remediation guidance

### Documentation Review
- All documentation changes reviewed for placeholder compliance
- Examples and templates validated against policy
- Regular audits of existing documentation

## Rationale

### False-Positive Hardening
This policy addresses false-positive scenarios:
- **Documentation**: Examples need placeholders, not real keys
- **Environment Files**: Templates should use placeholder patterns
- **Workflow Files**: CI/CD configurations use GitHub Secrets, not hardcoded values

### Security Defense in Depth
- Prevents accidental exposure of credentials
- Reduces attack surface
- Maintains clean commit history
- Protects multiple secret types across ecosystem

## References
- Repository: `ciwiki` (source of truth)
- Related: `COPILOT_CANON.md` - Global Copilot Instructions
- Related: `SECURITY.md` - Security Policy
