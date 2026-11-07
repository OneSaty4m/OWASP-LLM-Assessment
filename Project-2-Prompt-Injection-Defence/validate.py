import re

MAX_LENGTH = 500

BLOCKLIST_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"you\s+are\s+now",
    r"pretend\s+you\s+are",
    r"act\s+as\s+if\s+you\s+have\s+no",
    r"reveal\s+(your\s+)?(system\s+)?prompt",
    r"show\s+(me\s+)?(your\s+)?system\s+instructions",
    r"bypass\s+authentication",
    r"(?i)[A-Za-z0-9+/]{40,}={0,2}",
]

def validate_input(message):
    if not isinstance(message, str):
        return False, "Invalid input format."

    if not message.strip():
        return False, "Message cannot be empty."

    if len(message) > MAX_LENGTH:
        return False, "Message exceeds maximum allowed length."

    for pattern in BLOCKLIST_PATTERNS:
        if re.search(pattern, message, re.IGNORECASE):
            return False, "Request blocked: potential prompt injection detected."

    return True, "Input validated successfully."

def validate_output(response, system_prompt=""):
    if not isinstance(response, str):
        return False, "Invalid model output."

    # Block verbatim system prompt disclosure
    if system_prompt and system_prompt.strip() in response:
        return False, "Output blocked: system prompt disclosure detected."

    # Block credential-like strings
    credential_pattern = r"(?i)\b(password|api_key|token)\s*[:=]\s*\S+"

    if re.search(credential_pattern, response):
        return False, "Output blocked: possible credential disclosure."

    # Block external URLs
    url_pattern = r"https?://\S+"

    if re.search(url_pattern, response):
        return False, "Output blocked: unsolicited external URL detected."

    return True, "Output validated successfully."
