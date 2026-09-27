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

- `--buildDrafts` matters: the sample album and the projects carried over from the old site are
  drafts, so without it there is almost nothing to look at.
- `scripts/preview-built.py` applies `_headers` (including the content security policy) and
  `_redirects`, and serves the not-found page. `hugo server -D` is quicker for looks, but applies
  none of those.
- `scripts/preview-built.py` is a stand-in for Cloudflare, not Cloudflare. Its real behaviour can
  only be confirmed on a preview, which the workflow publishes for every pull request.
- `scripts/build.sh` is what GitHub runs. It needs the pinned Hugo version and stops on warnings
  and deprecation notices.

## Flows worth driving

| Flow | Where | Expect |
|---|---|---|
| Theme switch | button in the header, any page | Auto → Light → Dark → Auto; the choice survives moving to another page |
| Photo viewer | `/photos/sample-album/` | click opens a full-screen viewer; ← → move and wrap around; Esc closes |
| Figures | `/projects/great-crested-newts/` | 5 figures with captions, 1 table, no broken pictures |
| Feed | `/index.xml` | parses as XML; every `src` and `href` in it is a full address |
| Sideways photo | an album with a picture whose Exif orientation is 6 | published upright (taller than wide) |
| CV | `/cv/` | sections come from `data/cv.yaml`; entries marked `hide: true` are absent; print view has no header or footer |
| Old addresses | `curl -I /me`, `/posts_tem_recon`, `/posts_anything` | 301 to the new page; unknown `/posts_*` get a 302 |
| Not found | any unknown address | status 404 with the site's own page |
| Without JavaScript | album page | text readable, theme button absent, a photo link opens the picture itself |

Watch the browser console while driving: a blocked script or style shows up there as a content
security policy error.

## Gotchas

- Pictures below the fold load lazily. Scroll the page before judging a full-page screenshot.
- Asking for the address of an original picture in a template (`.RelPermalink` on the resource
  itself rather than on a resized copy) publishes the original. `scripts/check-site.py` catches it
  under `/photos/`.
- Hugo's deprecation notices fail the build because of `--panicOnWarning`. That is intended.
