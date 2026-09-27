# muscaglar.com

My personal website: projects, photographs, short updates and a CV.

The site is a folder of plain text files. [Hugo](https://gohugo.io) turns them into web pages, and
Cloudflare publishes them whenever a change reaches GitHub. There is no database, no JavaScript
framework and nothing to install besides Hugo itself.

- [Day to day](#day-to-day)
- [Where things are](#where-things-are)
- [Writing](#writing)
- [Photographs](#photographs)
- [Publishing](#publishing)
- [Checks](#checks)
- [Setting up on a new machine](#setting-up-on-a-new-machine)
- [Upgrading Hugo](#upgrading-hugo)

## Day to day

| I want to… | Do this |
|---|---|
| See the site while I work | `hugo server -D` and open <http://localhost:1313>. The page reloads as files are saved. `-D` also shows drafts. |
| Post an update | `hugo new content updates/2026-10-01-a-title.md`, write below the dashes, save. |
| Add a project | `hugo new content projects/a-title`. This makes a folder with an `index.md`; pictures go in the same folder. |
| Add photographs | `hugo new content photos/an-album`, then drop the pictures into the new folder. |
| Change the CV | Edit `data/cv.yaml`. The top of the file explains the layout. |
| Change the text on the home page | Edit `intro` in `content/_index.md`. |
| Change the About page | Edit `content/about.md`. |
| Change the links in the footer, or the menu | Edit `hugo.toml`. |
| Keep something unpublished | Leave `draft: true` in its front matter. Delete the line to publish. |
| Publish | Commit and push to `master`. The live site updates about a minute later. |
| Try a change before it goes live | Push it to another branch. Cloudflare builds a preview with its own address. |

New files made with `hugo new content` start as drafts.

## Where things are

```text
content/            Everything that is written: one file or folder per page
  _index.md           the home page
  about.md            the About page
  cv.md               the CV page (its content comes from data/cv.yaml)
  projects/           one folder per project
  photos/             one folder per album
  updates/            one file per update
data/cv.yaml        The CV
hugo.toml           Settings: site title, menu, links, picture quality
layouts/            The HTML templates
assets/css/         The stylesheets (design tokens are in tokens.css)
assets/js/          Small scripts: theme switch, photo viewer
static/             Files published exactly as they are (_headers sets Cloudflare's headers)
archetypes/         The starting text of new files made with `hugo new content`
scripts/            The checker that runs on every push
build.sh            How Cloudflare builds the site
wrangler.jsonc      How Cloudflare serves the site
.github/workflows/  The checks that run on GitHub
```

## Writing

Pages are written in Markdown. The block between the `---` lines at the top of a file is its front
matter: the title, the date and other details.

### An update

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
period: "March – June 2026"    # optional: shown instead of the date
summary: "One or two sentences, shown in lists and link previews."
kind: tinkering                # research or tinkering
tags: [Python]
cover: picture.jpg             # optional: used in lists and link previews
featured: true                 # optional: show on the home page
links:
  - name: Code on GitHub
    url: https://github.com/muscaglar/example
aliases:                       # optional: old addresses that should lead here
  - /an-old-address
---

The write-up.
```

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

**Privacy.** The original files are never published. Visitors get resized copies, which carry no
camera or location data. The check that runs on every push fails if an original photograph, or any
file with such data in it, is about to be published.

`content/photos/sample-album/` holds placeholder pictures that show how an album looks. It is a
draft, so it is never published; delete the folder when it is no longer useful.

## Publishing

The site is served by Cloudflare. Whenever `master` changes on GitHub, Cloudflare runs `build.sh`
and publishes the result. Other branches are built as previews with their own address, which
Cloudflare posts as a comment on the pull request.

### First-time set-up

1. In the [Cloudflare dashboard](https://dash.cloudflare.com), open **Workers & Pages**, choose
   **Create application**, then **Import a repository**.
2. Connect the GitHub account, and allow access to the `musCaglar.com` repository only.
3. Name the project **`muscaglar`**. It must match `name` in `wrangler.jsonc`.
4. Leave the build command empty and the deploy command as `npx wrangler deploy`.
   Under the advanced settings, add the variable `SKIP_DEPENDENCY_INSTALL` with the value `true`.
5. Press **Deploy**. When the build finishes, the site is live at a `workers.dev` address.
   Check it there before moving the domain.
6. To build previews of other branches, open the project's **Settings → Builds** and switch on
   builds for non-production branches, with `npx wrangler versions upload` as their deploy command.

### Moving the domain

Do this once the `workers.dev` address looks right.

1. In the project, open **Settings → Domains & Routes → Add → Custom domain** and enter
   `muscaglar.com`. Cloudflare offers to replace the existing DNS record that points at the old
   host; accept. Repeat for `www.muscaglar.com`.
2. To send `www` to the bare domain, open the domain's **Rules → Redirect Rules** and create a rule:
   when the hostname equals `www.muscaglar.com`, redirect to
   `concat("https://muscaglar.com", http.request.uri.path)` with status 301.

> [!IMPORTANT]
> Change the records for `muscaglar.com` and `www` only. Other addresses on the domain, such as
> `home.muscaglar.com`, must be left exactly as they are. For the same reason, avoid settings that
> apply to the whole domain, and do not add `includeSubDomains` to the `Strict-Transport-Security`
> header in `static/_headers`.

### Undoing a release

Open the project in the Cloudflare dashboard, go to **Deployments**, and choose **Rollback** on the
version to return to. Then fix or revert the change on GitHub, so that the next push does not
publish it again.

### Headers and redirects

- `static/_headers` sets the security and caching headers.
- Old addresses are kept alive with `aliases` in a page's front matter. Hugo gathers them into one
  list (`_redirects`) that Cloudflare follows.
- The headers include a content security policy that allows pictures, styles and scripts from this
  site only. To embed something from elsewhere, such as a video, add its address to the policy in
  `static/_headers`.

## Checks

Every push and pull request runs `.github/workflows/build.yml` on GitHub. It builds the site twice,
as it will be published and again with drafts included, and fails when

- Hugo reports an error or a warning;
- a link, picture, stylesheet or script on the site is missing;
- a redirect leads nowhere;
- an original photograph, or a file with camera or location data, would be published;
- a page has no title or description.

To run the same checks before pushing:

```sh
hugo build --gc --minify --panicOnWarning && python3 scripts/check-site.py
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

1. `brew upgrade hugo`, then check the site with `hugo server -D` and run the checks above.
2. Write the new version number and the checksum of `hugo_extended_<version>_linux-amd64.tar.gz`
   into both `build.sh` and `.github/workflows/build.yml`. The checksums are in the
   `checksums.txt` file of each [Hugo release](https://github.com/gohugoio/hugo/releases).
