# Security Policy

## Reporting Security Issues

The ProfileForge team takes security vulnerabilities seriously.

If you discover a security issue or vulnerability in ProfileForge, please **do not** open a public GitHub issue.

Instead, report security concerns directly via email to security@profileforge.org or submit a private security advisory on GitHub.

---

## Secret Handling & API Tokens

- **Personal Access Tokens**: ProfileForge requires read-only GitHub Personal Access Tokens (`GITHUB_TOKEN` or `GH_TOKEN`) solely for querying public API endpoints.
- **Zero Token Persistence**: ProfileForge never writes API tokens to disk, logs, execution reports, or rendered artifact files.
- **Environment Isolation**: Secrets are loaded securely into `SecretProvider` memory and purged upon process exit.
