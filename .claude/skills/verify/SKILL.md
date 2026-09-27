---
name: verify
description: How to build, serve and drive this site to check that a change works.
---

# Verifying a change to this site

The site is static: Hugo builds it, Cloudflare serves it. Verify by building, serving the result
and using the pages in a browser.

## Build and serve

```sh
hugo build --gc --minify --panicOnWarning --buildDrafts --destination /tmp/site-check
python3 scripts/preview-built.py /tmp/site-check 8788      # http://127.0.0.1:8788
```

- `--buildDrafts` adds the drafts: the sample album, the sample recipe, About and the proof sheet
  of drawings (`/figures/`). The projects and recipes are published, so they are there either way.
- `scripts/preview-built.py` applies `_headers` (including the content security policy) and
  `_redirects`, and serves the not-found page. `hugo server -D` is quicker for looks, but applies
  none of those.
- `scripts/preview-built.py` is a stand-in for Cloudflare, not Cloudflare. Its real behaviour can
  only be confirmed on a preview, which the workflow publishes for every pull request.
- `scripts/build.sh` is what GitHub runs. It needs the pinned Hugo version and stops on warnings
  and deprecation notices.

### With the gate

While `gate = true` in `hugo.toml`, `scripts/build.sh` builds two sites: the open one into the
folder, the whole one into `_full` inside it. Serve them as Cloudflare does, with the gate in front:

```sh
scripts/build.sh --destination /tmp/site-check
node scripts/preview-gate.mjs /tmp/site-check 8789      # http://127.0.0.1:8789, prints its password
```

- This runs `worker/gate.js` itself. Only the store of files behind it is a stand-in.
- `python3 scripts/preview-built.py /tmp/site-check/_full` still serves the whole site without a gate.
- Send crooked addresses with `curl --path-as-is`, or curl tidies them before they leave.
- The real thing is the preview of a pull request. It has the password only if the repository
  has the secret `SITE_PASSWORD`.

## Flows worth driving

| Flow | Where | Expect |
|---|---|---|
| Theme switch | "Theme: Auto" in the header and in the footer, any page | each click moves on: Auto, Light, Dark; both switches show the same word; the choice survives moving to another page; Auto forgets it |
| Photo viewer | `/photos/sample-album/` | click opens a full-screen viewer; ← → move and wrap around; Esc closes |
| Figures | `/projects/great-crested-newts/` | 5 figures with captions, 1 table, no broken pictures |
| Feed | `/index.xml` | parses as XML; every `src` and `href` in it is a full address |
| Sideways photo | an album with a picture whose Exif orientation is 6 | published upright (taller than wide) |
| Recipe | `/recipes/sample-flatbreads/` | time, quantity, ingredients beside the method, notes below |
| Updates | `/updates/` | notes in full; projects, recipes and albums as a line each, all labelled with their kind |
| CV | `/cv/` | sections come from `data/cv.yaml`; entries marked `hide: true` are absent; print view has no header or footer |
| Old addresses | `curl -I /me`, `/posts_tem_recon`, `/posts_anything` | 301 to the new page; unknown `/posts_*` get a 302 |
| Not found | any unknown address | status 404 with the site's own page |
| Without JavaScript | album page | text readable, theme switches absent, a photo link opens the picture itself |
| Sections | `/`, `/projects/`, `/cv/` | a rule with a red mark opens each; number and title in the first column, content in the other three; one column below 62rem |
| Drawings | `/`, `/projects/`, a project with `figure:` | inline SVG in the page, coloured by the theme; one red element; "Fig. n" counts up through a page |
| Years | every page, with `showYears = false` (the default) | no year in any visible text; notes show day and month; projects, recipes, albums and the CV show no date; "©" has no year |
| Proof sheet | `/figures/` (drafts only) | every drawing at three sizes, on light and on dark paper |
| Phone | `/` at 390 wide | the drawings are one row that swipes sideways; the page itself never scrolls sideways |
| Gate, closed | `/`, `/cv/`, then `/projects/` without signing in | landing page with the menu Home and CV only; `/projects/` leads to `/enter/`; no title of a private page anywhere in the HTML |
| Gate, signing in | **Sign in** in the footer, wrong password, then the right one | wrong: back on the form with "That is not the password."; right: the page first asked for opens, and the menu has every section |
| Gate, signing out | **Sign out** in the footer | back on the landing page; `/projects/` asks for the password again |
| Gate, the store | `curl --path-as-is` for `/_full/`, `/%5Ffull/`, `/css/..%2f_full/` | 404 or 400, never a page of the whole site |

Watch the browser console while driving: a blocked script or style shows up there as a content
security policy error.

## Gotchas

- Pictures below the fold load lazily. Scroll the page before judging a full-page screenshot.
- The layout answers to the width of the sheet (container queries), not of the window: 62rem and
  40rem are where it changes. Check just above and just below both.
- A drawing with a script, a link or an embedded picture in it stops the build on purpose
  (`layouts/_partials/sketch.html`).
- Asking for the address of an original picture in a template (`.RelPermalink` on the resource
  itself rather than on a resized copy) publishes the original. `scripts/check-site.py` catches it
  under `/photos/`.
- Hugo's deprecation notices fail the build because of `--panicOnWarning`. That is intended.
