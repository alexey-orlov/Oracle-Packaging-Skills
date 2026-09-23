# What the delivered Workforce Optimization artifacts get wrong

Best reference for **anatomy**, worst for **consistency**: a builder copying a value out of one of them copies one of these. Every one is resolved in the spec — read the spec, not the artifact.

| Divergence | What the estate carries | The resolved value |
|---|---|---|
| Five PoV infrastructure prices | no infra row · `€0` · `€4K` · `~€2K *` · `€4K/mo` | `~€2K / month`, indicative, with its footnote. The spec is the only source. |
| Two tier vocabularies | `PoV · S / Roll-out · M / Scaling · L` in print; `Jumpstart Proof-of-Value / Integration / Scale` on the site | `PoV Jumpstart / Integration / Scaling` everywhere; `S / M / L` as internal size tags only. |
| Three contacts | the alliances contact in print, the practice mailbox on the site, the R&D mailbox internally | A per-channel mapping in `contacts`; the builder reads its own channel. |
| Two names for one product | "Oracle Field Service" · "Oracle **Fusion** Field Service" | The catalog's canonical name, re-verified against the vendor at each build. |
| Two glyph systems | two colours of the same `●` for available and partial | `● ◐ ○`, three distinct glyphs. |
| Two figure sets | print ships one set, the site another for the same pack | One metric set per pack; attribution varies by channel, figures never. |
| Two PoV durations | "2 months" in print, "4–8 weeks" on the site | 4–8 weeks, 10-week cap. |
| Two grouping axes, mixed casing | `Area > Category > Feature` vs the site's `Stage > Item` | The second is derived from the first, per pack; casing from `meta.name_variants`. |
