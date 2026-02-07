# Security Policy

## Supported Versions

The following versions of CiWiki are currently being supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in CiWiki or any Cimeika ecosystem repository, please report it by:

1. **DO NOT** open a public issue
2. Use GitHub's private security advisory feature:
   - Go to the repository
   - Click "Security" tab
   - Click "Report a vulnerability"
3. Or email the maintainers at: security@cimeika.example.com (якщо налаштовано)
4. Include detailed information about the vulnerability:
   - Description of the issue
   - Steps to reproduce
   - Potential impact
   - Affected versions
   - Suggested fix (if available)

### Response Timeline

- **Initial Response**: Within 48 hours of report submission
- **Status Updates**: Every 7 days until resolution
- **Resolution**: Security patches will be released as soon as possible after verification

### What to Expect

- **Accepted Vulnerabilities**: Will be patched in the next security release with credit given to the reporter (unless anonymity is requested)
- **Declined Reports**: Will receive an explanation of why the report was not accepted as a security issue

## Security Practices

### Secrets Management

**CRITICAL**: Never commit secrets to the repository.

- All secrets must be in environment variables or GitHub Secrets
- Use `.env` files locally (add to `.gitignore`)
- Follow [Secrets Management Guide](./docs/processes/secrets-management.md)

### Automated Security Scanning

All repositories have automated security scanning:

- **Dependabot** — dependency vulnerability scanning
- **CodeQL** — static code analysis
- **Secret Scanning** — detects leaked credentials
- **Copilot Guard** — prevents secrets in documentation

See [policies/copilot-guard.md](./docs/policies/copilot-guard.md) for details.

### Code Review Requirements

Security-related changes require:
- [ ] Review by security team member
- [ ] Security testing completed
- [ ] Documentation updated
- [ ] Approval from 2+ reviewers

## Security Vulnerabilities

### Classification

**Critical** 🔴
- Remote code execution
- Authentication bypass
- Data breach potential
- **Action**: Immediate patch and deployment

**High** 🟠
- Privilege escalation
- Sensitive data exposure
- SQL injection
- **Action**: Patch within 7 days

**Medium** 🟡
- XSS vulnerabilities
- CSRF issues
- Information disclosure
- **Action**: Patch within 30 days

**Low** 🟢
- Minor information disclosure
- Low-impact DoS
- **Action**: Patch in next release

### Disclosure Policy

**Coordinated Disclosure**:
1. Vulnerability reported privately
2. Fix developed and tested
3. Security advisory created
4. Patch released
5. Public disclosure after 90 days or patch availability

**CVE Assignment**: For significant vulnerabilities affecting multiple users

## Security Best Practices

### For Developers

1. **Input Validation** ✅
   - Validate all user inputs
   - Sanitize data before database queries
   - Use parameterized queries

2. **Authentication & Authorization** ✅
   - Use strong password policies
   - Implement MFA where possible
   - Follow principle of least privilege

3. **Cryptography** ✅
   - Use established libraries (no custom crypto)
   - Keep encryption keys secure
   - Use TLS/HTTPS for all connections

4. **Dependencies** ✅
   - Keep dependencies up to date
   - Review dependency security advisories
   - Use `npm audit` or equivalent regularly

5. **Logging & Monitoring** ✅
   - Log security events
   - Don't log sensitive data
   - Monitor for suspicious activity

### For Operations

1. **Infrastructure Security** ✅
   - Use firewalls and network segmentation
   - Enable encryption at rest and in transit
   - Regular security patches

2. **Access Control** ✅
   - Implement RBAC (Role-Based Access Control)
   - Regular access reviews
   - Revoke access promptly when needed

3. **Backup & Recovery** ✅
   - Regular automated backups
   - Test recovery procedures
   - Secure backup storage

## Security Checklist

### Before Deployment

- [ ] All dependencies updated and audited
- [ ] Security tests passing
- [ ] No secrets in code or configuration
- [ ] Authentication/authorization tested
- [ ] Input validation implemented
- [ ] HTTPS enabled
- [ ] Security headers configured
- [ ] Monitoring and logging enabled

### After Deployment

- [ ] Monitor logs for anomalies
- [ ] Verify security configurations
- [ ] Test incident response procedures
- [ ] Review access controls

## Incident Response

### If Security Breach Detected

1. **Immediate** (Hour 0)
   - Contain the breach
   - Preserve evidence
   - Notify security team

2. **Short-term** (Hours 1-24)
   - Assess impact
   - Identify root cause
   - Begin remediation
   - Notify stakeholders

3. **Long-term** (Days 1-30)
   - Complete remediation
   - Update security measures
   - Post-mortem analysis
   - Update documentation

### Contact Information

**Security Team**: #security-incidents (Slack)  
**Emergency Contact**: security-emergency@example.com  
**PGP Key**: [Link to public key if available]

## Compliance

### Standards

Cimeika ecosystem follows:
- OWASP Top 10 guidelines
- GitHub Security Best Practices
- Industry-standard security practices

### Regular Audits

- **Code security reviews**: Quarterly
- **Dependency audits**: Monthly  
- **Infrastructure reviews**: Quarterly
- **Penetration testing**: Annually

## Security Training

All team members must complete:
- Security awareness training (onboarding)
- Annual security refresher
- Secure coding practices workshop

## Updates to This Policy

This security policy is reviewed and updated:
- Quarterly by security team
- After major security incidents
- When new threats emerge

**Last Updated**: 2026-01-23  
**Next Review**: 2026-04-23

## Additional Resources

- [Secrets Management Guide](./docs/processes/secrets-management.md)
- [Copilot Guard Policy](./docs/policies/copilot-guard.md)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)

---

**Remember**: Security is everyone's responsibility. If you see something, say something.
