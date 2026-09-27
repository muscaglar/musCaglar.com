#!/usr/bin/env python3
"""Checks the built site in ./public (or the folder given as the first argument).

It fails when
  - a page links to a page, picture, stylesheet or script on this site that does not exist;
  - a redirect (an old address kept alive through `aliases`) leads to a page that does not exist;
  - a link points to a part of a page (#anchor) that does not exist;
  - an original photograph or a file carrying camera or location data has been published;
  - a page is missing its title or description.

Only the Python standard library is used, so it runs anywhere:  python3 scripts/check-site.py
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlparse

SITE_HOSTS = {"muscaglar.com", "www.muscaglar.com"}


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.title = ""
        self.description = ""
        self.is_redirect = False
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "name" in a:
            self.ids.add(a["name"])
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            if a.get("name") == "description":
                self.description = a.get("content", "")
            if a.get("http-equiv", "").lower() == "refresh":
                self.is_redirect = True
        for key in ("href", "src", "poster"):
            if key in a and a[key]:
                # A <link rel=canonical> or an og: address is a statement, not a link to follow.
                if tag == "link" and a.get("rel") in ("canonical",):
                    continue
                self.links.append(a[key])
        for key in ("srcset", "imagesrcset"):
            if key in a:
                for part in a[key].split(","):
                    url = part.strip().split(" ")[0]
                    if url:
                        self.links.append(url)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def target_file(root: Path, page: Path, url: str) -> tuple[Path | None, str]:
    """Returns the file a link on `page` points to (None when it leaves the site) and its #anchor."""
    url, anchor = urldefrag(url)
    parsed = urlparse(url)
    if parsed.scheme in ("mailto", "tel", "data", "javascript", "sms"):
        return None, ""
    if parsed.scheme in ("http", "https") or url.startswith("//"):
        if parsed.netloc not in SITE_HOSTS:
            return None, ""
        path = parsed.path or "/"
    else:
        path = parsed.path
    path = unquote(path)
    if path == "":
        return page, anchor
    base = root if path.startswith("/") else page.parent
    candidate = (base / path.lstrip("/")).resolve()
    if path.endswith("/") or candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate, anchor


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    if not root.is_dir():
        print(f"{root} does not exist — build the site first (hugo build).")
        return 2

    pages: dict[Path, Page] = {}
    for file in sorted(root.rglob("*.html")):
        parser = Page()
        parser.feed(file.read_text(encoding="utf-8", errors="replace"))
        pages[file.resolve()] = parser

    problems: list[str] = []

    for file, page in pages.items():
        shown = "/" + str(file.relative_to(root))
        if page.is_redirect:
            continue
        if not page.title.strip():
            problems.append(f"{shown}: no <title>")
        if file.name != "404.html" and not page.description.strip():
            problems.append(f"{shown}: no description")
        for link in page.links:
            target, anchor = target_file(root, file, link)
            if target is None:
                continue
            if not target.is_relative_to(root):
                problems.append(f"{shown}: link leaves the site folder: {link}")
                continue
            if not target.exists():
                problems.append(f"{shown}: broken link {link}")
                continue
            if anchor and target.suffix == ".html":
                other = pages.get(target.resolve())
                if other is not None and unquote(anchor) not in other.ids:
                    problems.append(f"{shown}: {link} points to a part of the page that does not exist")

    # The list of redirects for Cloudflare: every destination on this site must exist.
    redirects = root / "_redirects"
    count = 0
    if redirects.exists():
        for number, line in enumerate(redirects.read_text(encoding="utf-8").splitlines(), start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 2 or (len(parts) > 2 and parts[2] not in ("301", "302", "303", "307", "308")):
                problems.append(f"/_redirects line {number}: cannot be read: {line}")
                continue
            count += 1
            if ":splat" in parts[1] or ":" in parts[1].replace("://", ""):
                continue
            target, _ = target_file(root, root / "index.html", parts[1])
            if target is not None and not target.exists():
                problems.append(f"/_redirects line {number}: {parts[0]} leads to {parts[1]}, which does not exist")

    # Redirect pages must lead somewhere that exists.
    for file, page in pages.items():
        if not page.is_redirect:
            continue
        text = file.read_text(encoding="utf-8", errors="replace")
        match = re.search(r'url=([^"\'>\s]+)', text, flags=re.I)
        if not match:
            continue
        target, _ = target_file(root, file, match.group(1))
        if target is not None and not target.exists():
            problems.append(f"/{file.relative_to(root)}: redirects to a page that does not exist ({match.group(1)})")

    # Photographs: only resized copies may be published, and they must carry no camera or location data.
    markers = (b"Exif\x00\x00", b"GPSLatitude", b"http://ns.adobe.com/xap/1.0/")
    for file in sorted(root.rglob("*")):
        if file.suffix.lower() not in (".jpg", ".jpeg", ".webp", ".avif", ".png", ".heic", ".tif", ".tiff"):
            continue
        shown = "/" + str(file.relative_to(root))
        under_photos = shown.startswith("/photos/")
        if under_photos and "_hu_" not in file.name:
            problems.append(f"{shown}: an original photograph has been published")
        head = file.read_bytes()[: 256 * 1024]
        if any(m in head for m in markers):
            problems.append(f"{shown}: the file carries camera or location data")

    if problems:
        print(f"{len(problems)} problem(s) found in {root}:")
        for p in problems:
            print("  - " + p)
        return 1

    real = sum(1 for p in pages.values() if not p.is_redirect)
    print(f"Checked {real} pages and {count + len(pages) - real} redirects in {root}: all good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
