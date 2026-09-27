# muscaglar.com

My personal website: projects, recipes, photographs, short notes and a CV.

The site is a folder of plain text files. [Hugo](https://gohugo.io) turns them into web pages.
Whenever a change reaches GitHub, the site is built, checked and published to Cloudflare. There is
no database, no JavaScript framework and nothing to install besides Hugo itself.

- [Day to day](#day-to-day)
- [Where things are](#where-things-are)
- [Writing](#writing)
- [Photographs](#photographs)
- [Drawings](#drawings)
- [The look](#the-look)
- [Publishing](#publishing)
- [Checks](#checks)
- [Setting up on a new machine](#setting-up-on-a-new-machine)
- [Upgrading Hugo](#upgrading-hugo)

## Day to day

| I want to… | Do this |
|---|---|
| See the site while I work | `hugo server -D` and open <http://localhost:1313>. The page reloads as files are saved. `-D` also shows drafts. |
| Post a note | `hugo new content updates/2026-10-01-a-title.md`, write below the dashes, save. |
| Add a recipe | `hugo new content recipes/a-title`. This makes a folder with an `index.md`; pictures go in the same folder. |
| Add a project | `hugo new content projects/a-title`. Same: a folder with an `index.md`. |
| Add photographs | `hugo new content photos/an-album`, then drop the pictures into the new folder. |
| Give a page a drawing | Put `figure.svg` in the page's folder and name it in the front matter. See [Drawings](#drawings). |
| See every drawing at once | `hugo server -D`, then open <http://localhost:1313/figures/>. |
| Change the CV | Edit `data/cv.yaml`. The top of the file explains the layout. |
| Change the words on the home page | Edit `intro` and `skills` in `content/_index.md`. |
| Have an About page | Delete `draft: true` in `content/about.md`, and add it to the menu in `hugo.toml`. |
| Change the links in the footer, or the menu | Edit `hugo.toml`. |
| Keep something unpublished | Leave `draft: true` in its front matter. Delete the line to publish. |
| Publish | Commit and push to `master`. The live site updates a minute or two later. |
| Try a change before it goes live | Push it to another branch and open a pull request. A preview with its own address is posted on the pull request. |

New files made with `hugo new content` start as drafts.

Everything new shows up in **Updates** and in the feed, labelled with its kind: a note, a project,
a recipe, photos. "New" means dated on or after `streamSince` in `hugo.toml`. A section with nothing published in it is left out of the menu.

## Where things are

```text
content/            Everything that is written: one file or folder per page
  _index.md           the home page
  about.md            the About page
  cv.md               the CV page (its content comes from data/cv.yaml)
  projects/           one folder per project
  recipes/            one folder per recipe
  photos/             one folder per album
  updates/            one file per note
data/cv.yaml        The CV
hugo.toml           Settings: site title, menu, links, picture quality
layouts/            The HTML templates
assets/css/         The stylesheets. Colours, sizes and typefaces are in tokens.css
assets/figures/     The drawings that stand for the sections, and the one on the not-found page
assets/fonts/       The typefaces, served from this site
assets/images/      The name as a drawing, the icon, and the picture used in link previews
assets/js/          Small scripts: theme switch, photo viewer
static/             Files published exactly as they are (_headers sets Cloudflare's headers)
archetypes/         The starting text of new files made with `hugo new content`
scripts/            build.sh builds the site, check-site.py checks it, preview-built.py serves it locally,
                    signature/ redraws the name and cuts the typeface of the titles
wrangler.jsonc      How Cloudflare serves the site
.github/workflows/  What GitHub does on every push: build, check, publish
```

## Writing

Pages are written in Markdown. The block between the `---` lines at the top of a file is its front
matter: the title, the date and other details.

### A note

```markdown
---
title: "A title"
tags: [Site]
---

The text.
```

The date and the address come from the file name: `2026-10-01-a-title.md` is dated 1 October 2026
and appears at `/updates/a-title/`.

### A project

```markdown
---
title: "A title"
date: 2026-10-01
period: "March – June 2026"    # optional: shown instead of the date, while years are shown
summary: "One or two sentences, shown in lists and link previews."
kind: software                 # software, hardware, research or tinkering: the heading it is listed under
tags: [Python]
status: ongoing                # optional: ongoing, finished or paused
figure: figure.svg             # optional: the drawing of the project (see Drawings)
figure_caption: "What the drawing shows."
cover: picture.jpg             # optional: used in link previews, and in lists when there is no drawing
featured: true                 # optional: show on the home page
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/example
aliases:                       # optional: old addresses that should lead here
  - /an-old-address
---

The write-up.
```

### A recipe

```markdown
---
title: "Flatbreads in a pan"
date: 2026-10-01
summary: "One line about the dish."
course: side                   # snack, breakfast, main, side, dessert or coffee: the heading it is listed under
status: tested                 # tested, developing (made, not settled yet) or concept (an idea, not made yet)
time: "40 min"
makes: "Makes 6"
tags: [Bread]
figure: figure.svg             # optional: the drawing of the dish (see Drawings)
figure_caption: "What the drawing shows."
cover: picture.jpg             # optional
develop:                       # optional: what is still to be worked out
  - "How long the dough rests."
ingredients:
  - 250 g plain flour
  - 200 g natural yoghurt
---

1. The method, as a numbered list.
2. …

## Notes

What to change next time.
```

Ingredients can be grouped:

```yaml
ingredients:
  - group: For the dough
    items:
      - 250 g plain flour
  - group: To finish
    items:
      - Olive oil
```

A recipe can be unfinished, and say so. Whatever is listed under `develop` appears at the foot of
the page under "Still to work out", each with a box to tick in the mind. Take a line out when it
is settled. A recipe with `status: concept` is marked as an idea in every list, and one with
`status: developing` as in progress. Projects can have a `develop` list too.

Any other word under `course` makes a heading of its own, after the ones named above.

`content/recipes/sample-flatbreads/` is a draft that shows the layout; delete it when it is no
longer useful.

### Dates and years

Years are left off the pages.

| Kind of page | What a visitor sees |
|---|---|
| A project, a recipe, an album | No date at all. Lists are still in order of date, newest first. |
| A note | The day and the month: "27 September" |
| The CV | No dates |

The `date` of a page is still needed: it puts the page in its place in a list.

Projects, recipes and albums dated before `streamSince` in `hugo.toml` stay out of **Updates** and
of the feed. Set that day to when the log began; work from before it is listed in its own section
only.

To show years again, set `showYears = true` in `hugo.toml`. Lists then show the year, notes their
full date, and the CV its dates.

One thing to keep in mind when writing: a sentence such as "I built this in 2019" puts the year
back. So do the names of folders, which become part of the address: `smart-home`, not
`smart-home-2017`.

### Pictures in a page

Put the picture in the same folder as the page, then:

```markdown
![What the picture shows](picture.jpg "An optional caption")
```

Two to four pictures side by side:

```markdown
{{< figures >}}
![First picture](a.png "Caption")
![Second picture](b.png "Caption")
{{< /figures >}}
```

Pictures are resized and converted to modern formats automatically, so add them at full size.

A drawing inside the text (see [Drawings](#drawings)):

```markdown
{{< drawing file="first-version.svg" caption="What it shows." >}}
{{< drawing file="architecture.svg" caption="How the parts fit." wide=true >}}
```

With `wide=true` the drawing takes the full width of the text. That is for a diagram with many
parts: draw it in a frame of 480 by 270, with up to twelve labels.

## Photographs

An album is a folder in `content/photos/` with an `index.md` and the pictures beside it.

```markdown
---
title: "An album"
date: 2026-10-01
summary: "A sentence about it."
cover: picture.jpg             # optional: the first picture is used otherwise
location: "Somewhere"          # optional
order: name                    # optional: sort by file name instead of by the time taken
photos:                        # optional: captions, matched by file name
  - file: picture.jpg
    caption: "A caption"
  - file: another.jpg
    hide: true                 # keep the file but leave it out of the album
---
```

Every picture in the folder appears in the album, oldest first. The camera, lens and exposure are
read from each file and shown under the picture.

**Before adding pictures.** Export them as JPEG in the sRGB colour space. Colour profiles are not
carried over to the published copies, so a picture in a wider colour space would look dull, and
HEIC files cannot be processed. Full camera resolution is fine.

**Privacy.** The original files are never published. Visitors get resized copies, which carry no
camera or location data. The check that runs on every push fails if an original photograph, or any
file with such data in it, is about to be published.

`content/photos/sample-album/` holds placeholder pictures that show how an album looks. It is a
draft, so it is never published; delete the folder when it is no longer useful.

## Drawings

Every section has a drawing, and so can every page: a thin line drawing with a few small labels and
one thing in red. The home page shows the drawings of the sections as its way in; the list of
projects shows one per project; a page shows its own in the margin, as figure 1.

To give a page a drawing, put the file in the page's folder and name it in the front matter:

```yaml
figure: figure.svg
figure_caption: "A moka pot in section. Steam pushes the water up through the grounds."
```

The drawings of the sections are in `assets/figures/` and are named in the same way, in the
`_index.md` of each section (and in `content/cv.md`).

A drawing is an SVG file that starts from this frame:

```svg
<svg xmlns="http://www.w3.org/2000/svg" class="sketch" viewBox="0 0 240 180" role="img" aria-label="One sentence.">
  <path class="sk-ink" d="…"/>
  <path class="sk-accent" d="…"/>
  <path class="sk-line" d="…"/>
  <text x="…" y="…">label</text>
</svg>
```

| Class | Use |
|---|---|
| `sk-ink` | the object itself |
| `sk-line` | axes, leader lines, dimension lines, lesser detail |
| `sk-dash` | hidden edges, levels, guides |
| `sk-accent` | the one red element |
| `sk-dot`, `sk-accent-dot` | small filled dots |
| `sk-hole` | a shape that must cover what is behind it |
| `sk-atoms` | a row of dots, as in a sheet of atoms seen side on |

The rules that keep the drawings alike:

1. The frame is 240 by 180. Keep 8 units free on every side.
2. Lines only, all of one weight. No fills except small dots.
3. One thing is red: what the drawing is about.
4. At most five labels, in lower case, one to three words each.
5. Draw what someone who knows the subject would call correct: a section, a circuit, a plan, a
   graph of what the thing measures. Not a logo and not a cartoon.

The site colours the drawing itself, in both themes, so a drawing needs no colours of its own. A
`<style>` block in the file is ignored; the files in `assets/figures/` carry one only so that they
also look right when opened on their own.

A drawing may hold shapes and text only. A file with a script, a link or an embedded picture in it
stops the build.

`hugo server -D` and <http://localhost:1313/figures/> show every drawing at three sizes, on light
and on dark paper. That page is a draft, so it is never published.

Pictures and further drawings inside a page are numbered after it: figure 2, figure 3 and so on.

## The look

| To change | Edit |
|---|---|
| A colour, a type size, the spacing | `assets/css/tokens.css`. Every colour is given twice, for light and for dark. |
| The red | `--color-accent` in `assets/css/tokens.css` |
| The size of the name | `--name-size` in `assets/css/tokens.css` |
| The typefaces | The files in `assets/fonts/`, their list in `layouts/_partials/fonts.html`, and `--font-sans`, `--font-mono` and `--font-display` in `tokens.css` |
| The rule and the red mark that open a section | `--rule-strong`, `--mark-width` and `--mark-height` in `assets/css/tokens.css` |
| The words in the header, such as "Scholar" for Google Scholar | `short` beside the link in `hugo.toml` |
| The icon in the browser tab | `assets/images/icon.svg`, and `icon.png` (512 pixels square, for phones) |
| The picture in link previews | `assets/images/social.png`, for pages without a cover of their own |

The text is set in IBM Plex Sans and IBM Plex Mono, the titles in Special Gothic, condensed and
semi-bold. Their licences are beside them in `assets/fonts/`.

Only a small part of Special Gothic is served: one weight, one width, and the letters of the
European languages that are written in Latin script. A title with a letter from outside that set
shows that letter in another typeface. To cut the file again, with other letters or another weight, change
`scripts/signature/display-font.sh` and run it:

```sh
brew install harfbuzz woff2
scripts/signature/display-font.sh path/to/SpecialGothic.ttf
```

The name is a drawing, `assets/images/signature.svg`, made from the same typeface, so that the
marks on its letters can be red. To redraw it, for another wording or weight:

```sh
python3 scripts/signature/make.py path/to/SpecialGothic.ttf "Mustafa Çağlar"
```

The typeface is free to download from <https://fonts.google.com/specimen/Special+Gothic>.

### How a page is laid out

Every page stands on four columns.

| Page | First column | Second and third | Fourth |
|---|---|---|---|
| Home | The name, then the title of each section | The introduction, then what each section holds (it runs on into the fourth) | |
| A project, a note | What it is filed under, and its facts | The title and the text | Its drawing |
| A recipe | The ingredients | The title and the method | Its drawing and its facts |
| A list, the CV | The title of each section | What the section holds (it runs on into the fourth) | The drawing of the section, beside the heading |

Each section opens with a rule and a small red mark. On a narrow screen the columns follow one
another down the page.

## Publishing

GitHub does the work; Cloudflare serves the result. The steps are in `.github/workflows/site.yml`.

| When | What happens |
|---|---|
| A push to `master` | The site is built and checked. If the checks pass, that same build is published to muscaglar.com. |
| A pull request | The site is built and checked. A preview is published and its address is posted on the pull request. |
| A pull request is closed | Its preview is removed. |

If a check fails, nothing is published and the live site stays as it was.

### First-time set-up

GitHub needs to know which Cloudflare account to publish to, and be allowed to.

1. **Account ID.** In the [Cloudflare dashboard](https://dash.cloudflare.com), open
   **Workers & Pages**. The account ID is shown in the panel on the right.
2. **Token.** Open **My Profile → API Tokens → Create Token** and use the template
   **Edit Cloudflare Workers**. Under account resources choose your account; under zone resources
   choose `muscaglar.com`. Copy the token: it is shown once.
3. **Give both to GitHub.** In the repository, open **Settings → Secrets and variables → Actions**.
   - On the **Variables** tab, add `CLOUDFLARE_ACCOUNT_ID` with the account ID.
   - On the **Secrets** tab, add `CLOUDFLARE_API_TOKEN` with the token.

   Or from a terminal:

   ```sh
   gh variable set CLOUDFLARE_ACCOUNT_ID --repo muscaglar/musCaglar.com --body "the account ID"
   gh secret set CLOUDFLARE_API_TOKEN --repo muscaglar/musCaglar.com      # paste the token when asked
   ```

4. **Publish once.** Push to `master`, or open **Actions → Site → Run workflow**. The first run
   creates the project `muscaglar` on Cloudflare. The site is then live at a `workers.dev`
   address, shown in the run's log and in the Cloudflare dashboard. Check it there before moving
   the domain.

Until the variable and the secret exist, the workflow still builds and checks the site. It just
does not publish.

### Moving the domain

Do this once the `workers.dev` address looks right. The old site goes offline at step 1 and the
new one appears at step 2, so do them together.

1. In the Cloudflare dashboard, open the domain `muscaglar.com`, then **DNS → Records**. Note down
   and then delete the records named `muscaglar.com` and `www`. They point at the old host.
2. Open **Workers & Pages → muscaglar → Settings → Domains & Routes → Add → Custom domain**. Add
   `muscaglar.com`, then add `www.muscaglar.com`. Cloudflare creates the new records itself.
3. Open the domain's **Rules → Redirect Rules** and create one rule that tidies up addresses:
   - When: hostname equals `www.muscaglar.com`, or the request is not over HTTPS and the hostname
     equals `muscaglar.com`.
   - Then: a dynamic redirect to `concat("https://muscaglar.com", http.request.uri.path)`, status
     301, keeping the query string.

> [!IMPORTANT]
> Change the records for `muscaglar.com` and `www` only. Every other address on the domain, such as
> `home.muscaglar.com`, must be left exactly as it is. For the same reason, avoid settings that
> apply to the whole domain (such as "Always Use HTTPS"; the redirect rule above does that job for
> the website alone), and do not add `includeSubDomains` to the `Strict-Transport-Security` header
> in `static/_headers`.

### Undoing a release

Open **Workers & Pages → muscaglar → Deployments** in the Cloudflare dashboard and choose
**Rollback** on the version to return to. Then revert the change on GitHub, so that the next push
does not publish it again.

### Headers and redirects

- `static/_headers` sets the security and caching headers.
- Old addresses are kept alive with `aliases` in a page's front matter. Hugo gathers them into one
  list (`_redirects`) that Cloudflare follows.
- The headers include a content security policy that allows pictures, styles and scripts from this
  site only. To embed something from elsewhere, such as a video, add its address to the policy in
  `static/_headers`.

## Checks

Every push and pull request builds the site twice, as it will be published and again with drafts
included, and stops when

- Hugo reports an error or a warning, or says that something used here is deprecated;
- a link, picture, stylesheet or script on the site is missing;
- a redirect leads nowhere;
- an original photograph, or a file with camera or location data, would be published;
- a page has no title or description.

To run the same checks before pushing:

```sh
scripts/build.sh && python3 scripts/check-site.py
```

To look at the built site with Cloudflare's headers and redirects applied:

```sh
python3 scripts/preview-built.py          # http://127.0.0.1:8788
```

## Setting up on a new machine

```sh
brew install hugo                  # macOS; see gohugo.io/installation for other systems
git clone https://github.com/muscaglar/musCaglar.com.git
cd musCaglar.com
hugo server -D
```

## Upgrading Hugo

The version that builds the live site is pinned, so that a new release of Hugo cannot change the
site unannounced. To move to a newer version:

1. `brew upgrade hugo`, then look at the site with `hugo server -D`.
2. In `scripts/build.sh`, write the new version number and the checksum of
   `hugo_extended_<version>_linux-amd64.tar.gz`. The checksums are in the `checksums.txt` file of
   each [Hugo release](https://github.com/gohugoio/hugo/releases).
3. Run the checks above, then push.
