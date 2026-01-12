# Security Recommendations

This document provides security best practices and recommendations for contributing to and using CiWiki.

## For Contributors

### Code Security
- Always validate and sanitize user inputs
- Use prepared statements for database queries
- Never commit sensitive data (API keys, passwords, tokens)
- Keep dependencies up to date
- Follow the principle of least privilege

### Development Practices
- Run `npm audit` before committing changes
- Review security warnings in IDE/editor
- Use environment variables for configuration
- Enable 2FA on your GitHub account
- Sign commits with GPG keys

## For Users

### Installation Security
- Only install from official sources
- Verify package integrity when possible
- Keep Node.js and npm up to date
- Review dependencies before installation

### Runtime Security
- Use strong passwords and secure authentication
- Keep the application and all dependencies updated
- Monitor security advisories
- Report security issues responsibly (see [SECURITY.md](../SECURITY.md))

## Automated Security Measures

This project uses:
- **Dependabot**: Automated dependency updates
- **CodeQL**: Static code analysis for security vulnerabilities
- **npm audit**: Regular vulnerability scanning

---

**Last Updated**: 2026-01-12
