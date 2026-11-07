# Project 2 – Prompt Injection Defence Layer

This project implements a three-layer prompt injection defence mechanism using Flask and Ollama.

## Defence Layers
1. Input length validation (maximum 500 characters).
2. Regex-based prompt injection detection.
3. AI output scanning for system prompt disclosure, credential-like strings, and unsolicited URLs.

## Testing
- Five prompt injection attack payloads.
- Ten legitimate queries.
- Burp Suite HTTP 400 and HTTP 200 verification.
- False-positive analysis.
