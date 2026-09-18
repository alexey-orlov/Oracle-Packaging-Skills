#!/usr/bin/env bash
# render_probe.sh — what can render a .pptx on THIS machine, and how.
#
# Renderers differ per machine and break silently (a converter that answers
# --version can still produce nothing). This script only reports what exists
# and prints the recipe for it; it never assumes a renderer and never claims a
# tool works because it is installed.
#
#   render_probe.sh [--deck <file.pptx>] [--out <dir>] [--json] [--help]
#
# With --deck it also prints a ready-to-paste command line for the best
# available path. Nothing is rendered by this script.

set -u

DECK=""
OUTDIR="renders"
JSON=0

usage() {
  sed -n '2,14p' "$0" | sed 's/^# \{0,1\}//'
  cat <<'EOF'

Options:
  --deck <file.pptx>  deck to build the recipe for (optional)
  --out <dir>         output directory used in the printed recipe (default: renders)
  --json              machine-readable summary of what was found
  --help              this text
EOF
}

while [ $# -gt 0 ]; do
  case "$1" in
    --deck) DECK="${2:-}"; shift 2 ;;
    --out) OUTDIR="${2:-}"; shift 2 ;;
    --json) JSON=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

have() { command -v "$1" >/dev/null 2>&1 && echo "$1"; }

QL=$(have qlmanage)
SOFFICE=$(have soffice); [ -z "$SOFFICE" ] && SOFFICE=$(have libreoffice)
[ -z "$SOFFICE" ] && [ -x "/Applications/LibreOffice.app/Contents/MacOS/soffice" ] \
  && SOFFICE="/Applications/LibreOffice.app/Contents/MacOS/soffice"
PDFTOPPM=$(have pdftoppm)
PDFTOTEXT=$(have pdftotext)
NODE=$(have node)
PY=$(have python3)
MAGICK=$(have magick); [ -z "$MAGICK" ] && MAGICK=$(have convert)
TIMEOUT=$(have timeout); [ -z "$TIMEOUT" ] && TIMEOUT=$(have gtimeout)
PERL=$(have perl)

PIL="no"
if [ -n "$PY" ]; then
  "$PY" -c "import PIL" >/dev/null 2>&1 && PIL="yes"
fi

if [ "$JSON" = "1" ]; then
  printf '{\n'
  printf '  "qlmanage": "%s",\n' "${QL:-}"
  printf '  "soffice": "%s",\n' "${SOFFICE:-}"
  printf '  "pdftoppm": "%s",\n' "${PDFTOPPM:-}"
  printf '  "pdftotext": "%s",\n' "${PDFTOTEXT:-}"
  printf '  "node": "%s",\n' "${NODE:-}"
  printf '  "python3": "%s",\n' "${PY:-}"
  printf '  "pillow": "%s",\n' "$PIL"
  printf '  "imagemagick": "%s",\n' "${MAGICK:-}"
  printf '  "timeout": "%s"\n' "${TIMEOUT:-}"
  printf '}\n'
  exit 0
fi

echo "Renderers found"
echo "---------------"
printf '  %-14s %s\n' "qlmanage"    "${QL:-— not found (macOS only)}"
printf '  %-14s %s\n' "soffice"     "${SOFFICE:-— not found}"
printf '  %-14s %s\n' "pdftoppm"    "${PDFTOPPM:-— not found (poppler)}"
printf '  %-14s %s\n' "pdftotext"   "${PDFTOTEXT:-— not found (poppler)}"
printf '  %-14s %s\n' "node"        "${NODE:-— not found}"
printf '  %-14s %s\n' "python3"     "${PY:-— not found}"
printf '  %-14s %s\n' "Pillow"      "$PIL"
printf '  %-14s %s\n' "imagemagick" "${MAGICK:-— not found}"
printf '  %-14s %s\n' "timeout"     "${TIMEOUT:-— not installed; use: perl -e 'alarm N; exec @ARGV' ...}"
echo

D="${DECK:-<deck.pptx>}"

echo "How to render a contact sheet with what is here"
echo "----------------------------------------------"
n=0

if [ -n "$QL" ]; then
  n=$((n+1))
  cat <<EOF
$n. QuickLook, one slide at a time (macOS; fast, no converter needed)
   QuickLook renders only slide 1, so render slide N from a temp copy of the
   deck that keeps only that <p:sldId/> in ppt/presentation.xml and copies
   every other zip entry verbatim (ZIP_STORED). Delete docProps/thumbnail.* in
   the copy or QuickLook may serve Office's cached cover image instead.
     mkdir -p "$OUTDIR"
     ${TIMEOUT:-perl -e 'alarm 60; exec @ARGV'} ${TIMEOUT:+60} qlmanage -t -s 1600 -o "$OUTDIR" one-slide.pptx
   (-s = long edge in px; 2600 for close reading. Delete each temp file right
   after rendering — it is full deck size.)
   Caveats: brand fonts substitute unless installed; SVG images and some
   rounded-rect fills render blank. Trust geometry, not glyph widths.
EOF
fi

if [ -n "$SOFFICE" ]; then
  n=$((n+1))
  cat <<EOF
$n. LibreOffice headless -> PDF -> PNG
     "$SOFFICE" --headless --convert-to pdf --outdir "$OUTDIR" "$D"
     ${PDFTOPPM:+pdftoppm -r 110 -png "$OUTDIR/\$(basename "${D%.pptx}").pdf" "$OUTDIR/slide"}
   VERIFY, never trust the return code: ls "$OUTDIR" and check a PDF appeared.
   soffice can hang or exit non-zero with an empty outdir on some machines,
   and a stale instance silently swallows later runs:
     pgrep -f soffice.bin   # before blaming the tool
     pkill -x soffice; pkill -f soffice.bin   # after a guarded run
EOF
fi

if [ -n "$PDFTOPPM" ] && [ -z "$SOFFICE" ]; then
  n=$((n+1))
  cat <<EOF
$n. A PDF already exists (exported by hand): rasterise it
     pdftoppm -r 110 -png "<deck>.pdf" "$OUTDIR/slide"
     ${PDFTOTEXT:+pdftotext "<deck>.pdf" - | less   # content QA}
EOF
fi

if [ -n "$NODE" ]; then
  n=$((n+1))
  cat <<EOF
$n. node is available — usable only if a renderer package is already installed
   in this project (there is no bundled one). Check before relying on it:
     node -e "require.resolve('puppeteer')" 2>/dev/null && echo puppeteer present
EOF
fi

if [ "$n" = "0" ]; then
  cat <<EOF
   None found. Options:
     - open the .pptx in PowerPoint / Keynote / Google Slides and export images
     - install poppler (pdftoppm) and render an exported PDF
     - run the QA on a machine that has QuickLook or LibreOffice
   Do not report a deck as reviewed without a render.
EOF
fi

if [ "$PIL" = "yes" ]; then
  cat <<EOF

Contact sheet from the PNGs (Pillow):
   downscale each render to a fixed thumb width, paste on a grid, label each
   cell with its slide number, keep the sheet <= ~2400 px wide so it stays
   readable. ${MAGICK:+Or: $MAGICK montage "$OUTDIR"/*.png -tile 3x -geometry +6+6 "$OUTDIR/contact-sheet.png"}
EOF
elif [ -n "$MAGICK" ]; then
  cat <<EOF

Contact sheet:
   $MAGICK montage "$OUTDIR"/*.png -tile 3x -geometry +6+6 "$OUTDIR/contact-sheet.png"
EOF
fi

echo
echo "Reminder: the fit report in build_deck.py is the text-overflow check."
echo "A render proves layout and colour; it does not prove the brand font fits."
