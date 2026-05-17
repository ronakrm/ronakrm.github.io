#!/usr/bin/env bash
# Build header.tex -> header.png at 1100x220.
# Usage:  ./build.sh           (builds header.tex)
#         ./build.sh foo.tex   (builds foo.tex -> foo.png)
set -euo pipefail

cd "$(dirname "$0")"

src="${1:-header.tex}"
stem="${src%.tex}"

pdflatex -interaction=nonstopmode "$src" > /dev/null
pdftocairo -png -scale-to-x 1100 -scale-to-y 220 "${stem}.pdf" "$stem"
mv -f "${stem}-1.png" "${stem}.png"

rm -f "${stem}.aux" "${stem}.log"

echo "wrote ${stem}.png"
