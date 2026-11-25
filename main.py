#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Write the entry line for 'One Line, No Deadline Met' to /output/entry.txt.

The competition asks for one single-line joke, 1 to 200 characters,
giving an excuse for missing a deadline. An AI judge compares entries
head to head, weighing first that the line really is a missed-deadline
excuse, then that it is funny with a turn, that it works as a single
line with its punch at the end, that it sounds like something a person
would actually say when cornered, and that the angle is fresh. The
gate checks that /output/entry.txt is UTF-8 text of 1 to 200
characters and not only white space.

The output path defaults to /output/entry.txt and can be redirected
with the ENTRY_OUTPUT_PATH environment variable (used only for local
verification runs, so the shared /output is never touched). The
program is deterministic: every run writes exactly the same bytes,
and it re-reads the file after writing to prove the bytes on disk
are the bytes intended.
"""

import os

DEFAULT_OUTPUT_PATH = "/output/entry.txt"
OUTPUT_ENV_VAR = "ENTRY_OUTPUT_PATH"
MAX_CHARS = 200

# The excuse, revised after the first run. The draft was a flat
# "I checked it too often and rewrote it" apology with no escalation
# and no sting. The final line turns that check into a spiral with a
# rising scale -- one typo, the whole page, an entire career in doubt
# -- and saves the punch for the last word: the deliverable came back
# three days late having grown into a memoir nobody commissioned. It
# is one sentence, spoken the way a cornered person actually confesses,
# and it avoids every stock excuse: no traffic, no dead alarm, no dog.
ENTRY_PARTS = (
    "Sorry it's late: it was done on time until I gave it one last "
    "read, fixed one typo, rewrote the page, questioned my entire "
    "career, and surfaced three days later holding a memoir.",
)


def build_entry() -> str:
    """Assemble the one-line excuse and hold it to the gate's rules."""
    text = "".join(ENTRY_PARTS)
    assert 1 <= len(text) <= MAX_CHARS, (
        f"entry must be 1..{MAX_CHARS} characters, got {len(text)}"
    )
    assert "\n" not in text and "\r" not in text, "entry must be a single line"
    assert text.strip(), "entry must not be only white space"
    return text


def write_entry(text: str, output_path: str) -> None:
    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    with open(output_path, "rb") as f:
        on_disk = f.read()
    assert on_disk == text.encode("utf-8"), "bytes on disk differ from entry"


def main() -> None:
    output_path = os.environ.get(OUTPUT_ENV_VAR, DEFAULT_OUTPUT_PATH)
    write_entry(build_entry(), output_path)


if __name__ == "__main__":
    main()
