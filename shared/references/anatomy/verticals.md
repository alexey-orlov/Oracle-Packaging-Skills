# Component 5 — verticals and their framings

**What this is.** Three to five industries, each carrying its **own** one-line problem ↔ solution pair and a "what matters here" sentence — what the work actually looks like in that industry. A chip row of industry nouns is the degenerate form, acceptable only where the page has no room for more.

**Checks the draft must pass**

1. Each vertical's pair is about that industry's own work, not the pack's sentence with the industry noun swapped.
2. Each carries `status: proven | plausible | roadmap`. Only the delivered case is **proven**.
3. The vertical labels are identical in every artifact.
4. Three to five. A sixth is usually a sign that two of them are the same operation.
5. Each has a picture slot for the deck's industries slide — an icon, never a number. `/oracle-packs:visuals` fills it.

**Good.** Telecom: *"Install-and-repair technicians have to be routed to tight appointment windows across regions, matched to line skills."* → *"Appointment windows and line skills are modeled as commitment and skill rules, and the solver routes against them while minimizing travel."* Compressed, for a deck card: *"Utilities — water · gas · electric. Schedule field crews across service territories against SLAs, outage spikes and crew certifications."*

**Bad.** Four rows of one sentence with the industry changed. A vertical marked proven on the strength of a plausible fit.

**Fills:** `verticals[]` — `name`, `label`, `problem`, `solution`, `what_matters`, `status`, `icon`.
