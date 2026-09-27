#!/usr/bin/env bash

# Builds the site with the version of Hugo it was made for.
#
#   scripts/build.sh                     the site as it is published, into ./public
#   scripts/build.sh --buildDrafts       extra arguments are handed to `hugo build`
#
# GitHub runs this on every push. On your own machine `hugo server -D` is the everyday preview;
# run this script when you want exactly what will be published.

set -euo pipefail

# The Hugo version, and the checksum of its Linux download. This is the only place they are
# written down. To move to a newer Hugo see "Upgrading Hugo" in README.md.
HUGO_VERSION="0.166.0"
HUGO_SHA256_LINUX_AMD64="0e39b901e3f919f1daae05c8ff64f0c14c8a348ef46886d63f8e6d1bb2653885"

export TZ="${TZ:-Europe/London}"

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${root}"

say() { printf 'build: %s\n' "$*" >&2; }

right_hugo_installed() {
  command -v hugo >/dev/null 2>&1 && hugo version | grep -q "hugo v${HUGO_VERSION}[+-]"
}

install_hugo() {
  if [[ "$(uname -s)" != "Linux" || "$(uname -m)" != "x86_64" ]]; then
    say "Hugo ${HUGO_VERSION} is needed; this machine has: $(hugo version 2>/dev/null | cut -d' ' -f2 || echo none)."
    say "Install it (on a Mac: brew install hugo, or brew upgrade hugo), or change HUGO_VERSION in scripts/build.sh."
    exit 1
  fi
  local archive="hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
  local folder="${HOME}/.local/hugo-${HUGO_VERSION}"
  local temp
  temp="$(mktemp -d)"
  say "Downloading Hugo ${HUGO_VERSION}"
  curl --fail --silent --show-error --location --retry 3 --output "${temp}/${archive}" \
    "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/${archive}"
  if ! echo "${HUGO_SHA256_LINUX_AMD64}  ${temp}/${archive}" | sha256sum --check --status; then
    say "The download does not match its checksum. Stopping."
    rm -rf "${temp}"
    exit 1
  fi
  mkdir -p "${folder}"
  tar -C "${folder}" -xzf "${temp}/${archive}" hugo
  rm -rf "${temp}"
  export PATH="${folder}:${PATH}"
}

right_hugo_installed || install_hugo
hugo version >&2

# Pictures that were processed by an earlier build are kept here and reused.
export HUGO_CACHEDIR="${HUGO_CACHEDIR:-${root}/.cache/hugo}"

log="$(mktemp)"
trap 'rm -f "${log}"' EXIT

# Warnings stop the build. Notices that something in the templates will stop working in a later
# Hugo are printed at a quieter level, so they are looked for separately.
hugo build --gc --minify --cleanDestinationDir --panicOnWarning --logLevel info "$@" 2>&1 | tee "${log}"
if grep -qi "deprecated" "${log}"; then
  say "Hugo says something used here is deprecated (see above). Fix it before publishing."
  exit 1
fi
