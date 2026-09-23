# Where a picture may come from

**What this is.** The licence gate every candidate passes before it is shown, and the record kept for every file that is chosen. Long form, with what each source needs: `shared/references/visual-assets.md`.

**The checks**

1. **Only licences that permit commercial use without a credit line.** Photographs: CC0 and the Public Domain Mark through Openverse, the Pexels License, the Unsplash License. Icons: the MIT and ISC open sets — Tabler first, Lucide as the fallback.
2. **Never** an image from a search engine; never a stock-library preview (Getty, Shutterstock, Adobe Stock, iStock, Alamy — watermark-free previews and free trials included); never CC-BY, -SA or -NC; never a file whose licence nobody recorded; never a vendor's logo as an icon; never a generated picture.
3. **Say what is reachable before the first question.** Run one search and read what the tool reports: which sources answered, which need a key. If the sources that carry contemporary working life need a key this machine does not have, say so in one plain line and let the owner decide whether to add one or work with what is reachable.
4. **A source that cannot be reached is deferred, never "nothing found."** Name the source, what it needs, and that the picture is still open — then retry. Exit code 3 from any of these tools means deferred. "Nothing found" closes the item forever on the strength of a timeout.
5. **The credits file is part of the pack.** Every chosen file gets a row in `packs/<slug>/visuals/credits.md` — file, slot, source, creator, licence, page, date — including files whose licence asks for no credit. A picture with no row is not in the pack.

**Writes:** the credits file; a `.json` sidecar beside every candidate downloaded.
