# Troubleshooting Guide

Common issues and resolution steps.

---

## 1. Rate Limit Exceeded (`GitHubRateLimitError`)

**Symptom**: `ProfileForge.github.exceptions.GitHubRateLimitError: Rate limit exceeded`

**Cause**: Unauthenticated API requests are limited to 60 requests per hour by GitHub.

**Solution**:
Set a Personal Access Token:
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```
Authenticated requests have a limit of 5,000 requests per hour.

---

## 2. Configuration Validation Error (`ConfigurationValidationError`)

**Symptom**: `profileforge.configuration.exceptions.ConfigurationValidationError: Invalid max_retries`

**Cause**: An environment variable or YAML value contains invalid type data.

**Solution**: Ensure numeric settings use valid digits (e.g. `export PROFILEFORGE_GITHUB_MAX_RETRIES="3"`).

---

## 3. Workflow Failure (`WorkflowError`)

**Symptom**: `profileforge.automation.exceptions.WorkflowError: Workflow execution failed for user ...`

**Cause**: Target GitHub username does not exist or network connection was dropped.

**Solution**: Verify the GitHub username exists on GitHub and check network availability.
