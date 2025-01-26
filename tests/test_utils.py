import re


def normalize_ansi_whitespace(text: str) -> str:
    """Normalise whitespace in ANSI-coloured text while preserving colour codes."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    parts = []
    current = ''
    
    for part in ansi_escape.split(text):
        normalized = ' '.join(part.split())
        current += normalized
        ansi_match = ansi_escape.search(text, len(''.join(parts)) + len(current))
        if ansi_match:
            current += ansi_match.group()
        parts.append(current)
        current = ''
    
    return ''.join(parts)