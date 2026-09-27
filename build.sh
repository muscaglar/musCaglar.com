#!/usr/bin/env bash

# Builds the site on Cloudflare. Locally, just run `hugo` (or `hugo server` to preview).

set -euo pipefail

# The version of Hugo used to build the live site, and the checksum of its download. Keep them in
# step with .github/workflows/build.yml. To move to a newer Hugo, change both values in both files
# (the checksums are listed on https://github.com/gohugoio/hugo/releases).
HUGO_VERSION=0.166.0
HUGO_SHA256=0e39b901e3f919f1daae05c8ff64f0c14c8a348ef46886d63f8e6d1bb2653885

export TZ=Europe/London
export HUGO_CACHEDIR="${PWD}/.cache/hugo"

cleanup() {
  if [[ -n "${build_temp_dir:-}" && -d "${build_temp_dir}" ]]; then
    rm -rf "${build_temp_dir}"
  fi
}
trap cleanup EXIT SIGINT SIGTERM

main() {
  build_temp_dir=$(mktemp -d)

  local archive="hugo_extended_${HUGO_VERSION}_linux-amd64.tar.gz"
  echo "Installing Hugo ${HUGO_VERSION}..."
  curl -sfL --retry 3 --output-dir "${build_temp_dir}" -O \
    "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/${archive}"
  echo "${HUGO_SHA256}  ${build_temp_dir}/${archive}" | sha256sum --check --strict
  mkdir -p "${HOME}/.local/hugo"
  tar -C "${HOME}/.local/hugo" -xf "${build_temp_dir}/${archive}" hugo
  export PATH="${HOME}/.local/hugo:${PATH}"
  hugo version

  hugo build --gc --minify
}

main "$@"
