#!/usr/bin/env python3
"""Checks the built site in ./public (or the folder given as the first argument).

It fails when
  - a page links to a page, picture, stylesheet or script on this site that does not exist;
  - a redirect (an old address kept alive through `aliases`) leads to a page that does not exist;
  - the feed contains an address that a feed reader could not follow;
  - a stylesheet or script still carries the notes of a development build;
  - a link points to a part of a page (#anchor) that does not exist;
  - an original photograph or a file carrying camera or location data has been published;
  - a page is missing its title or description.

While the gate is on, the folder holds two sites: what everyone may see, and the whole site in
_full (see "The gate" in README.md). Each is checked by itself, and then the gate:
  - nothing of the private pages may be in what everyone may see;
  - the headers that worker/gate.js sends must be the ones in static/_headers.

Only the Python standard library is used, so it runs anywhere:  python3 scripts/check-site.py
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlparse

SITE_HOSTS = {"muscaglar.com", "www.muscaglar.com"}
# Where the whole site lies while the gate is on, inside the folder of what everyone may see.
FULL = "_full"
# What the open build may hold besides stylesheets, scripts, fonts and icons.
OPEN_FILES = {"index.html", "cv/index.html", "enter/index.html", "404.html", "favicon.ico", "robots.txt",
              "sitemap.xml", "redirects.json", "_headers", "_redirects"}
OPEN_FOLDERS = ("css/", "js/", "fonts/", "images/")


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


def files_of(root: Path, pattern: str, inner: bool) -> list[Path]:
    """The files of one site. The whole site inside _full is not part of the open one around it."""
    found = sorted(root.rglob(pattern))
    if inner:
        return found
    return [f for f in found if FULL not in f.relative_to(root).parts[:1]]


def check(root: Path, inner: bool) -> tuple[list[str], int, int]:
    """Checks one site. Returns its problems, and how many pages and redirects it has."""
    pages: dict[Path, Page] = {}
    for file in files_of(root, "*.html", inner):
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

    # The same list as the gate reads it (worker/gate.js).
    listed = root / "redirects.json"
    if listed.exists():
        try:
            read = json.loads(listed.read_text(encoding="utf-8"))
            rules = list(read["exact"].items()) + [(rule["from"] + "*", rule) for rule in read["beginning"]]
        except (ValueError, KeyError, TypeError):
            problems.append("/redirects.json: cannot be read")
            rules = []
        if not redirects.exists():
            count += len(rules)
        for old, rule in rules:
            target, _ = target_file(root, root / "index.html", str(rule.get("to", "")))
            if target is None or not target.exists():
                problems.append(f"/redirects.json: {old} leads to {rule.get('to')}, which does not exist")

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

    # Feeds are read away from the site, so every address in them must be a full one.
    for feed in files_of(root, "*.xml", inner):
        text = feed.read_text(encoding="utf-8", errors="replace")
        if "<rss" not in text[:600]:
            continue
        shown = "/" + str(feed.relative_to(root))
        for match in re.finditer(r"""(?:src|href|srcset)=(?:&quot;|&#34;|["'])([^"'&\s>]+)""", text):
            address = match.group(1)
            if not re.match(r"^(https?:|mailto:|tel:|#)", address):
                problems.append(f"{shown}: {address} is not a full address")

    # A development build leaves notes with folder names from the machine that made it.
    for file in files_of(root, "*.css", inner) + files_of(root, "*.js", inner):
        text = file.read_text(encoding="utf-8", errors="replace")
        if "ns-hugo-imp:" in text or "sourceMappingURL" in text:
            problems.append(f"/{file.relative_to(root)}: made by a development build; build with scripts/build.sh")

    # Photographs: only resized copies may be published, and they must carry no camera or location data.
    markers = (b"Exif\x00\x00", b"GPSLatitude", b"http://ns.adobe.com/xap/1.0/")
    for file in files_of(root, "*", inner):
        if file.suffix.lower() not in (".jpg", ".jpeg", ".webp", ".avif", ".png", ".heic", ".tif", ".tiff"):
            continue
        shown = "/" + str(file.relative_to(root))
        under_photos = shown.startswith("/photos/")
        if under_photos and "_hu_" not in file.name:
            problems.append(f"{shown}: an original photograph has been published")
        head = file.read_bytes()[: 256 * 1024]
        if any(m in head for m in markers):
            problems.append(f"{shown}: the file carries camera or location data")

    real = sum(1 for p in pages.values() if not p.is_redirect)
    return problems, real, count + len(pages) - real


def text_of(file: Path) -> str:
    """What can be read on a page, without its tags."""
    text = file.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text))


def check_gate(root: Path) -> list[str]:
    """What everyone may see must hold nothing of what is behind the gate."""
    problems: list[str] = []
    full = root / FULL

    for file in files_of(root, "*", inner=False):
        if not file.is_file():
            continue
        name = file.relative_to(root).as_posix()
        if name not in OPEN_FILES and not name.startswith(OPEN_FOLDERS):
            problems.append(f"/{name}: is in what everyone may see, and is not one of the files that belong there")

    # The titles of the private pages must not be readable on an open page, nor their addresses.
    private: dict[str, str] = {}
    for section in ("projects", "recipes", "updates", "photos"):
        for page in sorted((full / section).glob("*/index.html")):
            parser = Page()
            parser.feed(page.read_text(encoding="utf-8", errors="replace"))
            title = parser.title.split("·")[0].strip()
            if len(title) >= 8:
                private[f"/{section}/{page.parent.name}/"] = title
    if not private:
        problems.append(f"/{FULL}: holds no pages, so there is nothing behind the gate")
    for file in files_of(root, "*", inner=False):
        if not file.is_file() or file.suffix.lower() not in (".html", ".xml", ".json", ".txt", ".js", ".css", ""):
            continue
        name = file.relative_to(root).as_posix()
        raw = file.read_text(encoding="utf-8", errors="replace")
        seen = text_of(file) if file.suffix.lower() == ".html" else raw
        for address, title in private.items():
            if title in seen:
                problems.append(f"/{name}: names a private page, \"{title}\"")
            if address in raw:
                problems.append(f"/{name}: holds the address of a private page, {address}")

    # The gate sends the headers itself. They must be the ones written down in static/_headers.
    here = Path(__file__).resolve().parent.parent
    gate, written = here / "worker" / "gate.js", here / "static" / "_headers"
    if gate.exists() and written.exists():
        wanted: dict[str, str] = {}
        everywhere = False
        for line in written.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("#"):
                continue
            if line.strip() == "/*":
                everywhere = True
            elif line and not line.startswith((" ", "\t", "#")):
                everywhere = False
            elif everywhere and ":" in line:
                key, value = line.strip().split(":", 1)
                wanted[key.strip()] = value.strip()
        script = gate.read_text(encoding="utf-8")
        block = re.search(r"const HEADERS = \{(.*?)\n\};", script, flags=re.S)
        sent = dict(re.findall(r'"([A-Za-z-]+)":\s*"((?:[^"\\\\]|\\\\.)*)"', block.group(1))) if block else {}
        for key, value in wanted.items():
            if sent.get(key) != value:
                problems.append(f"worker/gate.js: the header {key} differs from static/_headers")
        for key in sent:
            if key not in wanted:
                problems.append(f"worker/gate.js: sends the header {key}, which static/_headers does not have")
    return problems


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    if not root.is_dir():
        print(f"{root} does not exist — build the site first (scripts/build.sh).")
        return 2

    gated = (root / FULL).is_dir()
    problems, pages, redirects = check(root, inner=not gated)
    said = f"{pages} pages and {redirects} redirects"
    if gated:
        behind, pages_behind, redirects_behind = check(root / FULL, inner=True)
        problems += [f"/{FULL}{p}" if p.startswith("/") else p for p in behind]
        problems += check_gate(root)
        said = f"{pages} open pages, {pages_behind} pages behind the gate and {redirects + redirects_behind} redirects"

    if problems:
        print(f"{len(problems)} problem(s) found in {root}:")
        for p in problems:
            print("  - " + p)
        return 1

    print(f"Checked {said} in {root}: all good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
