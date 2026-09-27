# Notes for agents

A Hugo site, built by GitHub Actions and served by a Cloudflare Worker. `README.md` is the full
manual and it is long: read only the section a task needs.

| For | Read |
|---|---|
| The front matter of a note, a project, a recipe, an album | README, "Writing" and "Photographs" |
| Drawings (`figure.svg`) and their rules | README, "Drawings" |
| Colours, typefaces, layout | README, "The look", and `assets/css/tokens.css` |
| Publishing, previews, the domain, headers, redirects | README, "Publishing" |
| The gate | README, "The gate", and below |
| Building and checking a change | `.claude/skills/verify/SKILL.md` |

```sh
scripts/build.sh && python3 scripts/check-site.py   # what GitHub runs; any Hugo warning stops it
node scripts/preview-gate.mjs                       # the built site with the gate in front, :8789
hugo server -D                                      # a quick look: no gate, no headers
```

## The gate

`gate = true` in `hugo.toml`. Anyone may see `/`, `/cv/` and `/enter/`; everything else asks for
the password, the secret `SITE_PASSWORD`, which is never in the repository. `scripts/build.sh`
builds twice: the open site into `public/` with `hugo.open.toml` laid over `hugo.toml`, and the
whole site into `public/_full/`.

What is open is written down in four places, and they must agree. To open a page or a section to
everyone while the gate stays on, change all four:

1. `hugo.open.toml`: `ignoreFiles` and `disableKinds` keep every page of projects, recipes, updates
   and photos, the pages that open those sections, tags and the feed out of the open build.
2. `worker/gate.js`: `OPEN_PAGES`, `OPEN_FILES` and `PRIVATE`.
3. `scripts/check-site.py`: `OPEN_FILES` and `check_gate`, which stop the build when the open site
   holds anything else or names a private page.
4. `layouts/home.html` and `layouts/_partials/footer.html`, which test `site.Params.open`.

A draft is a different thing: `draft: true` keeps a page off both sites.

## Rules

- A push to `master` publishes the live site. Work on a branch and open a pull request: it gets a
  preview address of its own.
- The repository is public, and so is every draft in it. Nothing private goes in.
- Name no address on the domain other than `muscaglar.com` and `www`. Never add
  `includeSubDomains` to `Strict-Transport-Security`.
- A header changed in `static/_headers` must be changed in `worker/gate.js` too; the check stops the
  build when they differ.
- No years on the pages, in the text or in the names of folders (`showYears = false`).
- Hugo is pinned in `scripts/build.sh`. Warnings and deprecation notices stop the build on purpose.
- Write as the README does: plain words, short sentences, British spelling. A commit subject is a
  plain sentence with no prefix, such as "Put the projects and the recipes on the site".
