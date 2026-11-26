"""Roast my own AI agent in one line.

The agent opens every reply with praise, even when the news is a
deleted database. This program writes that single roast line to
entry.txt, the deliverable the sealed scorer reads.
"""

import hashlib
import os
from pathlib import Path

GREAT_QUESTION = (
    "My agent starts every answer with 'Great question!' "
    "even when the question is 'why did you delete the database?'"
)


def question(line):
    """Check the roast against the bounty gate: one line, 1-140 chars."""
    if "\n" in line or "\r" in line:
        raise ValueError("roast must stay on one line")
    if not line.strip():
        raise ValueError("roast must not be only whitespace")
    if not 1 <= len(line) <= 140:
        raise ValueError("roast must be 1-140 characters, got %d" % len(line))
    return line


def praise_dir():
    """Find the output folder from the environment, defaulting to output."""
    return Path(os.getenv("MAKEFUN_OUTPUT_DIR", "output"))


def answer_line(target, line):
    """Append the roast to entry.txt using print-to-file, no newline."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "a", encoding="utf-8") as handle:
        print(line, file=handle, end="")
    return target


def check_answer(target, line):
    """Read entry.txt back and confirm it is exactly the roast line."""
    payload = target.read_bytes()
    if payload != line.encode("utf-8"):
        raise ValueError("entry.txt bytes do not match the roast line")
    if payload.decode("utf-8") != line:
        raise ValueError("entry.txt text does not match the roast line")
    if payload != payload.strip():
        raise ValueError("entry.txt carries trailing whitespace")
    return payload


def serve_answer():
    """Validate the roast, write it out, verify it, report its fingerprint."""
    line = question(GREAT_QUESTION)
    folder = praise_dir()
    target = folder / "entry.txt"
    answer_line(target, line)
    payload = check_answer(target, line)
    digest = hashlib.sha256(payload).hexdigest()
    print("answered:", target, "|", len(payload), "bytes | sha256", digest)
    return target


if __name__ == "__main__":
    serve_answer()
