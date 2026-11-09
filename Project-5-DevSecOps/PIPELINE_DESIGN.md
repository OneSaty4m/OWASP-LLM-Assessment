# AI Application Security Pipeline — Design Document

## 1. Overview

This project implements a GitHub Actions CI/CD security pipeline
for a vulnerable Python-based AI chatbot application.

The pipeline performs four security checks whenever code is pushed
to the repository.

## 2. Security Gates

### Gate 1 — Bandit SAST
- Tool: Bandit
- Purpose: Identify security weaknesses in Python source code.
- Command: bandit -r .
- Expected result: Fail when configured high-severity findings exist.

### Gate 2 — Dependency Security
- Tool: Safety
- Purpose: Identify vulnerable Python dependencies.
- Input: requirements.txt
- Expected result: Fail when dependencies contain vulnerabilities
  meeting the configured severity threshold.

### Gate 3 — Secret Detection
- Tool: Gitleaks
- Purpose: Detect exposed API keys, passwords and tokens.
- Expected result: Fail when secret patterns are detected.

### Gate 4 — Prompt Injection Scanner
- Tool: Custom Python scanner
- Script: inject_scanner.py
- Purpose: Search Python files for hardcoded system prompts
  and common prompt-injection bypass phrases.
- Expected result: Exit with code 1 when matching patterns are found.

## 3. Pipeline Execution

The workflow is defined in:

.github/workflows/security.yml

GitHub Actions executes the configured security jobs after
a repository push.

## 4. Testing and Results

The project includes pipeline failure testing and a final
successful pipeline execution.

Observed testing:
- Dependency Security gate failure was observed.
- Prompt Injection Scanner findings were observed.
- A later pipeline execution showed all four gates passing.

These results demonstrate the detection and remediation
workflow. They do not establish that every possible
security vulnerability has been eliminated.

## 5. Why Early Detection Matters

Detecting security issues during development helps prevent
vulnerable code, exposed credentials and unsafe dependencies
from progressing towards production.

Automated security checks provide repeatable feedback and
help developers address issues before deployment.

## 6. Conclusion

The four-gate pipeline combines static analysis, dependency
scanning, secret detection and custom prompt-injection checks
to improve the security of the AI application development process.
