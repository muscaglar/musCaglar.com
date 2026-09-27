// The gate in front of the site.
//
// The site is built twice (scripts/build.sh). What everyone may see lies at the root of ./public:
// the landing page, the CV, the page with the password form, and the stylesheets, scripts, fonts
// and icons. The whole site lies beside it in ./public/_full. Every request comes here first
// (`run_worker_first` in wrangler.jsonc), and this file decides which of the two to answer from.
//
//   no password given     the landing page, the CV, the form; everything else asks for the password
//   password given        the whole site, read from /_full but shown at its ordinary addresses
//
// The password is the secret SITE_PASSWORD of the Worker. It is not in this repository. Without it
// no password is accepted, so the private pages stay closed to everyone.
//
// When the site is built without a gate (gate = false in hugo.toml) there is no /_full, and this
// file serves the one site to everyone. It still adds the headers, because Cloudflare applies
// the files _headers and _redirects only to what it serves without a Worker.

const FULL = "/_full";
const DAYS = 30;
const SECONDS = DAYS * 24 * 60 * 60;
const WAIT_AFTER_A_WRONG_PASSWORD = 500; // milliseconds

// What a visitor without the password may be given, by its decoded address.
const OPEN_PAGES = new Set(["/", "/cv", "/cv/", "/enter", "/enter/"]);
const OPEN_FILES = /^\/(?:(?:css|js|fonts|images)\/[^/]+(?:\/[^/]+)*|favicon\.ico|robots\.txt|sitemap\.xml)$/;
// What asks for the password. Anything else that is not open is simply not found.
const PRIVATE = /^\/(?:projects|recipes|updates|photos|tags|about|figures)(?:\/|$)|^\/index\.xml$/;

// The headers of every answer. Keep them the same as static/_headers: scripts/check-site.py compares.
const HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=(), browsing-topics=()",
  "Cross-Origin-Opener-Policy": "same-origin",
  "Strict-Transport-Security": "max-age=31536000",
  "Content-Security-Policy":
    "default-src 'self'; script-src 'self' 'inline-speculation-rules'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; media-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests",
};
// Files whose names change when their contents do may be kept by a browser for a year.
const KEPT_FOR_A_YEAR = /^\/(?:css|js)\/|\.(?:avif|webp|woff2)$/;

const encoder = new TextEncoder();

export default {
  async fetch(request, env) {
    try {
      return await answer(request, env);
    } catch (error) {
      // Say nothing of what went wrong to the visitor; the log of the Worker has it.
      console.error("gate:", error && error.stack ? error.stack : error);
      return plain(500, "Something went wrong.");
    }
  },
};

async function answer(request, env) {
  const url = new URL(request.url);
  const path = decoded(url.pathname);
  if (path === null) return plain(400, "That address cannot be read.");

  // The whole site is never given out under the address it is stored at.
  if (/^\/_full(?:\/|$)/i.test(path)) return notFound(request, env, url, "");

  const gated = await gateIsOn(env, url);
  const local = url.hostname === "localhost" || url.hostname === "127.0.0.1";
  const secure = url.protocol === "https:";

  if (path === "/enter" || path === "/enter/") {
    // With the gate off there is nothing to sign in to.
    if (!gated) return redirect(url, "/", 303);
    if (request.method === "POST") {
      if (!secure && !local) return plain(400, "The password is only taken over HTTPS.");
      return enter(request, env, url, secure);
    }
  }
  if (path === "/leave" || path === "/leave/") {
    if (request.method !== "POST") return withHeaders(plain(405, "Use the button on the page."), { Allow: "POST" });
    if (foreign(request, url)) return plain(403, "That request came from another site.");
    return withHeaders(redirect(url, "/", 303), { "Set-Cookie": cookie(secure, "", 0) });
  }
  if (request.method !== "GET" && request.method !== "HEAD") {
    return withHeaders(plain(405, "Only reading is possible here."), { Allow: "GET, HEAD" });
  }

  const inside = gated ? await hasPassed(request, env, secure) : true;
  const store = gated && inside ? FULL : "";

  // Addresses of the old site.
  const old = await oldAddress(env, url, store, path);
  if (old) return withHeaders(redirect(url, old.to, old.status), robots(url));

  if (inside) return fromStore(request, env, url, store, path, gated);

  if (OPEN_PAGES.has(path) || OPEN_FILES.test(path)) return fromStore(request, env, url, "", path, gated);
  if (PRIVATE.test(path)) {
    return withHeaders(redirect(url, `/enter/?next=${encodeURIComponent(path + url.search)}`, 303), { "X-Robots-Tag": "noindex" });
  }
  return notFound(request, env, url, "");
}

// ---------------------------------------------------------------------------------------------
// Addresses

// The address as a visitor means it: decoded once, and refused when it is anything but plain.
// Deciding on the decoded address, and asking the store for exactly that address, leaves no room
// between what is checked and what is fetched.
function decoded(pathname) {
  let path;
  try {
    path = decodeURIComponent(pathname);
  } catch {
    return null; // a broken %-sequence
  }
  if (!path.startsWith("/")) return null;
  if (/%[0-9a-f]{2}/i.test(path)) return null; // encoded twice
  if (/[\u0000-\u001f\u007f\\]/.test(path)) return null; // control characters, backslashes
  if (path.includes("//")) return null;
  if (path.split("/").some((part) => part === "." || part === "..")) return null;
  if (path.length > 1024) return null;
  return path;
}

function encoded(path) {
  return path.split("/").map(encodeURIComponent).join("/");
}

// Only addresses on this site, written as a path.
function safeNext(value) {
  if (typeof value !== "string" || value.length === 0 || value.length > 512) return "/";
  if (!value.startsWith("/") || value.startsWith("//")) return "/";
  if (/[\u0000-\u001f\u007f\\]/.test(value)) return "/";
  const [path] = value.split(/[?#]/, 1);
  const plainPath = decoded(path);
  if (plainPath === null || /^\/_full(?:\/|$)/i.test(plainPath)) return "/";
  if (plainPath === "/enter" || plainPath === "/enter/" || plainPath === "/leave" || plainPath === "/leave/") return "/";
  const query = value.includes("?") ? "?" + value.slice(value.indexOf("?") + 1).split("#", 1)[0] : "";
  return encoded(plainPath) + query;
}

// ---------------------------------------------------------------------------------------------
// The store of files

let gateKnown = null; // whether this build has a gate; the same for the life of this Worker

async function gateIsOn(env, url) {
  if (gateKnown === null) {
    const probe = await env.ASSETS.fetch(new Request(new URL(`${FULL}/gate.txt`, url.origin), { method: "HEAD" }));
    gateKnown = probe.status === 200;
  }
  return gateKnown;
}

async function fromStore(request, env, url, store, path, gated) {
  const headers = new Headers();
  for (const name of ["Accept", "Accept-Encoding", "If-None-Match", "If-Modified-Since", "Range"]) {
    const value = request.headers.get(name);
    if (value !== null) headers.set(name, value);
  }
  const found = await env.ASSETS.fetch(new Request(new URL(store + encoded(path), url.origin), { method: request.method, headers, redirect: "manual" }));
  const response = new Response(found.body, found);
  relocate(response, store, url);
  dress(response, url, path, { behind: store === FULL, gated });
  return response;
}

async function notFound(request, env, url, store) {
  // An address that does not exist brings back the nearest 404 page.
  const found = await env.ASSETS.fetch(new Request(new URL(`${store}/there-is-no-such-page`, url.origin), { method: request.method === "HEAD" ? "HEAD" : "GET" }));
  const response = new Response(found.body, { status: 404, headers: found.headers });
  dress(response, url, "/404", { behind: false, gated: true });
  response.headers.set("Cache-Control", "no-store");
  return response;
}

// The store answers with its own addresses. A visitor never sees /_full, and is never sent
// anywhere but to this site.
function relocate(response, store, url) {
  const to = response.headers.get("Location");
  if (to === null) return;
  let target;
  try {
    target = new URL(to, url.origin);
  } catch {
    response.headers.set("Location", "/");
    return;
  }
  let path = target.origin === url.origin ? target.pathname : "/";
  if (store !== "" && (path === store || path.startsWith(store + "/"))) path = path.slice(store.length) || "/";
  response.headers.set("Location", path + (target.origin === url.origin ? target.search : ""));
}

// The headers of an answer: the ones every answer has, and how long it may be kept.
function dress(response, url, path, { behind, gated }) {
  for (const [name, value] of Object.entries(HEADERS)) response.headers.set(name, value);
  const page = (response.headers.get("Content-Type") || "").includes("text/html");
  if (behind) {
    // Pages behind the gate are for the one who has the password, and for no cache in between.
    response.headers.set("Cache-Control", page || !KEPT_FOR_A_YEAR.test(path) ? "private, no-store" : "private, max-age=31556952, immutable");
    response.headers.set("X-Robots-Tag", "noindex");
    response.headers.append("Vary", "Cookie");
    return;
  }
  if (KEPT_FOR_A_YEAR.test(path) && response.status === 200) {
    response.headers.set("Cache-Control", "public, max-age=31556952, immutable");
  } else if (page && gated) {
    // The same address shows another page once the password is given.
    response.headers.set("Cache-Control", "private, no-cache");
    response.headers.append("Vary", "Cookie");
  }
  for (const [name, value] of Object.entries(robots(url))) response.headers.set(name, value);
  if (path === "/enter" || path === "/enter/") response.headers.set("X-Robots-Tag", "noindex");
}

// Search engines should list muscaglar.com only, not Cloudflare's own addresses for the site.
function robots(url) {
  return url.hostname.endsWith(".workers.dev") ? { "X-Robots-Tag": "noindex" } : {};
}

// ---------------------------------------------------------------------------------------------
// Addresses of the old site: redirects.json, made by the build from the `aliases` of every page

const lists = new Map();

async function oldAddress(env, url, store, path) {
  if (!lists.has(store)) {
    let list = { exact: {}, beginning: [] };
    const found = await env.ASSETS.fetch(new Request(new URL(`${store}/redirects.json`, url.origin)));
    if (found.status === 200) {
      try {
        const read = await found.json();
        if (read && typeof read.exact === "object" && Array.isArray(read.beginning)) list = read;
      } catch {
        // an unreadable list is an empty list
      }
    }
    lists.set(store, list);
  }
  const list = lists.get(store);
  const exact = Object.prototype.hasOwnProperty.call(list.exact, path) ? list.exact[path] : null;
  const rule = exact || list.beginning.find((entry) => path.startsWith(entry.from) && path.length > entry.from.length) || null;
  if (!rule || typeof rule.to !== "string" || !rule.to.startsWith("/") || rule.to.startsWith("//")) return null;
  return { to: rule.to, status: [301, 302, 303, 307, 308].includes(rule.status) ? rule.status : 302 };
}

// ---------------------------------------------------------------------------------------------
// The password

async function enter(request, env, url, secure) {
  if (foreign(request, url)) return plain(403, "That request came from another site.");
  const length = Number(request.headers.get("Content-Length") || "0");
  if (!(length > 0 && length <= 4096)) return plain(400, "That form cannot be read.");
  const kind = request.headers.get("Content-Type") || "";
  if (!kind.startsWith("application/x-www-form-urlencoded") && !kind.startsWith("multipart/form-data")) {
    return plain(400, "That form cannot be read.");
  }
  let form;
  try {
    form = await request.formData();
  } catch {
    return plain(400, "That form cannot be read.");
  }
  const given = form.get("password");
  const next = safeNext(form.get("next"));
  const wanted = passwordOf(env);

  let right = false;
  if (wanted !== null && typeof given === "string" && given.length > 0 && given.length <= 200) {
    right = same(await digest(given), await digest(wanted));
  }
  if (!right) {
    await new Promise((done) => setTimeout(done, WAIT_AFTER_A_WRONG_PASSWORD));
    return withHeaders(redirect(url, `/enter/?wrong=1&next=${encodeURIComponent(next)}`, 303), { "X-Robots-Tag": "noindex" });
  }
  const until = Math.floor(Date.now() / 1000) + SECONDS;
  const pass = `v1.${until}.${await sign(wanted, `v1.${until}`)}`;
  return withHeaders(redirect(url, next, 303), { "Set-Cookie": cookie(secure, pass, SECONDS), "X-Robots-Tag": "noindex" });
}

function passwordOf(env) {
  const value = env.SITE_PASSWORD;
  return typeof value === "string" && value.length >= 8 ? value : null;
}

async function hasPassed(request, env, secure) {
  const wanted = passwordOf(env);
  if (wanted === null) return false;
  const name = cookieName(secure);
  const all = request.headers.get("Cookie") || "";
  for (const part of all.split(";")) {
    const at = part.indexOf("=");
    if (at === -1 || part.slice(0, at).trim() !== name) continue;
    const found = /^v1\.(\d{1,12})\.([A-Za-z0-9_-]{43})$/.exec(part.slice(at + 1).trim());
    if (!found) continue;
    const until = Number(found[1]);
    const now = Math.floor(Date.now() / 1000);
    if (!(until > now && until <= now + SECONDS + 60)) continue;
    if (same(encoder.encode(found[2]), encoder.encode(await sign(wanted, `v1.${until}`)))) return true;
  }
  return false;
}

// A request that says it comes from another site is not acted on.
function foreign(request, url) {
  const origin = request.headers.get("Origin");
  if (origin !== null) return origin !== url.origin;
  const site = request.headers.get("Sec-Fetch-Site");
  return site !== null && site !== "same-origin" && site !== "none";
}

function cookieName(secure) {
  // The prefix __Host- makes a browser refuse the cookie unless it is for this one host, over HTTPS.
  return secure ? "__Host-pass" : "pass";
}

function cookie(secure, value, seconds) {
  return `${cookieName(secure)}=${value}; Path=/; Max-Age=${seconds}; HttpOnly; SameSite=Lax${secure ? "; Secure" : ""}`;
}

async function digest(text) {
  return new Uint8Array(await crypto.subtle.digest("SHA-256", encoder.encode(text)));
}

async function sign(password, text) {
  const key = await crypto.subtle.importKey("raw", await digest(`muscaglar-gate:${password}`), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const signature = new Uint8Array(await crypto.subtle.sign("HMAC", key, encoder.encode(text)));
  let binary = "";
  for (const byte of signature) binary += String.fromCharCode(byte);
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

// Compares every byte, however early the first difference comes.
function same(a, b) {
  if (a.length !== b.length) return false;
  let difference = 0;
  for (let i = 0; i < a.length; i++) difference |= a[i] ^ b[i];
  return difference === 0;
}

// ---------------------------------------------------------------------------------------------
// Small answers

function plain(status, text) {
  return withHeaders(new Response(text + "\n", { status, headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" } }), HEADERS);
}

function redirect(url, to, status) {
  return withHeaders(new Response(null, { status, headers: { Location: new URL(to, url.origin).pathname + new URL(to, url.origin).search, "Cache-Control": "no-store" } }), HEADERS);
}

function withHeaders(response, headers) {
  for (const [name, value] of Object.entries(headers)) response.headers.set(name, value);
  return response;
}
