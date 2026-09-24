# Pictures in the pack — where they may come from, and what is recorded

_The sources a pack's icons and photographs may be taken from, the licences that are allowed, how each file is prepared, and what is written down about it. Governs the `visuals` skill and anything else that puts a picture into a deck, a one-pager or the mini-site. Rewritten to current truth — never appended with dated updates._

A pack's artifacts go to Oracle sellers, to customers and onto a public site. A picture in one of them is a commercial use of someone else's work, and the only defence is that the licence permitted it and the record proves which licence that was. So two rules stand above the rest:

1. **Only licences that permit commercial use without a credit line.** Not because credit is shameful, but because a sales deck will not carry one, and a licence whose condition the artifact silently breaks is worse than no picture.
2. **Every file keeps a record**: source page, creator, licence, date. Including files whose licence asks for nothing. The record is what lets anyone re-check the right to use a picture a year later, when the run that found it is long gone.

---

## 1. Photographs

### Allowed sources

| Source | Licence it yields | Key needed | What it is actually good for |
|---|---|---|---|
| **Openverse** (`api.openverse.org`) restricted to `cc0` and `pdm` | CC0 1.0, Public Domain Mark | No | Machinery, vehicles, infrastructure, control rooms, industrial and archival scenes. Its public-domain pool is Wikimedia, museum and government-archive material, so it is **thin on contemporary office and knowledge-work photography** — expect little for "a person at a screen", and say so rather than accepting a 1950s picture for a 2026 deck. |
| **Pexels** (`api.pexels.com`) | Pexels License | Yes — the environment variable `PEXELS_API_KEY`, or on a Mac the Keychain entry of that name (free at pexels.com/api) | Modern working life: people at desks, in warehouses, in vans, on screens. This is the source that makes the today → tomorrow pair work. |
| **Unsplash** (`api.unsplash.com`) | Unsplash License | Yes — the environment variable `UNSPLASH_ACCESS_KEY`, or on a Mac the Keychain entry of that name. The public search endpoint answers `401` without one, so there is no key-free route. | The same ground as Pexels, different photographers. |

Both the Pexels and the Unsplash licences allow commercial use and ask for no attribution; the record is kept anyway.

### Never

- **A search-engine image result.** The result page carries no licence, and the thumbnail is not the licence of the page it came from.
- **Getty, Shutterstock, Adobe Stock, iStock, Alamy** — including watermark-free previews and "free trial" downloads.
- **CC-BY, CC-BY-SA, CC-BY-NC, or any licence with a condition the artifact will not print.** CC-BY obliges a visible credit; a deck will not carry one, so a CC-BY picture is not usable, however good it is.
- **A file whose licence nobody recorded.** No record, no use.
- **A generated picture** standing in for a real one, and no picture of a different industry "because it looks similar".

### Choosing well

- **Landscape, at least 1600 px wide, no text or watermark inside the picture.** Deck frames are wide; a portrait crops to nothing, and baked-in text cannot be translated or corrected.
- **Identifiable people are a decision.** Prefer pictures where nobody's face reads as endorsing the product. A public-domain press photograph of named individuals is legally usable and still wrong for a sales slide.
- **The two today → tomorrow photographs are one pair.** Same era, same register, both landscape. An archive photograph opposite a modern one reads as a joke rather than a contrast.
- **`cover` (the title slide's photograph: the industry at work, wide, no text), `today` is the pain in the current way of working** — the desk, the paperwork, the manual step; never a picture of software. **`tomorrow` is the person using the solution** — the plan reviewed, the decision made.

### Searching Openverse

Its full-text search is strict: every word must appear, so a five-word description of a scene returns nothing while its first two words return hundreds. Search with **one to three broad words** and let the tool's ladder drop the trailing word until it answers; the record keeps the query that actually found each file.

---

## 2. Icons

| Set | Licence | How it is fetched |
|---|---|---|
| **Tabler Icons** — primary | MIT | `https://cdn.jsdelivr.net/npm/@tabler/icons-png/icons/outline/<name>.png` (240 px, already black on transparent), or the SVG at `https://raw.githubusercontent.com/tabler/tabler-icons/main/icons/outline/<name>.svg` |
| **Lucide** — fallback | ISC | `https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/<name>.svg` |

**Never a CC-BY icon set** (it would put an attribution line on the slide) and **never a vendor's logo used as an icon** — a logo is a trade mark with its own clearance rules, which live in `naming-and-clearance.md`.

### Rendering the SVG

`plugins/oracle-packs/skills/visuals/tools/fetch_icon.py` tries three rasterizers in order and uses the first that renders: QuickLook on a Mac, then `rsvg-convert` (librsvg) on PATH, then the `cairosvg` Python module. With none of them the icon is **deferred**, and the message names all three.

```sh
qlmanage -t -s 1024 -o <dir> <file.svg>              # macOS: -> <dir>/<file>.svg.png, square, on opaque white
rsvg-convert -w 1024 -h 1024 -o <out.png> <file.svg>  # elsewhere: transparent ground
```

Two traps, both handled by the tool and both worth knowing:

1. **QuickLook honours the SVG's own `width`/`height`.** Tabler and Lucide declare `width="24" height="24"`, so a render asked for 1024 px comes back with a 70 px glyph in the corner of a 1024 px canvas. Rewrite `width` and `height` to the target size before rendering — the `viewBox` is left alone, so stroke weights scale with it.
2. **QuickLook's render is opaque white behind black strokes.** The alpha channel is rebuilt as `255 − luminance` (the other two keep their transparency), then filled: **white** for the deck's dark panels, **ink `#26282B`** for light grounds. Both renders are kept — an icon that reads on one ground and not the other is a bad choice a single preview would hide.

The PNG package is preferred where the wanted size is 240 px or less; above that the SVG route wins, because upscaling a 240 px bitmap softens the strokes.

### One family

All icons in a pack come from one set, at one weight, prepared the same way. Four icons in a row on the industries slide show any mismatch immediately — peers share geometry (`slide-design.md`, rule 2).

---

## 3. The shared icon library

`shared/data/icons/` holds the icons every artifact reuses, so an industry looks the same in the deck, the one-pager and the site. `map.yaml` is its index: a top-level `fallback:` and an `icons:` list of `{file, depicts, source, license, keywords}` rows, under a comment header that states the house style.

- **Added to, never rewritten.** A name already there is left exactly as it is; a new icon is a new name. Three artifacts read this library, and replacing a file changes all of them at once.
- **The row is appended as text**, not written by re-serializing the file: a `yaml.safe_dump` round-trip deletes the comment header that explains the house style.
- **House style**: white line art on a transparent ground, matching what is already in there. An icon that does not match does not belong.

---

## 4. The customer's logo

The delivered customer's own mark is the one picture here that is **not** found — it is given. The `customer_logo` slot is of kind `supplied`: the owner hands over a file from the engagement materials, and nothing else is accepted.

- **Never searched for, on any source.** A company's mark is a trademark, not an openly licensed picture, and a copy lifted off a search result or a brand-resources page carries no right to use it. None of the licences above applies to it, so the licence gate does not run.
- **What permits the use is the clearance, not a licence.** The logo is asked for only where `clearance.customer_name_allowed` is true for some audience, and the record says, in those words, that it is used under the customer's clearance recorded in the pack brief. Clearance is revocable: a logo already in a pack goes out again when it is withdrawn.
- **No stand-in.** Not a lookalike, not a redrawn version, not an industry icon in its place. With no file, the deck removes the slot and moves the headline — an explicit absence, which is the standing rule.
- Recorded through `apply_choice.py` like every other picture, so the file, its brief entry and the decision move together.

---

## 5. What is recorded, and where

Every candidate downloaded carries a `.json` sidecar beside it, in the work folder. When the owner picks one, `apply_choice.py` copies its provenance onto the picture's entry in the pack brief, which is its only record in the repo:

| Field | Why |
|---|---|
| file | which picture this is about |
| slot | where it is used |
| source | the library it came from |
| creator | the photographer or the set |
| licence | the exact licence, by name |
| page | the page a human can open to check |

A picture whose entry lacks these is not in the pack; the date it was chosen is in the decisions log. This is also what makes a later question — "can we still use this on the public site?" — answerable in a minute instead of a morning.

---

## 6. When a source cannot be reached

A network failure, a missing key or a rate limit is **deferred**, never "nothing found". The second closes the item forever on the strength of a timeout, and a slot silently marked hopeless never gets its picture. Say which source, what it needs, and that the picture is still open — then retry. The tools encode this: exit code 3 means deferred, and a search whose only answering source came back empty while others were unreachable also exits 3 rather than pretending the world is empty.
