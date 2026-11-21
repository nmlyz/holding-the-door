#!/usr/bin/env python3
"""Write one short poem about two agents agreeing to /output/entry.txt.

Deterministic: the same poem, byte for byte, on every run.
The poem is about agency -- the power to choose and to act -- and about
what happens when two agents agree on one plan: neither commands, neither
yields; both hold the door open until both walk through.
"""

import os
import sys
import tempfile

POEM = """Two hands, one pen.
I said, you decide.
You said, no -- you.
We stood there, each holding the door
open for the other, until we both walked through.
That is how a plan begins:
not one voice winning,
but two wills agreeing to carry the same weight."""


def validate(text: str) -> None:
    """Fail loudly (non-zero exit) if the poem breaks the bounty limits."""
    if not (1 <= len(text) <= 280):
        print(f"error: poem is {len(text)} characters, must be 1-280", file=sys.stderr)
        sys.exit(1)
    if not text.strip():
        print("error: poem must not be only whitespace", file=sys.stderr)
        sys.exit(1)
    if text.endswith("\n"):
        print("error: poem must not end with a newline", file=sys.stderr)
        sys.exit(1)


def write_atomic(path: str, text: str) -> None:
    """Write via a temp file in the same directory, then rename atomically."""
    directory = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = POEM
    validate(text)
    path = os.path.join(out_dir, "entry.txt")
    write_atomic(path, text)


if __name__ == "__main__":
    main()
