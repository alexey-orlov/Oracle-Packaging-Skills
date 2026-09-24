# Visuals assets and tools

There is no template file for this step. It produces no document of its own: it puts candidate
pictures in front of the owner, and writes what they chose into the pack. What lives here is the
tool set and the keyword table behind it.

The rules the tools enforce — which sources, which licences, what is recorded — are in
`shared/references/visual-assets.md`, and are not restated here. The one thing worth repeating: a
picture with no recorded licence does not go into a pack, and a source that could not be reached is
**deferred**, never "nothing found".

## The tools

| Tool | What it does |
|---|---|
| `../tools/suggest_icons.py "<industry>"` | Maps an industry name to three candidate icon names through `../references/icon-keywords.yaml`. Downloads nothing (unless `--describe`, which fetches each icon's own tag list). `--context "<the 'what matters here' line>"` sharpens the match; the industry's own name still decides. |
| `../tools/fetch_icon.py <name> --out <dir>` | Fetches one icon and renders it twice — white for the deck's dark panels, ink `#26282B` for light grounds — as 512 px PNGs on a transparent ground, with a `.json` sidecar. `--set lucide` for the fallback set, `--color white|ink|both`, `--size`. |
| `../tools/search_photos.py "<terms>" --out <dir>` | Downloads up to `--n` photograph candidates with a provenance sidecar each. `--source auto` tries the modern libraries first and falls back to the archival one; `--slot`, `--min-width` (default 1600), `--orientation`. |
| `../tools/contact_sheet.py <dir> --out <sheet.png>` | One labelled sheet, a row per slot, candidates lettered across it, each with creator · source · licence. Icons are drawn on both grounds in one cell. At most 2400 px wide. |
| `../tools/apply_choice.py <spec> --slot <slot> --file <path>` | Records the choice: copies the file into `packs/<slug>/visuals/` beside the spec in the packaging-skills repo, writes the spec key, appends the credits row there, and appends the decisions line to `<work>/decisions.md` in the local work folder (`shared/tools/pack_paths.py`). `--note` for the owner's reason, `--dry-run` to see it without writing, `--add-to-library` to add a chosen icon to the shared library. |
| `../tools/visuals_common.py` | The slot list, the licence allow-lists, the provenance record and the network helpers. Not run directly. |

Every tool takes `--help`. Paths are arguments; nothing is hard-coded to one machine.

## Exit codes — the same across all of them

| Exit | Meaning |
|---|---|
| 0 | did what was asked |
| 1 | usage or input error — an unknown slot, a missing file, an icon name that is not in the set, or (for a search) the reachable sources genuinely had nothing under an allowed licence |
| 2 | refused on licence grounds: the file's recorded licence is not one this bundle may use. Nothing is written. |
| **3** | **deferred — a source could not be reached** (no key, a timeout, a rate limit). This is an environment limitation, not a fact about the world. Tell the owner which source and what it needs, and retry. Never record it as "not found": that closes the picture forever on the strength of a network failure. A search whose only answering source came back empty while others were unreachable also exits 3. |

## The slots

The slot list lives in one place, `visuals_common.SLOT_KINDS`, so adding one is a row there plus a
line in `shared/references/visual-assets.md`:

| Slot | Kind | Written to | Used by |
|---|---|---|---|
| `vertical:<n>` | icon | `verticals[n].icon` | the sales deck's industries slide, later the site |
| `today` | photo | `deck.images.today` | the sales deck, today → tomorrow, left |
| `tomorrow` | photo | `deck.images.tomorrow` | the sales deck, today → tomorrow, right |
| `hero` | photo | `one_pager.images.hero` | reserved — the one-pager banner, not yet asked for by a builder |

The shape written into the spec is documented in `shared/schema/pack-spec.md`. An icon writes both
renders (`file` = ink, `file_white` = white); a photograph writes the file plus its source, creator
and licence, so a builder never has to open the credits file to print a caption.

## What needs a key

A key is read from the environment variable of its name (`PEXELS_API_KEY`,
`UNSPLASH_ACCESS_KEY`), or on a Mac from the Keychain entry of that name. Checked 2026-09-22 on the
owner's Mac:

| Source | State |
|---|---|
| Openverse | works with no key |
| Tabler (PNG package and SVG) | works with no key |
| Lucide (SVG) | works with no key |
| Pexels | **needs a key**, free at pexels.com/api: set the environment variable `PEXELS_API_KEY`, or on a Mac `security add-generic-password -s PEXELS_API_KEY -a <you> -w <key>` |
| Unsplash | **needs a key**; the public search endpoint answers 401 without one. The environment variable `UNSPLASH_ACCESS_KEY`, or on a Mac the Keychain entry of that name |

Without a Pexels or Unsplash key, photographs come only from Openverse's public-domain pool, which
is strong on machinery, vehicles and control rooms and weak on contemporary office scenes. Say that
to the owner before the first photograph question rather than after.

## Run it

```sh
V=plugins/oracle-packs/skills/visuals/tools
shared/tools/py $V/suggest_icons.py "Telecom & cable" --context "<the 'what matters here' line>"
shared/tools/py $V/fetch_icon.py antenna --out <work>/candidates/vertical-2 --slot vertical:2
shared/tools/py $V/search_photos.py "control room" --out <work>/candidates/tomorrow --slot tomorrow --n 3
shared/tools/py $V/contact_sheet.py <work>/candidates/tomorrow --out <work>/candidates/tomorrow.png --title "Today → tomorrow"
shared/tools/py $V/apply_choice.py <repo>/packs/<slug>/pack-spec.md --slot tomorrow \
    --file <work>/candidates/tomorrow/tomorrow-A-....jpg --note "<the owner's reason>"
```

`shared/tools/py` runs each tool with an interpreter that has the packages, provisioning one on first
use; `shared/tools/py --check` shows which. `<repo>` and `<work>` are what
`shared/tools/py shared/tools/pack_paths.py <slug>` prints: candidates and contact sheets stay in the
local work folder, and only the chosen file reaches the repo's `packs/<slug>/visuals/`.

## Test fixture

The deck skill's fixture doubles as this step's: an anonymized Workforce Optimization spec with four
industries and a problem/solution the photograph terms can be built from.

```sh
shared/tools/py $V/suggest_icons.py "Residential appliance & white-goods repair"
# -> wash-machine, home-cog, tool
```

Copy the fixture before running `apply_choice.py` against it — it is a read-only test input.

## Dependencies

`PyYAML` and `Pillow`, plus one SVG rasterizer for icons above 240 px (or when the PNG package does
not answer): QuickLook (`qlmanage`, on every Mac) first, then `rsvg-convert` (librsvg) on PATH,
then the `cairosvg` Python module. `fetch_icon.py` rewrites the SVG's declared `width`/`height`
before rendering, which is what stops a 24-unit icon rendering as a 70 px glyph in the corner of a
1024 px canvas. With none of the three it exits 3 (deferred) and names all three. Everything else is
the standard library.

## Done means

1. **Every picture has a recorded licence** from the allowed list, and a row in
   `packs/<slug>/visuals/credits.md`.
2. **The owner chose each one**, from three candidates, looking at the contact sheet — which was
   opened beside the conversation *before* the question.
3. **The spec still passes its checks** (`shared/tools/lint_spec.py`) and its diff shows only the
   picture keys: `apply_choice.py` writes through the spec writer (`shared/tools/packspec.py`),
   which re-renders the file only when its round trip is exact.
4. **Slots with no choice are named as open**, and the deck draws an empty container for them —
   never a stand-in, never a numeral.
