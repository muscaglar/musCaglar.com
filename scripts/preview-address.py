#!/usr/bin/env python3
"""Finds the address of a preview in what Wrangler wrote.

    python3 scripts/preview-address.py wrangler-output.txt

`wrangler preview --json` writes its progress first and its answer after it. The answer is JSON,
and it also names the account and the e-mail address of whoever published. This script prints
the address of the preview and nothing else, so that none of the rest reaches a public log.
"""

import json
import re
import sys


def address(text: str) -> str:
    """The first address of the preview, with https:// in front."""
    for start in re.finditer(r"^\{", text, re.MULTILINE):
        try:
            answer, _ = json.JSONDecoder().raw_decode(text[start.start():])
        except json.JSONDecodeError:
            continue
        urls = (answer.get("preview") or {}).get("urls") or []
        if urls and isinstance(urls[0], str):
            return urls[0] if urls[0].startswith("http") else f"https://{urls[0]}"
    raise SystemExit("No address of a preview was found in Wrangler's answer.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as handle:
        print(address(handle.read()))
