# One-pager assets

`one-pager-template.html` — the sales one-pager, with the anatomy and CSS of the Workforce
Optimization build source (2026-07-17) and the content replaced by tokens. Rendered by
`../tools/build_one_pager.py`. Block order, word budgets, CSS tokens and print rules:
`../references/one-pager-anatomy.md`.

## Run it

```sh
python3 -m venv .venv
.venv/bin/pip install -r plugins/oracle-packs/requirements.txt

.venv/bin/python plugins/oracle-packs/skills/one-pager/tools/build_one_pager.py \
    packs/<slug>/pack-spec.yaml \
    --out packs/<slug>/artifacts \
    --channel partner_print \
    --hero /path/to/approved-hero.jpg          # optional
```

`--help` lists every option. Paths are arguments — nothing is hard-coded to one machine.

| Flag | Effect |
|---|---|
| `--channel partner_print` | Default. External name variant + subheading, `contacts.partner_print`. |
| `--channel internal` | `meta.name_variants.internal_slide`, `contacts.internal`. |
| `--hero <image>` | Embedded as a `data:` URI. Omitted, the hero renders with no photo and the one-liner widens. |
| `--no-pdf` | Write the HTML and the word-budget table; skip Chrome. Fast, but proves nothing. |
| `--template <file>` | Render a variant template instead of this one. |

Outputs `<slug>-one-pager-<channel>.html` and `.pdf` into `--out`. The HTML is kept on purpose: it
is the editable source, and the PDF is a render of it.

## Dependencies

`PyYAML`, `pypdf`, and **Google Chrome or Chromium** for the PDF. The browser is found via
`$CHROME_BIN`, then the macOS default application path, then `google-chrome` / `chromium` on PATH.
Nothing else is required and nothing is fetched at render time.

## Hero images

**None ship with this plugin** — approved photography is licensed, and licensed images do not
belong in a Git repository. The owner keeps the cleared hero images for each pack in the pack's own
folder on the practice's shared drive (`Projects/Oracle/Packs/<pack>/`), and passes one with `--hero`.
Without `--hero` the page renders correctly on the plain dark hero — it is a supported state, not a
degraded one.

The same applies to a customer logo in the proof strip: it is passed through
`one_pager.proof_logo` in the spec and is only used when `clearance.customer_name_allowed` is true
for the channel being built.

## Fonts

None are shipped. The page asks for `"Helvetica Neue", Arial, sans-serif` — present on macOS and
Windows respectively — and the layout tolerates the substitution. Do not add an `@font-face` or a
Google Fonts link: the artifact is mailed around and must render identically offline.

## Done means

1. **One A4 page.** `build_one_pager.py` exits 0 and prints `1 page, 594.96 x 841.92 pt`. Exit 3
   means it is longer; cut content and rebuild. Do not shrink the type or the margins.
2. **Clearance clean.** Exit 2 means a name this channel may not carry reached the page.
3. **Every block inside its word budget**, or a deliberate, stated exception. The tool prints the
   table after a successful build.
4. **Looked at, not just counted.** Open the PDF. Check: the CTA contact block is fully on the page;
   no tier scope line has orphaned a single word; the capability glyphs read left to right as an
   increasing ladder; every figure has its footnote; the proof attribution matches the channel.
5. **Reviewed by the owner** against the spec, then delivered — the HTML alongside the PDF.
