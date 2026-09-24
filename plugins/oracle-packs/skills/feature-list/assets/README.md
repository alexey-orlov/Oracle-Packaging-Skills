# Feature-list assets

There is no template file for this artifact. The feature list is a generated `.docx` — the
structure, geometry and brand tokens live in `../tools/build_feature_list.py` and are documented in
`../references/feature-list-anatomy.md`. A `.dotx` would add a binary to review and a second place
for the column widths to drift.

## The wordmark

| File | What it is |
|---|---|
| `softserve-wordmark-ink.png` | What the document embeds: the SoftServe wordmark in ink, trimmed to its bounding box on white, ~2400 px wide. `run.add_picture(..., width=Inches(1.0))` places it. |
| `softserve-wordmark-ink.svg` | The source, copied from the practice mini-site (`site/assets/img/brand/softserve-wordmark-ink.svg`) so the provenance of the PNG is in the repo. |

**To regenerate** (no SVG rasterizer is installed on the owner's Mac — QuickLook does the work):

```sh
qlmanage -t -s 2400 -o <tmp> softserve-wordmark-ink.svg      # → <tmp>/softserve-wordmark-ink.svg.png
# QuickLook pads the render into a square; crop it back to the mark and keep a white ground:
shared/tools/py - <<'PY'
from PIL import Image, ImageChops, ImageOps
im = Image.open("<tmp>/softserve-wordmark-ink.svg.png").convert("RGB")
box = ImageChops.invert(im).getbbox()                         # the ink's own bounding box
im.crop(box).save("softserve-wordmark-ink.png")
PY
```

Keep it at least 1200 px wide: it is placed at 1.0 in, so anything smaller softens in print. If the
file is ever missing the build does not silently drop the brand — it falls back to the word
"SoftServe" set in the body face and says so on stderr.

## Fonts

The document asks for **Azurio** (the title) and **Replica LL TT** (everything else), the mini-site's
two faces. They ship privately in the plugin's `fonts/` folder, for practice members only (see the
README there); on the owner's Mac they are also installed in `/Library/Fonts/Managed/`. The
document names the faces and never embeds the files.

The three status glyphs are set in a third face, **Apple Symbols**
(`/System/Library/Fonts/Apple Symbols.ttf`). Neither brand face carries U+25CF / U+25D0 / U+25CB, so
without this the renderer picks a different substitute per glyph and they come out at different
sizes. Apple Symbols draws all three within 4% of each other. Where it is absent the estimator
measures the glyphs with Segoe UI Symbol (Windows) or DejaVu Sans (Linux) instead — the document
still names Apple Symbols, with Segoe UI Symbol as its `altName` — and where none of the three is
there the build falls back to per-glyph point sizes that look equal (● and ○ at 1.15× ◐) and says
so on stderr.

The builder writes an `altName` for each face into `word/fontTable.xml` after saving — Azurio →
Georgia, Replica LL TT → Arial, Apple Symbols → Segoe UI Symbol — so a machine without them
substitutes something sane instead of letting Word guess. The same font files are what make the one-page estimate exact: the height
estimator measures text with the brand face through Pillow — the plugin's `fonts/` copy first, then
the installed font folders — and falls back to an average glyph width (saying so on stderr) when it
finds neither.

## Run it

```sh
shared/tools/py plugins/oracle-packs/skills/feature-list/tools/build_feature_list.py \
    <repo>/packs/<slug>/pack-spec.md \
    --out <work>/artifacts
```

`shared/tools/py` runs it with an interpreter that has the packages, provisioning one on first use;
`shared/tools/py --check` shows which. `<repo>` and `<work>` are what
`shared/tools/py shared/tools/pack_paths.py <slug>` prints: the spec is read from the
packaging-skills repo, and the document is written to the local work folder, never the repo.

`--help` lists every option. Paths are arguments — nothing is hard-coded to one machine.

| Flag | Effect |
|---|---|
| *(default)* | Adds the `Tier first available` column when every feature carries `tier_first_available`. |
| `--tier-column` | Force the six-column layout even when some features have no tier. |
| `--no-tier-column` | Force the five-column reference layout. |
| `--fit one-page` *(default)* | Walk the fit ladder and guarantee one A4 page: a row per feature at 7.5pt → 7pt → compact (a row per category, features inline, status and tier columns dropped) at 7.5pt → 7pt. |
| `--fit none` | One row per feature at 7.5pt over as many pages as it takes, header row repeating. |
| `--check-pages` / `--no-check-pages` | Verify the real page count by exporting to PDF — Pages.app on macOS, else LibreOffice (`soffice --headless`), counted with pypdf (default: on wherever either is installed; hard 90- and 120-second limits). The report names the renderer that verified the count; a count nobody could verify is a `WARNING: page count NOT verified` line, never an error. |

Writes `<slug>-feature-list.docx` into `--out`, with the spec stamp (`shared/tools/spec_stamp.py`)
in its identifier property, and prints the stamp, the area / category / feature counts, the
status split, the layout it used and the estimated fill — so a miscount or an unexpectedly tight
page is visible without opening the file.

| Exit | Meaning |
|---|---|
| 0 | written |
| 1 | usage or spec error |
| 2 | a pricing figure reached the page, which the feature list must never carry |
| **3** | **the capability tree does not fit one A4 page even in compact mode at 7pt.** Nothing is written. The report names the counts, the largest areas and categories, and what to group. Take it to the owner: merge sibling features, fold small categories, shorten names — then fix the tree in the spec and rebuild. Never answer this with smaller type. |

## Dependencies

`PyYAML` and `python-docx`; `Pillow` is optional and only makes the one-page estimate exact. No
browser and no Word — the document is written directly as Office Open XML. Pages.app or
LibreOffice is used only to confirm the page count, and only when one is there; with neither, the
report says so in a `WARNING` line.

## Test fixture

Both builders share one fixture, in the one-pager skill:

```sh
shared/tools/py plugins/oracle-packs/skills/feature-list/tools/build_feature_list.py \
    plugins/oracle-packs/skills/one-pager/tests/fixture-pack-spec.md --out /tmp/fl-check
```

It is an anonymized Workforce Optimization spec and never ships as the real one — no customer
name (every channel attributes to the anonymized descriptor), statuses arranged to exercise all
three glyphs rather than the delivered pack's real ones, prices and figures kept from the July 2026
reference artifacts only for realistic geometry, and two features carrying notes so the footnote
markers are exercised too.
Expected: 4 areas / 13 categories / 38 features, 19 available · 6 partial · 13 roadmap. At 38
features it does not fit one row per feature, so it lands on compact mode at 7.5pt (about two
thirds of the page) — itself a demonstration that 38 features is a tree past its size.

## Done means

1. **It builds**, exit 0, with the counts matching the spec's capability tree.
2. **One page.** The build printed the layout and the estimated fill, and — where Pages or
   LibreOffice is installed — verified the real page count, naming which one did. An exit 3 is not a build to be worked around; it is a
   question for the owner about grouping.
3. **No pricing.** Exit 2 means a price reached the document; the feature list never carries one.
4. **The brand is right**: the wordmark lockup with `Oracle AI & Data Solutions` at the top, the
   title in Azurio, everything else in Replica LL TT, and the two intro lines — the approved
   one-liner, then who it is for. **Nothing in the page footer**: the spec version and build date
   are in the file's properties (File > Properties), which the build fills in on every run.
   The three status glyphs are the same size — three shapes, one size.
5. **Footnotes are caveats**: at most three, each the caveat alone in 15 words or fewer, never the
   feature name or a description repeated back. The build warns on stderr when the list drifts.
6. **Opened in Word**, not only rendered in a previewer. Check: the Area and Category columns read
   as continuous merged blocks; no feature name is truncated; the three glyphs are distinguishable;
   every footnote marker has its line. (QuickLook does not honour vertical merges — continuation
   cells looking separate there is the previewer, not the file.)
7. **Statuses re-checked against the product**, not against the last version of this document.
   Feature lists rot faster than any other artifact in the pack, and a stale `available` is the one
   error that reaches a customer as a promise.
8. **Reviewed by the owner** against the spec, then delivered.

## The capability table in the spec

In `pack-spec.md` the capabilities are one table per area, a row per feature with its category
first, and values go in through `shared/tools/packspec.py set` rather than by editing cells. A spec
converted from YAML can still carry the old flow-style damage — an unquoted value split at its
commas, so `name: Dispatcher UI (map, table views)` read as `Dispatcher UI (map` plus a junk key —
which the Markdown shows as an extra column. It bit this tool's fixture while it was built;
`lint_spec.py` warns (SPEC024) naming the key.
