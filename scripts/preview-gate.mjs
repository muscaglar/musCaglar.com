#!/usr/bin/env node
// Serves the built site on this computer with the gate in front of it, the way Cloudflare does.
//
//   scripts/build.sh
//   node scripts/preview-gate.mjs                 http://127.0.0.1:8789, password "open-sesame-on-this-laptop"
//   node scripts/preview-gate.mjs public 8790     another folder, another port
//   SITE_PASSWORD=… node scripts/preview-gate.mjs the password to ask for
//
// It runs worker/gate.js itself, unchanged. What stands in for Cloudflare is only the store of
// files behind it: a page for an address that ends in "/", a redirect to the address with "/" for
// a folder, and the nearest 404.html for what is not there. Needs Node 20 or later, nothing else.

import { createServer } from "node:http";
import { createHash } from "node:crypto";
import { readFile, stat } from "node:fs/promises";
import { dirname, extname, join, normalize, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

import gate from "../worker/gate.js";

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(process.argv[2] ?? join(here, "..", "public"));
const port = Number(process.argv[3] ?? 8789);
const password = process.env.SITE_PASSWORD ?? "open-sesame-on-this-laptop";

const KINDS = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".json": "application/json", ".xml": "application/xml", ".txt": "text/plain; charset=utf-8",
  ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
  ".webp": "image/webp", ".avif": "image/avif", ".ico": "image/vnd.microsoft.icon", ".woff2": "font/woff2", ".pdf": "application/pdf",
};
// Cloudflare keeps these two for itself and never serves them.
const KEPT_BACK = new Set(["/_headers", "/_redirects"]);

async function isFile(path) {
  try {
    return (await stat(path)).isFile();
  } catch {
    return false;
  }
}

function inside(path) {
  const file = normalize(join(root, path));
  return file === root || file.startsWith(root + sep) ? file : null;
}

async function file(path, status, method, request) {
  const body = await readFile(path);
  const tag = `"${createHash("sha256").update(body).digest("hex").slice(0, 32)}"`;
  const headers = { "Content-Type": KINDS[extname(path).toLowerCase()] ?? "application/octet-stream", ETag: tag, "Cache-Control": "public, max-age=0, must-revalidate" };
  if (status === 200 && request.headers.get("If-None-Match") === tag) return new Response(null, { status: 304, headers });
  return new Response(method === "HEAD" ? null : body, { status, headers });
}

// The store of files, as the gate sees it: env.ASSETS.
const store = {
  async fetch(request) {
    const url = new URL(request.url);
    let path;
    try {
      path = decodeURIComponent(url.pathname);
    } catch {
      return new Response("Bad request\n", { status: 400 });
    }
    if (KEPT_BACK.has(path)) return nearest404(path, request);
    const wanted = inside(path);
    if (wanted === null) return new Response("Bad request\n", { status: 400 });

    if (path.endsWith("/index.html")) return Response.redirect(new URL(path.slice(0, -"index.html".length), url.origin), 307);
    if (path.endsWith(".html") && (await isFile(wanted))) return Response.redirect(new URL(path.slice(0, -".html".length), url.origin), 307);
    if (path.endsWith("/")) {
      if (await isFile(join(wanted, "index.html"))) return file(join(wanted, "index.html"), 200, request.method, request);
      if (path !== "/" && (await isFile(wanted.slice(0, -1) + ".html"))) return Response.redirect(new URL(path.slice(0, -1), url.origin), 307);
      return nearest404(path, request);
    }
    if (await isFile(wanted)) return file(wanted, 200, request.method, request);
    if (await isFile(join(wanted, "index.html"))) return Response.redirect(new URL(path + "/", url.origin), 307);
    if (await isFile(wanted + ".html")) return file(wanted + ".html", 200, request.method, request);
    return nearest404(path, request);
  },
};

async function nearest404(path, request) {
  let folder = path.endsWith("/") ? path : path.slice(0, path.lastIndexOf("/") + 1);
  for (;;) {
    const candidate = inside(join(folder, "404.html"));
    if (candidate && (await isFile(candidate))) return file(candidate, 404, request.method, request);
    if (folder === "/" || folder === "") break;
    folder = folder.slice(0, folder.slice(0, -1).lastIndexOf("/") + 1);
  }
  return new Response("Not found\n", { status: 404, headers: { "Content-Type": "text/plain; charset=utf-8" } });
}

const server = createServer(async (incoming, outgoing) => {
  try {
    const chunks = [];
    let size = 0;
    for await (const chunk of incoming) {
      size += chunk.length;
      if (size > 64 * 1024) {
        outgoing.writeHead(413).end();
        return;
      }
      chunks.push(chunk);
    }
    const headers = new Headers();
    for (let i = 0; i < incoming.rawHeaders.length; i += 2) headers.append(incoming.rawHeaders[i], incoming.rawHeaders[i + 1]);
    const has = incoming.method !== "GET" && incoming.method !== "HEAD";
    // The address is handed over exactly as it came, so that odd addresses can be tried out.
    let request;
    try {
      request = new Request(`http://${incoming.headers.host ?? `127.0.0.1:${port}`}${incoming.url}`, {
        method: incoming.method, headers, body: has ? Buffer.concat(chunks) : undefined, redirect: "manual",
      });
    } catch {
      // A method or an address that cannot be made into a request at all, such as TRACE.
      outgoing.writeHead(405, { "Content-Type": "text/plain; charset=utf-8" }).end("That request cannot be made.\n");
      return;
    }
    const response = await gate.fetch(request, { ASSETS: store, SITE_PASSWORD: password });
    const out = {};
    for (const [name, value] of response.headers) if (name.toLowerCase() !== "set-cookie") out[name] = value;
    const cookies = response.headers.getSetCookie();
    if (cookies.length) out["Set-Cookie"] = cookies;
    outgoing.writeHead(response.status, out);
    outgoing.end(response.body ? Buffer.from(await response.arrayBuffer()) : undefined);
  } catch (error) {
    console.error(error);
    outgoing.writeHead(500, { "Content-Type": "text/plain; charset=utf-8" }).end("The preview failed; see the terminal.\n");
  }
});

// This computer only: nobody else on the network can reach it.
server.listen(port, "127.0.0.1", () => {
  console.log(`The site with its gate: http://127.0.0.1:${port}  (from ${root})`);
  console.log(`The password on this computer: ${password}`);
});
