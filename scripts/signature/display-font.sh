#!/usr/bin/env bash

# Cuts the typeface of the headings out of Special Gothic: one weight, one width, and only the
# letters a heading is likely to need. The result is a quarter of the size of the whole typeface.
#
#   scripts/signature/display-font.sh path/to/SpecialGothic.ttf
#
# Needs hb-subset (brew install harfbuzz) and woff2_compress (brew install woff2).
# The typeface is free to download from https://fonts.google.com/specimen/Special+Gothic

set -euo pipefail

font="${1:?Give the path of SpecialGothic.ttf}"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "${work}"' EXIT

# Semi-bold and condensed. The letters of the European languages written in Latin script, dashes,
# quotes and arrows.
hb-subset \
  --variations="wght=600,wdth=75" \
  --unicodes="20-7E,A0-17F,2013-2014,2018-2019,201C-201D,2022,2026,20AC,2122,2190-2193,2212" \
  --layout-features="kern,liga,calt,ccmp,locl,mark,mkmk" \
  --output-file="${work}/special-gothic-condensed-600.ttf" \
  "${font}"
woff2_compress "${work}/special-gothic-condensed-600.ttf" >/dev/null
cp "${work}/special-gothic-condensed-600.woff2" "${root}/assets/fonts/"
ls -l "${root}/assets/fonts/special-gothic-condensed-600.woff2"
