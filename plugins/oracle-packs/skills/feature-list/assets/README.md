# Feature-list assets

There is no template file for this artifact. The feature list is a generated `.docx` — the
structure, geometry and brand tokens live in `../tools/build_feature_list.py` and are documented in
`../references/feature-list-anatomy.md`. A `.dotx` would add a binary to review and a second place
for the column widths to drift.

## Run it

```sh
python3 -m venv .venv
.venv/bin/pip install -r plugins/oracle-packs/requirements.txt

.venv/bin/python plugins/oracle-packs/skills/feature-list/tools/build_feature_list.py \
    packs/<slug>/pack-spec.yaml \
    --out packs/<slug>/artifacts
```

`--help` lists every option. Paths are arguments — nothing is hard-coded to one machine.

| Flag | Effect |
|---|---|
| *(default)* | Adds the `Tier first available` column when every feature carries `tier_first_available`. |
| `--tier-column` | Force the six-column layout even when some features have no tier. |
| `--no-tier-column` | Force the five-column reference layout. |

Writes `<slug>-feature-list.docx` into `--out`, and prints the area / category / feature counts and
the status split so a miscount is visible without opening the file.

## Dependencies

`PyYAML` and `python-docx`. No browser, no Word, no LibreOffice — the document is written directly
as Office Open XML. Fonts are not shipped: the document asks for **Arial**, which is present
wherever Word is.

## Test fixture

Both builders share one fixture, in the one-pager skill:

```sh
.venv/bin/python plugins/oracle-packs/skills/feature-list/tools/build_feature_list.py \
    plugins/oracle-packs/skills/one-pager/tests/fixture-pack-spec.yaml --out /tmp/fl-check
```

It is an anonymized Workforce Optimization spec — no customer name, statuses arranged to exercise
all three glyphs, and two features carrying notes so the footnote markers are exercised too.
Expected: 4 areas / 13 categories / 38 features, 6 columns, 19 available · 6 partial · 13 roadmap.

## Done means

1. **It builds**, exit 0, with the counts matching the spec's capability tree.
2. **No pricing.** Exit 2 means a price reached the document; the feature list never carries one.
3. **Opened in Word**, not only rendered in a previewer. Check: the Area and Category columns read
   as continuous merged blocks; the header row repeats on page 2 and after; no feature name is
   truncated; the three glyphs are distinguishable; every footnote marker has its line.
4. **Statuses re-checked against the product**, not against the last version of this document.
   Feature lists rot faster than any other artifact in the pack, and a stale `available` is the one
   error that reaches a customer as a promise.
5. **Reviewed by the owner** against the spec, then delivered.

## A note on YAML

`capabilities[]` is long and is usually written in YAML flow style (`- { name: ..., status: ... }`).
An **unquoted flow value containing a comma is silently truncated at the comma** — `name: Dispatcher
UI (map, table views)` becomes `Dispatcher UI (map`, with no error. Quote any feature name
containing a comma, a colon or a brace. This bit the fixture during the build of this tool; the
symptom is a feature name that looks fine in the spec and arrives half-length in the document.
