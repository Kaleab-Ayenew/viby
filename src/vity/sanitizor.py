# src/vity/sanitizer.py

import re
import sys

# Pre-compiled regex for efficiency.

# 1. A comprehensive regex to find and remove ANSI escape sequences.
# This covers color codes, including cursor movement, screen clearing, etc.
_ANSI_ESCAPE_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# 2. Regex to remove the "Script started/done" lines added by the `script` command.
# The re.MULTILINE flag allows `^` to match the start of each line.
_SCRIPT_ARTIFACT_RE = re.compile(r'^Script (started|done) on.*?\n', re.MULTILINE)

# 3. Regex to remove common control characters that are not human-readable or
# useful for context. This includes carriage return (\r), backspace (\x08),
# and other non-printable characters, while preserving newline (\n) and tab (\t).
_CONTROL_CHARS_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]|\r')

# 4. Regex to normalize whitespace by collapsing 3 or more newlines into just 2.
# This preserves intentional paragraph breaks while cleaning up excessive spacing.
_EXCESS_NEWLINES_RE = re.compile(r'\n{3,}')


def sanitize_raw_log(raw_log_content: str) -> str:
    """
    Performs universal, low-level sanitization on a raw terminal log string.
    """
    if not raw_log_content:
        return ""

    # Ensure we are working with a string
    sanitized_text = str(raw_log_content)

    # --- Apply cleaning steps in a logical order ---

    # Step 1: Remove `script` command artifacts first, as they are predictable lines.
    sanitized_text = _SCRIPT_ARTIFACT_RE.sub('', sanitized_text)

    # Step 2: Remove all ANSI escape codes.
    sanitized_text = _ANSI_ESCAPE_RE.sub('', sanitized_text)

    # Step 3: Remove other disruptive control characters like carriage returns.
    sanitized_text = _CONTROL_CHARS_RE.sub('', sanitized_text)

    # Step 4: Normalize newlines to make the text more readable and consistently formatted.
    sanitized_text = _EXCESS_NEWLINES_RE.sub('\n\n', sanitized_text)

    # Step 5: Remove any leading or trailing whitespace from the entire block.
    sanitized_text = sanitized_text.strip()

    return sanitized_text




def get_last_x_lines(raw_log_content: str, lines: int) -> str:
    log_lines = "\n".join(raw_log_content.split("\n")[:lines])
    return log_lines