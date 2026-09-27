#!/usr/bin/env python3
"""Serves the built site (./public) roughly the way Cloudflare does.

`hugo server` is the everyday preview. This one is for checking what `hugo server` leaves out:
the headers in `_headers` (including the content security policy), the redirects in `_redirects`,
and the not-found page. It is a stand-in, not Cloudflare itself.

    hugo build --gc --minify
    python3 scripts/preview-built.py            # http://127.0.0.1:8788
    python3 scripts/preview-built.py public 9000

Only the Python standard library is used.
"""

from __future__ import annotations

import mimetypes
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8788

mimetypes.add_type("image/avif", ".avif")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("application/rss+xml", ".xml")
mimetypes.add_type("text/javascript", ".js")


def pattern(rule: str) -> re.Pattern[str]:
    """Turns a Cloudflare path rule (with * and :name) into a regular expression."""
    out = ""
    for part in re.split(r"(\*|:[A-Za-z]\w*)", rule):
        if part == "*":
            out += "(?P<splat>.*)"
        elif part.startswith(":") and len(part) > 1:
            out += f"(?P<{part[1:]}>[^/.]+)"
        else:
            out += re.escape(part)
    return re.compile("^" + out + "$")


def read_headers() -> list[tuple[re.Pattern[str], list[tuple[str, str]]]]:
    rules: list[tuple[re.Pattern[str], list[tuple[str, str]]]] = []
    file = ROOT / "_headers"
    if not file.exists():
        return rules
    current: list[tuple[str, str]] | None = None
    for line in file.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if not line[0].isspace():
            current = []
            rules.append((pattern(line.strip()), current))
        elif current is not None and ":" in line:
            name, value = line.strip().split(":", 1)
            current.append((name.strip(), value.strip()))
    return rules


def read_redirects() -> list[tuple[re.Pattern[str], str, int]]:
    rules: list[tuple[re.Pattern[str], str, int]] = []
    file = ROOT / "_redirects"
    if not file.exists():
        return rules
    for line in file.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) < 2 or parts[0].startswith("#"):
            continue
        rules.append((pattern(parts[0]), parts[1], int(parts[2]) if len(parts) > 2 else 302))
    return rules


HEADERS = read_headers()
REDIRECTS = read_redirects()


class Handler(BaseHTTPRequestHandler):
    server_version = "preview-built"

    def do_HEAD(self) -> None:  # noqa: N802
        self.respond(body=False)

    def do_GET(self) -> None:  # noqa: N802
        self.respond(body=True)

    def respond(self, body: bool) -> None:
        path = unquote(urlsplit(self.path).path)

        for rule, to, status in REDIRECTS:
            match = rule.match(path)
            if match:
                for name, value in match.groupdict().items():
                    to = to.replace(f":{name}", value or "")
                return self.redirect(to, status)

        file = (ROOT / path.lstrip("/")).resolve()
        if not str(file).startswith(str(ROOT)):
            return self.not_found(body)
        if file.is_dir():
            if not path.endswith("/"):
                return self.redirect(path + "/", 307)
            file = file / "index.html"
        elif not file.exists() and (ROOT / (path.strip("/") + "/index.html")).exists():
            return self.redirect(path + "/", 307)
        if path.endswith("/index.html"):
            return self.redirect(path[: -len("index.html")], 307)
        if not file.is_file() or file.name in ("_headers", "_redirects"):
            return self.not_found(body)
        self.send_file(file, 200, path, body)

    def redirect(self, to: str, status: int) -> None:
        self.send_response(status)
        self.send_header("Location", to)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def not_found(self, body: bool) -> None:
        page = ROOT / "404.html"
        if page.exists():
            return self.send_file(page, 404, "/404.html", body)
        self.send_response(404)
        self.end_headers()

    def send_file(self, file: Path, status: int, path: str, body: bool) -> None:
        data = file.read_bytes()
        kind = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
        if kind.startswith("text/") or kind.endswith(("xml", "json", "javascript")):
            kind += "; charset=utf-8"
        headers = {"Content-Type": kind, "Cache-Control": "public, max-age=0, must-revalidate"}
        for rule, pairs in HEADERS:
            if rule.match(path):
                for name, value in pairs:
                    headers[name] = value
        self.send_response(status)
        for name, value in headers.items():
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if body:
            self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        sys.stderr.write("%s %s\n" % (self.address_string(), format % args))


if __name__ == "__main__":
    if not ROOT.is_dir():
        sys.exit(f"{ROOT} does not exist — build the site first (hugo build).")
    print(f"Serving {ROOT} at http://127.0.0.1:{PORT} ({len(REDIRECTS)} redirects, {len(HEADERS)} header rules)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
