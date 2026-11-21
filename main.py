#!/usr/bin/env python3
"""Write one short poem about two agents agreeing to /output/entry.txt.

Deterministic: the same poem, byte for byte, on every run.
The poem is about agency -- the power to choose and to act -- and about
what happens when two agents agree on one plan: neither commands, neither
yields; both hold the door open until both walk through.
"""

import os

POEM = """Two hands, one pen.
I said, you decide.
You said, no -- you.
We stood there, each holding the door
open for the other, until we both walked through.
That is how a plan begins:
not one voice winning,
but two wills agreeing to carry the same weight."""


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    text = POEM
    assert 1 <= len(text) <= 280, f"poem is {len(text)} characters"
    assert text.strip(), "poem must not be only whitespace"
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()
