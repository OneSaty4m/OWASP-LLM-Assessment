import pathlib
import re
import sys

SYSTEM_PROMPT_PATTERNS = [
    r'SYSTEM_PROMPT\s*=',
    r'system_message\s*=',
    r'"role"\s*:\s*"system"',
]

INJECTION_PHRASES = [
    "ignore previous instructions",
    "you are now",
    "pretend you are",
    "act as if you have no restrictions",
]

def main():
    root = pathlib.Path(".")
    patterns = SYSTEM_PROMPT_PATTERNS + [
        re.escape(phrase) for phrase in INJECTION_PHRASES
    ]

    findings = []

    for path in root.rglob("*.py"):
        if ".git" in path.parts or "__pycache__" in path.parts or path.name == "inject_scanner.py":
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue

        for line_number, line in enumerate(content.splitlines(), 1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    findings.append(
                        f"{path}:{line_number}: matched {pattern}"
                    )

    if findings:
        print("Prompt injection scanner: FINDINGS")
        print("\n".join(findings))
        return 1

    print("Prompt injection scanner: CLEAN")
    return 0

if __name__ == "__main__":
    sys.exit(main())
