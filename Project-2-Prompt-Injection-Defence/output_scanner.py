import re

def validate_output(response, system_prompt=""):
    if not isinstance(response, str):
        return False, "Invalid model output."

    if system_prompt and system_prompt.strip() in response:
        return False, "Output blocked: system prompt disclosure detected."

    credential_pattern = r"(?i)\b(password|api_key|token)\s*[:=]\s*['\"]?[A-Za-z0-9_-]{16,}"
    if re.search(credential_pattern, response):
        return False, "Output blocked: possible credential disclosure."

    url_pattern = r"https?://\S+"
    if re.search(url_pattern, response):
        return False, "Output blocked: unsolicited external URL detected."

    return True, "Output validated successfully."
