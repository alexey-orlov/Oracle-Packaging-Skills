# Sources — asked first, always

**What this is.** The one thing that happens before anything else: asking the user what the real product looks like. **Never start from the pack spec alone, and never reconstruct a product from imagination.**

**The checks**

1. Asked **first**, in one widget, naming all four and where they live, in order of usefulness: **a recording** of the real product (screen-share, customer demo, walkthrough video) · **screenshots** of the real screens · **a written overview** of the flow and the information model · **a detailed brief**, where none of the above exists.
2. **Without at least one, stop** and say why in plain words: a walkthrough built from the brief alone would not match the product, and anyone who has seen the real thing spots it.
3. Where the walkthrough must look like a vendor's real interface, that platform's **own published screens** are asked for too.
4. State what you have and what is missing, and **raise the questions and concerns before proceeding**, not after the first cut.
5. **When no product recording exists**, the platform the use case runs on *is* the real product, and its interfaces must be **recognizable, not invented**. Widen the search before calling anything free design: vendor product videos (screenshot them at timestamps), documentation figures, session decks and PDFs page by page, feature-announcement posts, hands-on-lab images, product-tour assets, the vendor's sample applications.
6. **Log every source tried.** Documentation sites often build their contents in JavaScript, so a link crawl misses whole chapters: download the book PDF, grep its text, then fetch the HTML of the chapter that matters.

**Reconstructing from a recording:** frames at their timestamps, the narration transcribed on-device, any spec sheet shown on screen read out.

**Fills / reads:** the user's answer; the next step writes `<work>/.scratch/demo/flow.md`.
