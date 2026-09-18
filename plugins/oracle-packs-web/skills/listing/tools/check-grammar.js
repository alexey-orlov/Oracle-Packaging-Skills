#!/usr/bin/env node
/**
 * check-grammar.js — asserts that every product entry in a practice site's
 * `site/data/content.js` fills every slot of the listing's visual grammar, and
 * that no round's owner rule has been quietly lost in a rewrite.
 *
 *   node check-grammar.js --site-root /path/to/site-repo
 *   node check-grammar.js --content /path/to/content.js [--config /path/to/config.js]
 *   node check-grammar.js --help
 *
 * Exits 0 and prints OK when every product passes; exits 1 and names every
 * failure otherwise; exits 2 when it cannot find the files. Missing image files
 * are warnings, not failures — copy and imagery ship on separate tracks.
 * Dependency-free: any Node, no npm install, ever.
 *
 * ===========================================================================
 * PORTED from the practice site's own tools/check-grammar.js. Every change:
 *
 * 1. PATHS ARE INPUTS, NOT CONSTANTS. The original resolved everything from
 *    `path.resolve(__dirname, "..")`, which only works while the file sits in
 *    the site repo's own tools/. This copy resolves, in order:
 *      --site-root <dir>  the repo that contains site/   ($ORACLE_SITE_ROOT)
 *      --content <file>   an explicit content.js         ($ORACLE_SITE_CONTENT)
 *      --config <file>    an explicit config.js          ($ORACLE_SITE_CONFIG)
 *    With only --content, config.js and the site dir are resolved beside it.
 *    With neither, it probes ./site/data/content.js and ../site/data/content.js,
 *    so a copy dropped into a site repo's tools/ keeps working unchanged.
 *    Everything the checker reads off disk (app.js, index.html, review.js,
 *    the logo folder, the hero and step images) hangs off the resolved site
 *    dir instead of a fixed "site/" prefix.
 *
 * 2. THE PRODUCT-COUNT ASSERTION IS RELAXED. `products.length !== 7` became
 *    `products.length < 1`. That one comparison was the only thing rejecting an
 *    eighth pack by construction; no slug is hard-coded anywhere else in the
 *    300-plus assertions, so relaxing it makes the whole gate work for a
 *    catalog of any size. The closing OK line reports the real count.
 *
 * 3. THE HARD-CODED SLUG LIST IS DATA-DRIVEN. `UNPACKAGED` named two slugs of
 *    one catalog. It now resolves from, in order: --unpackaged <csv>,
 *    $ORACLE_UNPACKAGED, `SITE_CONFIG.unpackagedSlugs`, else derived from the
 *    data itself (every product carrying a `statusNote`). The rule is
 *    unchanged: a product with no package says so in one muted line, and no
 *    other product carries that line.
 *
 * 4. THE CUSTOMER DENY-LIST IS AN INPUT FILE. The original embedded the real
 *    customer names — exactly the content that must not travel in a shared
 *    bundle. This copy loads them from JSON, resolved from: --deny-list <file>,
 *    $ORACLE_DENY_LIST, <site-root>/tools/deny-list.json, else
 *    deny-list.example.json beside this script. Shape:
 *      { "customerNames": ["..."], "bannedStrings": [["...", "why"]] }
 *    Generic bans that carry no customer information (British spellings,
 *    packaging-internal disclaimers, internal markers, the "AIDP" abbreviation)
 *    stay inline. Running with an empty customer list WARNS loudly: an
 *    unconfigured deny-list is the one failure mode that ships a customer name.
 *
 * 5. THE SUCCESS LINE IS DATA-DRIVEN. It used to print "7 products".
 *
 * 6. TWO DISK READS ARE GUARDED. `index.html` and `assets/app.js` are read to
 *    check the Internal panel's script tags and the icon registry; a tree
 *    without them now warns instead of throwing.
 *
 * Nothing else is touched. Every other assertion, comment and message is the
 * original's, so a rule the owner won in a review round survives this port.
 *
 * A NOTE ON THE COMMENTS. Many assertions cite a section of the source site's
 * own documentation (its round record, its handoff, its start-here page, its
 * visual-grammar doc). Those documents do not ship with this bundle, and the
 * citations are kept deliberately: each one says WHY a rule exists and which
 * review round produced it, which is the difference between a rule you can
 * argue with and a rule you delete because it looks arbitrary. Read them as
 * provenance markers, not as files to go and find.
 *
 * The practice mailbox and the corporate domain asserted below are this
 * practice's own public addresses, printed on its external material. They are
 * the one site constant left inline; change them if you run a different
 * practice's site through this gate.
 * ===========================================================================
 */

"use strict";

var fs = require("fs");
var path = require("path");
var vm = require("vm");

/* ---- inputs (change 1) ---- */
var ARGV = process.argv.slice(2);
function opt(name) {
  var i = ARGV.indexOf("--" + name);
  return i !== -1 && i + 1 < ARGV.length ? ARGV[i + 1] : "";
}
function has(name) { return ARGV.indexOf("--" + name) !== -1; }
function firstExisting(cands) {
  for (var i = 0; i < cands.length; i++) if (cands[i] && fs.existsSync(cands[i])) return cands[i];
  return "";
}

if (has("help") || has("h")) {
  console.log([
    "check-grammar.js — the listing acceptance gate.",
    "",
    "  --site-root <dir>   repo containing site/            ($ORACLE_SITE_ROOT)",
    "  --content <file>    content.js to check              ($ORACLE_SITE_CONTENT)",
    "  --config <file>     config.js to pair with it        ($ORACLE_SITE_CONFIG)",
    "  --unpackaged <csv>  slugs that carry a statusNote    ($ORACLE_UNPACKAGED)",
    "  --deny-list <file>  JSON deny-list                   ($ORACLE_DENY_LIST)",
    "  --help",
    "",
    "Exit 0 = OK · 1 = failures listed · 2 = inputs not found."
  ].join("\n"));
  process.exit(0);
}

var argSiteRoot = opt("site-root") || process.env.ORACLE_SITE_ROOT || "";
var argContent = opt("content") || process.env.ORACLE_SITE_CONTENT || "";
var argConfig = opt("config") || process.env.ORACLE_SITE_CONFIG || "";
var siteRoot = argSiteRoot ? path.resolve(argSiteRoot) : "";

var CONTENT_PATH = argContent ? path.resolve(argContent) : firstExisting([
  siteRoot ? path.join(siteRoot, "site/data/content.js") : "",
  path.join(process.cwd(), "site/data/content.js"),
  path.join(path.resolve(__dirname, ".."), "site/data/content.js")
]);
if (!CONTENT_PATH || !fs.existsSync(CONTENT_PATH)) {
  console.error("check-grammar: no content.js found. Pass --site-root <repo containing site/> or --content <file>.");
  process.exit(2);
}
/* <site-root>/site is the publish root: every other read hangs off it. */
var SITE_DIR = siteRoot ? path.join(siteRoot, "site") : path.resolve(path.dirname(CONTENT_PATH), "..");
var CONFIG_PATH = argConfig ? path.resolve(argConfig) : path.join(path.dirname(CONTENT_PATH), "config.js");
var root = path.resolve(SITE_DIR, "..");
if (!fs.existsSync(CONFIG_PATH)) {
  console.error("check-grammar: no config.js found at " + CONFIG_PATH + ". Pass --config <file>.");
  process.exit(2);
}

var sandbox = { window: {} };
vm.createContext(sandbox);
[CONTENT_PATH, CONFIG_PATH].forEach(function (abs) {
  vm.runInContext(fs.readFileSync(abs, "utf8"), sandbox, { filename: path.basename(abs) });
});

/* ---- the deny-list (change 4) ---- */
var DENY_PATH = firstExisting([
  opt("deny-list") ? path.resolve(opt("deny-list")) : "",
  process.env.ORACLE_DENY_LIST ? path.resolve(process.env.ORACLE_DENY_LIST) : "",
  path.join(root, "tools/deny-list.json"),
  path.join(__dirname, "deny-list.example.json")
]);
var DENY = { customerNames: [], bannedStrings: [] };
var denyNote = "";
if (DENY_PATH) {
  try {
    var parsed = JSON.parse(fs.readFileSync(DENY_PATH, "utf8"));
    DENY.customerNames = Array.isArray(parsed.customerNames) ? parsed.customerNames : [];
    DENY.bannedStrings = Array.isArray(parsed.bannedStrings) ? parsed.bannedStrings : [];
    denyNote = path.basename(DENY_PATH);
  } catch (e) {
    console.error("check-grammar: deny-list " + DENY_PATH + " is not valid JSON: " + e.message);
    process.exit(2);
  }
}
var CUSTOMER_NAMES = DENY.customerNames;

var C = sandbox.window.SITE_CONTENT;
var CFG = sandbox.window.SITE_CONFIG;

var INDUSTRIES = [
  "manufacturing", "logistics", "utilities", "telecom", "healthcare",
  "financial-services", "insurance", "retail", "energy", "public-sector",
  "automotive", "life-sciences", "professional-services", "construction",
  "travel-transport", "cross-industry"
];
/* E3: the solution stack renders top → bottom in this order. A product may
   omit a layer (the Lakehouse pair has no NVIDIA engine) but may never
   re-order them — the Technology tab is the surface a technical buyer
   compares most directly across products. */
var STACK_KEYS = ["application", "ai-engine", "data-platform", "infrastructure", "custom"];
var STACK_VENDORS = ["oracle", "nvidia", "softserve"];
var DIRECTIONS = ["inbound", "outbound", "both"];
/* G: the Jumpstart block is the same three pillars on all seven, in this order. */
var PILLARS = ["fast", "low-risk", "tangible"];
var NEXT_TIERS = ["Integration", "Scale"];
/* A matrix row carrying a restrictive asterisk is PARTIAL: an unqualified
   SUPPORTED tag on it would overstate the source. */
var CAP_STATES = ["supported", "partial", "roadmap"];
/* Round 4, C1: a case study is measured, modeled against a historical baseline,
   or in preparation. The status drives the chip and the metric eyebrow — both
   have to say the same word as the story, which is what the eyebrow map below
   enforces — so a fourth value would render an empty chip. */
var CASE_STATUSES = ["measured", "modeled", "in-preparation"];
/* The status word renders ONCE per card, in the chip, read from
   shared.caseStudyStatus — Proven / Forecast / Estimated. The eyebrow over the
   figure used to repeat it, which put the same word on a card twice and made a
   forecast read as a disclaimer rather than a result. Both eyebrow keys are
   retired and the checker fails them if they come back. */
var CASE_STATUS_CHIPS = ["Proven", "Forecast", "Estimated"];
/* Round 4, T1: the three tag families and the two availability badges. */
var PATTERN_IDS = ["deep-research", "processing-pipelines", "data-analysis"];
/* Round 4, T3: ONE canonical technology set, used identically on the rail, the
   hero chip, the tile band and the Services platform cards. The ids and the
   labels are paired here so a product, a glyph and a card can never drift into
   a product-specific variant ("OCI + NVIDIA AI-Q") of a platform name. */
var FACET_IDS = ["oci-nvidia", "oracle-ai-data-platform", "oracle-ai-lakehouse", "oracle-ai-fusion"];
var FACET_LABELS = {
  "oci-nvidia": "OCI + NVIDIA",
  "oracle-ai-data-platform": "Oracle AI Data Platform",
  "oracle-ai-lakehouse": "Oracle Autonomous AI Lakehouse",
  "oracle-ai-fusion": "Oracle AI for Fusion Applications"
};
/* Round 4, T1: only these two carry the muted "in preparation" status line;
   every other product's state is told by its availability badges. */
/* CHANGE 3 — the two slugs this list used to name belonged to one catalog.
   The rule is the invariant, not the slugs: a product with no package says so
   in one muted line under the hero one-liner, and no other product carries
   that line. Source order: --unpackaged, $ORACLE_UNPACKAGED,
   SITE_CONFIG.unpackagedSlugs, else the data itself. */
var UNPACKAGED = (function () {
  var csv = opt("unpackaged") || process.env.ORACLE_UNPACKAGED || "";
  if (csv) return csv.split(",").map(function (s) { return s.trim(); }).filter(Boolean);
  if (Array.isArray((CFG || {}).unpackagedSlugs)) return CFG.unpackagedSlugs.slice();
  return ((C || {}).products || []).filter(function (p) {
    return typeof p.statusNote === "string" && p.statusNote.trim().length > 0;
  }).map(function (p) { return p.slug; });
})();
var RETIRED_TAGS = ["Available now", "Fixed-price offer", "In preparation"];
/* CHANGE 4 — CUSTOMER_NAMES is loaded from the deny-list file at the head of
   this script, so no customer name lives in a shared bundle. */
/* E: a one-liner says what the product does, for whom, with what outcome. It is
   not the place for the packaging story — that is what the Jumpstart tab is. */
var PACKAGING_PHRASES = [
  "packaged from proof of value",
  "from proof of value to enterprise scale",
  "fixed-price",
  "fixed price",
  "quick start",
  "proof of value to enterprise"
];

var failures = [];
var warnings = [];
function fail(where, message) { failures.push(where + " — " + message); }
function warn(where, message) { warnings.push(where + " — " + message); }

function str(v) { return typeof v === "string" && v.trim().length > 0; }
function arr(v) { return Array.isArray(v); }
function words(s) { return s.trim().split(/\s+/).length; }
function sentences(s) {
  return s.split(/(?<=[.!?])\s+/).filter(function (x) { return x.trim().length; }).length;
}
/* Assets and copy ship on separate tracks, so a missing file is a warning. */
function checkAsset(where, what, rel) {
  if (!fs.existsSync(path.join(SITE_DIR, rel))) {
    warn(where, what + " not on disk yet: site/" + rel);
  }
}

function checkHeroImage(where, image) {
  if (!image || typeof image !== "object") return fail(where, "hero.image missing");
  ["file", "alt", "focal"].forEach(function (k) {
    if (!str(image[k])) fail(where, "hero.image." + k + " missing or empty");
  });
  if (!/^assets\/img\/heroes\/[a-z0-9-]+\.(jpg|jpeg|png|webp)$/.test(image.file)) {
    fail(where, 'hero.image.file "' + image.file + '" is not assets/img/heroes/<name>.<ext>');
  }
  /* Not a failure: the data layer and the imagery ship on separate tracks. */
  if (!fs.existsSync(path.join(SITE_DIR, image.file))) {
    warn(where, "hero image not on disk yet: site/" + image.file);
  }
}

/* ---- shared heroes ----
   Round 5: the home page carries no hero photograph — the built-on stack visual
   is its only illustration — so `overview.hero.image` is retired, and the
   home-page block below fails if it returns. Services keeps its hero image, and
   so do all seven products. */
checkHeroImage("services", C.services.hero && C.services.hero.image);

/* ---- products ---- */
/* CHANGE 2 — was `!== 7`. The count is the catalog owner's business; the
   grammar is this file's. An empty catalog is still a failure. */
if (!arr(C.products) || C.products.length < 1) {
  fail("products", "expected at least one product, got " + (arr(C.products) ? C.products.length : "none"));
}

(C.products || []).forEach(function (p) {
  var w = "products[" + p.slug + "]";
  var o = p.overview || {};
  var t = p.technology || {};
  var v = p.jumpstart || {};

  /* identity + hero */
  ["slug", "name", "oneLiner"].forEach(function (k) {
    if (!str(p[k])) fail(w, k + " missing");
  });
  if (str(p.oneLiner)) {
    var lowOne = p.oneLiner.toLowerCase();
    PACKAGING_PHRASES.forEach(function (phrase) {
      if (lowOne.indexOf(phrase) !== -1) {
        fail(w, 'oneLiner carries the packaging phrase "' + phrase + '" — the one-liner says what the product does, not how it is sold');
      }
    });
  }
  if (p.pov !== undefined) fail(w, "pov is superseded by jumpstart — nothing renders it");
  /* Round 4, T1: the three availability states became two badges driven by
     config flags. Nothing renders the chip model any more. */
  ["availability", "availabilityChip", "availabilityTooltip"].forEach(function (k) {
    if (p[k] !== undefined) fail(w, k + " is superseded by the availability badges — nothing renders it");
  });
  if (p.statusNote !== undefined) {
    if (!str(p.statusNote)) fail(w, "statusNote must be a non-empty string where present");
    else if (UNPACKAGED.indexOf(p.slug) === -1) {
      fail(w, "statusNote belongs only to the two unpackaged products (" + UNPACKAGED.join(", ") + ")");
    } else if (sentences(p.statusNote) > 1) {
      fail(w, "statusNote is " + sentences(p.statusNote) + " sentences — it is one muted line under the hero one-liner");
    }
  }
  if (UNPACKAGED.indexOf(p.slug) !== -1 && !str(p.statusNote)) {
    fail(w, "statusNote missing — an unpackaged product says so in one line, since it carries no availability badge");
  }
  (p.tags || []).forEach(function (tag) {
    if (RETIRED_TAGS.indexOf(tag) !== -1) {
      fail(w, 'tags carries the retired availability chip "' + tag + '" — availability is a badge now, not a tag');
    }
  });
  if (!arr(p.tags) || !p.tags.length) fail(w, "tags missing");
  /* T3: the platform a product runs on is one of the four canonical facets, and
     the chip that names it carries that facet's label verbatim. */
  if (FACET_IDS.indexOf(p.facet) === -1) {
    fail(w, 'facet "' + p.facet + '" is not one of ' + FACET_IDS.join(" / "));
  }
  /* The hero chip row is built from `category` and `facet` and skips tags[0]
     and tags[1], so those two have to say what the renderer already says.
     Anything past them renders as a second technology chip beside the platform
     one, which is how "AI-Q" and "cuOpt" came to read as part of the platform
     name — engine detail belongs in the Technology tab, not in the chip row. */
  if (arr(p.tags)) {
    if (p.tags.length !== 2) {
      fail(w, "tags holds " + p.tags.length + " entries — exactly two: the pattern chip and the canonical platform label");
    }
    if (str(p.categoryChip) && p.tags[0] !== p.categoryChip) {
      fail(w, 'tags[0] is "' + p.tags[0] + '" but the pattern chip renders "' + p.categoryChip + '"');
    }
    var wantFacetLabel = FACET_LABELS[p.facet];
    if (wantFacetLabel && p.tags[1] !== wantFacetLabel) {
      fail(w, 'tags[1] is "' + p.tags[1] + '" but the technology chip renders "' + wantFacetLabel + '"');
    }
  }
  if (!p.hero) fail(w, "hero missing"); else checkHeroImage(w, p.hero.image);
  if (!CFG.products[p.slug]) fail(w, "no matching SITE_CONFIG.products entry");
  else {
    if (typeof CFG.products[p.slug].videoPoster !== "string") {
      fail(w, "config.videoPoster missing (must exist, may be empty)");
    }
    /* A string here would be truthy whatever it said, so "false" would turn
       the frame on. The flag decides a layout — it has to be a real boolean. */
    if (typeof CFG.products[p.slug].video !== "boolean") {
      fail(w, "config.video missing or not a boolean (true | false)");
    }
    /* Round 4, T1/T2: the Marketplace badge and the Marketplace facet both read
       this flag. A string would be truthy whatever it said. */
    if (typeof CFG.products[p.slug].marketplace !== "boolean") {
      fail(w, "config.marketplace missing or not a boolean (true | false)");
    }
    /* The two availability flags are the owner's statement that the thing
       exists; the URLs are the wiring, and they arrive later. So the only rule
       here is the type — either flag may be true with an empty URL (the badge
       renders unlinked, the video frame says a recording is in preparation),
       and neither flag is asserted to any particular value. The one cross-check
       that stays is the reverse case, where a URL exists but its flag is off and
       the control would never render. */
    if (CFG.products[p.slug].marketplaceUrl && !CFG.products[p.slug].marketplace) {
      fail(w, "config.marketplaceUrl is set but config.marketplace is false — the badge would not render for a listing that exists");
    }
  }

  /* 2.1 problem → solution */
  var ps = o.problemSolution;
  if (!ps) fail(w, "overview.problemSolution missing");
  else ["problem", "solution"].forEach(function (side) {
    var panel = ps[side];
    if (!panel) return fail(w, "problemSolution." + side + " missing");
    ["title", "text", "icon"].forEach(function (k) {
      if (!str(panel[k])) fail(w, "problemSolution." + side + "." + k + " missing");
    });
  });

  /* 2.2 metrics */
  if (!arr(o.metrics) || o.metrics.length < 1 || o.metrics.length > 4) {
    fail(w, "overview.metrics must hold 1–4 tiles, got " + (arr(o.metrics) ? o.metrics.length : "none"));
  } else o.metrics.forEach(function (m, i) {
    var mw = w + ".metrics[" + i + "]";
    if (!(m.value === null || str(m.value))) fail(mw, "value must be a non-empty string or null");
    if (str(m.value) && m.value.length > 20) fail(mw, 'value "' + m.value + '" is too long to set large');
    ["label", "qualifier", "icon"].forEach(function (k) {
      if (!str(m[k])) fail(mw, k + " missing");
    });
    if (str(m.qualifier) && words(m.qualifier) > 14) fail(mw, "qualifier is " + words(m.qualifier) + " words (max 14)");
  });
  if (!str(o.metricsNote)) fail(w, "overview.metricsNote missing — a metric row never renders without it");

  /* 2.3 roi */
  if (!o.roi) fail(w, "overview.roi missing");
  else ["icon", "text"].forEach(function (k) {
    if (!str(o.roi[k])) fail(w, "overview.roi." + k + " missing");
  });

  /* 2.4 features */
  if (!arr(o.features) || o.features.length < 6 || o.features.length > 8) {
    fail(w, "overview.features must hold 6–8 items, got " + (arr(o.features) ? o.features.length : "none"));
  } else o.features.forEach(function (f, i) {
    if (!str(f)) return fail(w, "features[" + i + "] is not a string");
    if (words(f) > 12) fail(w, 'features[' + i + '] is ' + words(f) + ' words (max 12): "' + f + '"');
  });
  if (!arr(o.featuresDetail) || o.featuresDetail.length < 6) {
    fail(w, "overview.featuresDetail must keep the long-form list (≥6 entries)");
  }

  /* 2.5 industries — the chips are superseded by the industryCases tabs; only
     the "where else this applies" line survives, under the tab component. */
  if (o.industries !== undefined) fail(w, "overview.industries is superseded by overview.industryCases — nothing renders it");
  if (!str(o.industriesNote)) fail(w, "overview.industriesNote missing");

  /* 2.6 scope */
  if (!o.scope || !arr(o.scope.in) || !arr(o.scope.out)) fail(w, "overview.scope.in / .out missing");
  else {
    if (o.scope.in.length < 4) fail(w, "overview.scope.in needs ≥4 items");
    if (o.scope.out.length < 4) fail(w, "overview.scope.out needs ≥4 items");
  }

  /* 2.7 more detail */
  if (!arr(o.moreDetail) || o.moreDetail.length < 3) fail(w, "overview.moreDetail needs ≥3 entries");
  else o.moreDetail.forEach(function (d, i) {
    if (!str(d.title) || !str(d.body)) fail(w, "moreDetail[" + i + "] needs { title, body }");
  });

  /* 2.8 case study — round 4, C1. An anonymized customer callout, or null.
     There is no empty state: a block whose only content is "nothing published
     yet" is worse than its absence on a page sellers demo live. */
  if (o.caseStudy === undefined) fail(w, "overview.caseStudy missing — it is null where no case study ships");
  if (o.successStory !== undefined) fail(w, "overview.successStory is superseded by overview.caseStudy — nothing renders it");
  if (o.caseStudy !== null && o.caseStudy !== undefined) {
    var cs = o.caseStudy;
    if (cs.metricsEyebrow !== undefined) {
      fail(w, "overview.caseStudy.metricsEyebrow is retired — the status chip carries the word once");
    }
    ["descriptor", "area", "industry", "status", "story", "ndaLine", "downloadLabel"].forEach(function (k) {
      if (!str(cs[k])) fail(w, "overview.caseStudy." + k + " missing");
    });
    if (cs.customer !== undefined) fail(w, "overview.caseStudy.customer is banned — no customer is named on this site");
    if (cs.logo !== undefined || cs.logoStacked !== undefined) {
      fail(w, "overview.caseStudy carries a logo — the industry medallion replaced it and no customer mark ships");
    }
    /* The header band was removed: it repeated the industry photograph the
       industry tabs render a few hundred pixels higher on the same page. */
    if (cs.image !== undefined) {
      fail(w, "overview.caseStudy.image is superseded — the callout opens on the medallion, not on a header band");
    }
    if (CASE_STATUSES.indexOf(cs.status) === -1) {
      fail(w, 'overview.caseStudy.status "' + cs.status + '" is not ' + CASE_STATUSES.join(" / "));
    }
    if (INDUSTRIES.indexOf(cs.industry) === -1) {
      fail(w, 'overview.caseStudy.industry "' + cs.industry + '" is not in the fixed set of 16');
    }
    /* One or two headline figures. Two is the default; one is correct where
       only one real outcome exists, and padding the second slot with a
       capability restatement set at 40px is the failure this allows out of. */
    if (!arr(cs.metrics) || cs.metrics.length < 1 || cs.metrics.length > 2) {
      fail(w, "overview.caseStudy.metrics must hold 1 or 2 headline figures");
    } else cs.metrics.forEach(function (m, i) {
      if (!str(m.value) || !str(m.label)) fail(w, "caseStudy.metrics[" + i + "] needs { value, label }");
      if (str(m.value) && m.value.length > 20) fail(w, 'caseStudy.metrics[' + i + '].value "' + m.value + '" is too long to set large');
    });
    if (!arr(cs.scope) || cs.scope.length !== 3) {
      fail(w, "overview.caseStudy.scope must hold exactly 3 facts — the compact scope row");
    } else cs.scope.forEach(function (f, i) {
      if (!str(f.label) || !str(f.value)) fail(w, "caseStudy.scope[" + i + "] needs { label, value }");
    });
    /* Rule 1 of VISUAL-GRAMMAR: a number never renders away from its caveat,
       and this block has no footnote row of its own. */
    if (str(cs.story) && !/illustrative|modeled simulations|not contractual/i.test(cs.story)) {
      fail(w, "caseStudy.story carries figures with no caveat sentence — the block has no footnote row of its own");
    }
  }

  /* E2 · How it works — the workflow stepper */
  if (!arr(o.steps) || o.steps.length < 3 || o.steps.length > 5) {
    fail(w, "overview.steps must hold 3–5 workflow steps, got " + (arr(o.steps) ? o.steps.length : "none"));
  } else {
    var covered = [];
    o.steps.forEach(function (s, i) {
      var sw = w + ".steps[" + i + "]";
      if (s.n !== i + 1) fail(sw, 'n is "' + s.n + '", expected ' + (i + 1) + " — steps are numbered in order from 1");
      ["title", "text", "image"].forEach(function (k) {
        if (!str(s[k])) fail(sw, k + " missing");
      });
      /* ≤ 2 lines in the stepper, whose column is narrow. */
      if (str(s.text) && words(s.text) > 30) fail(sw, "text is " + words(s.text) + " words (max 30 — it has to fit two lines)");
      if (str(s.image)) {
        var want = new RegExp("^assets/img/steps/" + p.slug + "-" + (i + 1) + "\\.(jpg|jpeg|png|webp|svg)$");
        if (!want.test(s.image)) fail(sw, 'image "' + s.image + '" must be assets/img/steps/' + p.slug + "-" + (i + 1) + ".<jpg|png|webp|svg>");
        else checkAsset(sw, "step image", s.image);
      }
      if (!arr(s.features) || !s.features.length) fail(sw, "features missing — every step carries the feature bullets that belong to it");
      else s.features.forEach(function (f) {
        if (!arr(o.features) || o.features.indexOf(f) === -1) fail(sw, 'feature "' + f + '" is not one of overview.features');
        else if (covered.indexOf(f) !== -1) fail(sw, 'feature "' + f + '" is claimed by more than one step');
        else covered.push(f);
      });
    });
    /* No bullet may fall between the steps: the stepper replaces the checklist. */
    (o.features || []).forEach(function (f) {
      if (covered.indexOf(f) === -1) fail(w, 'feature "' + f + '" belongs to no step — every overview.features item lands in exactly one');
    });
  }

  /* E2 · Industry use cases — the tab component */
  if (!arr(o.industryCases) || o.industryCases.length < 3 || o.industryCases.length > 6) {
    fail(w, "overview.industryCases must hold 3–6 cases, got " + (arr(o.industryCases) ? o.industryCases.length : "none"));
  } else {
    var seenKeys = [];
    o.industryCases.forEach(function (c, i) {
      var cw = w + ".industryCases[" + i + "]";
      if (INDUSTRIES.indexOf(c.industry) === -1) fail(cw, 'industry "' + c.industry + '" is not in the fixed set of 16');
      else if (seenKeys.indexOf(c.industry) !== -1) fail(cw, 'industry "' + c.industry + '" appears twice — one tab per industry');
      else seenKeys.push(c.industry);
      ["label", "image", "problem", "solution"].forEach(function (k) {
        if (!str(c[k])) fail(cw, k + " missing");
      });
      if (str(c.label) && C.shared.industryLabels[c.industry] && c.label !== C.shared.industryLabels[c.industry]) {
        fail(cw, 'label "' + c.label + '" does not match shared.industryLabels.' + c.industry);
      }
      if (str(c.image)) {
        var wantImg = new RegExp("^assets/img/industries/" + c.industry + "\\.(jpg|jpeg|png|webp)$");
        if (!wantImg.test(c.image)) fail(cw, 'image "' + c.image + '" must be assets/img/industries/' + c.industry + ".jpg");
        else checkAsset(cw, "industry image", c.image);
      }
      ["problem", "solution"].forEach(function (k) {
        if (str(c[k]) && (sentences(c[k]) < 2 || sentences(c[k]) > 3)) {
          fail(cw, k + " is " + sentences(c[k]) + " sentences (2–3)");
        }
      });
    });
  }

  /* The At-a-glance card is gone (round 3, H): every fact it denormalised is
     printed by the block that owns it — the chips, the Jumpstart investment
     card, the stack. A summary card that restates them is a second place to
     keep in sync. */
  if (o.sideFacts !== undefined) fail(w, "overview.sideFacts is superseded — the At-a-glance card was removed; nothing renders it");

  /* 3.1 narrative */
  if (!str(t.narrative)) fail(w, "technology.narrative missing");
  else {
    var narrativeSentences = sentences(t.narrative);
    if (narrativeSentences > 3) fail(w, "technology.narrative is " + narrativeSentences + " sentences (max 3)");
  }

  /* The shapes the layered stack and the capability list replaced are gone from
     the data. A re-introduced one would render nowhere and drift out of sync in
     silence. `flow` went with the How-it-runs diagram (the stack reads top to
     bottom instead); `security` went with the Security-and-deployment block,
     its facts folded into the layer summaries, the scope lists and the
     Jumpstart pillars. */
  ["groups", "layers", "integration", "notUsed", "flow", "security"].forEach(function (k) {
    if (t[k] !== undefined) fail(w, "technology." + k + " is superseded — nothing renders it");
  });

  /* E3 · the layered solution stack */
  if (!arr(t.stack) || t.stack.length < 4 || t.stack.length > 5) {
    fail(w, "technology.stack must hold 4–5 layers, got " + (arr(t.stack) ? t.stack.length : "none"));
  } else {
    var lastIdx = -1;
    var sawSoftServe = false;
    t.stack.forEach(function (layer, i) {
      var lw = w + ".stack[" + i + "]";
      var idx = STACK_KEYS.indexOf(layer.key);
      if (idx === -1) return fail(lw, 'key "' + layer.key + '" is not one of ' + STACK_KEYS.join(" / "));
      if (idx <= lastIdx) fail(lw, 'layer "' + layer.key + '" is out of order — the stack renders ' + STACK_KEYS.join(" → "));
      lastIdx = idx;
      ["label", "summary"].forEach(function (k) {
        if (!str(layer[k])) fail(lw, k + " missing");
      });
      if (str(layer.summary) && sentences(layer.summary) > 1) fail(lw, "summary is " + sentences(layer.summary) + " sentences (the accordion row holds one line)");
      if (!arr(layer.vendors) || !layer.vendors.length) fail(lw, "vendors missing — every layer carries at least one vendor mark");
      else layer.vendors.forEach(function (vn) {
        if (STACK_VENDORS.indexOf(vn) === -1) fail(lw, 'vendor "' + vn + '" is not oracle / nvidia / softserve');
        if (vn === "softserve") sawSoftServe = true;
      });
      if (!arr(layer.items) || !layer.items.length) return fail(lw, "items empty");
      var required = 0;
      layer.items.forEach(function (item, j) {
        var iw = lw + ".items[" + j + "]";
        if (!str(item.name)) fail(iw, "name missing");
        if (typeof item.required !== "boolean") fail(iw, "required must be a boolean — Required / Optional is a tag, not a guess");
        else if (item.required) required += 1;
        if (item.direction !== undefined && DIRECTIONS.indexOf(item.direction) === -1) {
          fail(iw, 'direction "' + item.direction + '" is not inbound / outbound / both');
        }
        if (item.direction !== undefined && layer.key !== "custom") {
          fail(iw, "direction belongs on the custom layer — that is where integrations render as Inbound / Outbound lines");
        }
      });
      if (!required) fail(lw, "no Required item — a layer with nothing required is not a layer of this stack");
    });
    var keys = t.stack.map(function (l) { return l.key; });
    ["application", "data-platform", "infrastructure", "custom"].forEach(function (k) {
      if (keys.indexOf(k) === -1) fail(w, 'technology.stack has no "' + k + '" layer');
    });
    if (!sawSoftServe) fail(w, "technology.stack carries no SoftServe vendor mark");
    var custom = t.stack.filter(function (l) { return l.key === "custom"; })[0];
    if (custom && arr(custom.items)) {
      var dirs = custom.items.map(function (x) { return x.direction; }).filter(Boolean);
      if (dirs.indexOf("inbound") === -1 && dirs.indexOf("both") === -1) {
        fail(w, "stack custom layer names no inbound integration");
      }
      if (dirs.indexOf("outbound") === -1 && dirs.indexOf("both") === -1) {
        fail(w, "stack custom layer names no outbound integration");
      }
    }
  }

  /* F · the capability list, grouped by the four workflow stages */
  if (!arr(t.capabilities) || t.capabilities.length !== 4) {
    fail(w, "technology.capabilities must hold exactly 4 workflow stages, got " + (arr(t.capabilities) ? t.capabilities.length : "none"));
  } else {
    var seenStages = [];
    t.capabilities.forEach(function (group, i) {
      var gw = w + ".capabilities[" + i + "]";
      if (!str(group.stage)) fail(gw, "stage missing");
      else if (seenStages.indexOf(group.stage) !== -1) fail(gw, 'stage "' + group.stage + '" appears twice');
      else seenStages.push(group.stage);
      if (!arr(group.items) || group.items.length < 3) fail(gw, "items needs ≥3 capabilities");
      else group.items.forEach(function (item, j) {
        if (!str(item.name)) fail(gw + ".items[" + j + "]", "name missing");
        if (item.state !== undefined && CAP_STATES.indexOf(item.state) === -1) {
          fail(gw + ".items[" + j + "]", 'state "' + item.state + '" is not supported / partial / roadmap — omit the key where no source states one');
        }
      });
    });
  }

  /* G · the Jumpstart Proof-of-Value block */
  if (!v || !Object.keys(v).length) fail(w, "jumpstart missing");
  else {
    ["title", "promise", "cta"].forEach(function (k) {
      if (k === "cta" ? !(v.cta && str(v.cta.label) && str(v.cta.route)) : !str(v[k])) {
        fail(w, "jumpstart." + k + " missing");
      }
    });
    if (str(v.title) && v.title !== "Jumpstart Proof-of-Value") {
      fail(w, 'jumpstart.title is "' + v.title + '" — the block title is the same on all seven');
    }
    if (!arr(v.pillars) || v.pillars.length !== 3) fail(w, "jumpstart.pillars must hold exactly 3");
    else v.pillars.forEach(function (pillar, i) {
      if (pillar.key !== PILLARS[i]) fail(w, 'pillars[' + i + '].key is "' + pillar.key + '", expected "' + PILLARS[i] + '"');
      ["title", "text"].forEach(function (k) {
        if (!str(pillar[k])) fail(w, "pillars[" + i + "]." + k + " missing");
      });
    });
    if (!arr(v.outcomes) || v.outcomes.length < 3 || v.outcomes.length > 4) {
      fail(w, "jumpstart.outcomes must hold 3–4 outcome lines, got " + (arr(v.outcomes) ? v.outcomes.length : "none"));
    }
    if (!arr(v.timeline) || v.timeline.length < 3 || v.timeline.length > 4) {
      fail(w, "jumpstart.timeline must hold 3–4 nodes, got " + (arr(v.timeline) ? v.timeline.length : "none"));
    } else v.timeline.forEach(function (node, i) {
      if (!str(node.label) || !str(node.text)) fail(w, "timeline[" + i + "] needs { label, text }");
    });
    if (!arr(v.needs) || v.needs.length !== 3) fail(w, "jumpstart.needs must hold exactly 3 items");
    var inv = v.investment;
    if (!inv) fail(w, "jumpstart.investment missing");
    else {
      /* A figure is a string or null: where nothing is published the card
         prints one scope line, not two tiles both reading the same
         placeholder. The footnote stays required — it renders with the
         figures, and a figure never renders without it. */
      ["price", "duration"].forEach(function (k) {
        if (!(inv[k] === null || str(inv[k]))) {
          fail(w, "jumpstart.investment." + k + " must be a non-empty string, or null where none is published");
        }
      });
      if (!str(inv.footnote)) fail(w, "jumpstart.investment.footnote missing — a figure never renders without it");
      if (!arr(inv.includes) || inv.includes.length < 3) fail(w, "jumpstart.investment.includes needs ≥3 lines");
      /* One footnote, not a disclaimer stack: the packaging-internal sentences
         were removed site-wide in round 3. */
      if (str(inv.footnote) && sentences(inv.footnote) > 2) {
        fail(w, "jumpstart.investment.footnote is " + sentences(inv.footnote) + " sentences — one footnote line, not a disclaimer stack");
      }
    }
    if (!arr(v.next) || v.next.length !== 2) fail(w, "jumpstart.next must hold exactly 2 steps — Integration and Scale");
    else v.next.forEach(function (step, i) {
      if (step.tier !== NEXT_TIERS[i]) fail(w, 'next[' + i + '].tier is "' + step.tier + '", expected "' + NEXT_TIERS[i] + '"');
      if (!str(step.text)) fail(w, "next[" + i + "].text missing");
      if (!str(step.price)) fail(w, "next[" + i + "].price missing — it reads Scoped per engagement where none is published");
    });
    if (v.cta && str(v.cta.route) && v.cta.route !== "#/products/" + p.slug + "/contacts") {
      fail(w, 'jumpstart.cta.route "' + v.cta.route + '" must point at this product’s contacts tab');
    }
    ["facts", "deliverables", "pricing", "disclaimers", "ladder", "ladderFootnote", "capabilityMatrix", "statStrip", "statNotes", "howItRuns", "prerequisites"].forEach(function (k) {
      if (v[k] !== undefined) fail(w, "jumpstart." + k + " is a superseded POV-tab shape — nothing renders it");
    });
  }

  /* invariants carried over from SCHEMA.md */
  if (!p.tile || !arr(p.tile.outcomes) || p.tile.outcomes.length !== 3) fail(w, "tile.outcomes must hold exactly 3");
});

/* ---- E5 · the contact card ---- */
(function () {
  var k = C.shared && C.shared.contact;
  if (!k) return fail("shared.contact", "missing — the Contacts tab and the Services contact section both render it");
  ["name", "email", "blurb"].forEach(function (f) {
    if (!str(k[f])) fail("shared.contact", f + " missing");
  });
  /* The photo is allowed to be empty — the card falls back to initials — but
     the key must exist so the renderer can test it. */
  if (typeof k.photo !== "string") fail("shared.contact", "photo must be a string (empty when no confirmed headshot ships)");
  else if (!k.photo.trim()) warn("shared.contact", "photo is empty — the card renders the initials avatar");
  /* The title is allowed to be empty — it is only printed when a source
     actually carries it — but the key must exist so the renderer can test it. */
  if (typeof k.title !== "string") fail("shared.contact", "title must be a string (empty when no source states it)");
  else if (!k.title.trim()) warn("shared.contact", "title is empty — the card renders name + email only");
  if (k.email !== "oracle@softserveinc.com") {
    fail("shared.contact", 'email must be the practice mailbox "oracle@softserveinc.com", got "' + k.email + '"');
  }
  if (str(k.blurb) && sentences(k.blurb) > 1) fail("shared.contact", "blurb is more than one line");
  /* E5 / round-3 C: the card is a bounded panel beside the form, and the list
     is what turns "get in touch" into a call someone can prepare for. */
  if (!str(k.bringTitle)) fail("shared.contact", "bringTitle missing — the heading of the Bring-to-the-call list");
  if (!arr(k.bring) || k.bring.length !== 3) fail("shared.contact", "bring must hold exactly 3 items");
  else k.bring.forEach(function (item, i) {
    if (!str(item)) fail("shared.contact", "bring[" + i + "] is not a string");
  });
  if (str(k.photo)) {
    if (!/^assets\/img\/people\/[a-z0-9-]+\.(jpg|jpeg|png|webp)$/.test(k.photo)) {
      fail("shared.contact", 'photo "' + k.photo + '" is not assets/img/people/<name>.<ext>');
    } else checkAsset("shared.contact", "contact photo", k.photo);
  }
  if (k.linkedin !== undefined && !/^https:\/\/([a-z]{2,3}\.)?linkedin\.com\//.test(k.linkedin)) {
    fail("shared.contact", "linkedin, when present, must be a public linkedin.com URL — omit the key otherwise");
  }
  var tabs = (C.shared.productTabs || []).map(function (x) { return x.id; });
  if (tabs.indexOf("contacts") === -1) fail("shared.productTabs", 'no "contacts" tab — the demo tab was renamed in E5');
  if (tabs.indexOf("demo") !== -1) fail("shared.productTabs", 'the "demo" tab id is retired; /demo redirects to /contacts');
  if (tabs.indexOf("jumpstart") === -1) fail("shared.productTabs", 'no "jumpstart" tab — the POV tab was renamed in round 3');
  if (tabs.indexOf("pov") !== -1) fail("shared.productTabs", 'the "pov" tab id is retired; /pov redirects to /jumpstart');
  var jump = (C.shared.productTabs || []).filter(function (x) { return x.id === "jumpstart"; })[0];
  if (jump && jump.legacyId !== "pov") fail("shared.productTabs", 'the jumpstart tab must carry legacyId "pov" so the old route still lands');
  if (!str(C.forms.demo && C.forms.demo.secondaryHeading)) {
    fail("forms.demo", "secondaryHeading missing — the form under the contact card is headed separately");
  }
})();

/* ---- the case-study status words ---- */
(function () {
  var st = (C.shared && C.shared.caseStudyStatus) || {};
  CASE_STATUSES.forEach(function (k, i) {
    if (!st[k]) return;
    if (st[k].chip !== CASE_STATUS_CHIPS[i]) {
      fail("shared.caseStudyStatus." + k, 'chip is "' + st[k].chip + '", expected "' + CASE_STATUS_CHIPS[i] +
        '" — one plain word, not a sentence about the proof of value');
    }
  });
})();

/* ---- no surface states the size of the catalog (2026-09-16) ----
   Seven agents are what is packaged today, not the offering. A total, a
   denominator or a "so far" turns the catalog into a ceiling and invites the
   reader to count what is missing, so none of them ships in copy. */
(function () {
  var pp = C.productsPage || {};
  if (pp.count !== undefined) fail("productsPage.count", "retired — no surface prints the size of the catalog");
  if ((C.facets || {}).footnote !== undefined) {
    fail("facets.footnote", "retired — it existed to explain the platforms with no product, which is the gap the rail no longer shows");
  }
  var strings = [
    ["productsPage.intro", pp.intro],
    ["productsPage.bottomBlock.body", (pp.bottomBlock || {}).body],
    ["productsPage.bottomBlock.heading", (pp.bottomBlock || {}).heading],
    ["overview.twoWays.panels[0].body", (((C.overview || {}).twoWays || {}).panels || [])[0] && C.overview.twoWays.panels[0].body],
    ["overview.catalog.lead", ((C.overview || {}).catalog || {}).lead],
    ["overview.catalog.title", ((C.overview || {}).catalog || {}).title]
  ];
  (C.products || []).forEach(function (pr) {
    strings.push(["products[" + pr.slug + "].overview.metricsNote", (pr.overview || {}).metricsNote]);
  });
  strings.forEach(function (pair) {
    var s = pair[1];
    if (!str(s)) return;
    if (/\b(seven|these seven|four are priced|three are scoped)\b/i.test(s)) {
      fail(pair[0], "states the size of the catalog — say what a reader gets, not how many there are");
    }
    if (/\bso far\b|\byet\b|\bnot seeing\b/i.test(s)) {
      fail(pair[0], "names the gap — the page says what is here, never what is not");
    }
  });
})();

/* ---- T1 · the three tag families ---- */
(function () {
  var tf = C.shared && C.shared.tagFamilies;
  if (!tf) return fail("shared.tagFamilies", "missing — the chip row reads its tooltips and icons from here");
  ["pattern", "tech"].forEach(function (fam) {
    var g = tf[fam];
    if (!g) return fail("shared.tagFamilies." + fam, "missing");
    if (!str(g.tooltip)) fail("shared.tagFamilies." + fam, "tooltip missing — every family names itself on hover");
    if (!g.icons || typeof g.icons !== "object") return fail("shared.tagFamilies." + fam, "icons map missing");
    var want = fam === "pattern" ? PATTERN_IDS : FACET_IDS;
    want.forEach(function (id) {
      if (!str(g.icons[id])) fail("shared.tagFamilies." + fam, 'icons has no entry for "' + id + '"');
    });
    Object.keys(g.icons).forEach(function (id) {
      if (want.indexOf(id) === -1) fail("shared.tagFamilies." + fam, 'icons carries "' + id + '", which is not one of ' + want.join(" / "));
    });
  });
  var av = tf.availability;
  if (!av) return fail("shared.tagFamilies.availability", "missing — the Demo and Marketplace badges read their labels here");
  ["demo", "marketplace"].forEach(function (k) {
    var b = av[k];
    if (!b) return fail("shared.tagFamilies.availability." + k, "missing");
    ["label", "tooltip", "icon"].forEach(function (f) {
      if (!str(b[f])) fail("shared.tagFamilies.availability." + k, f + " missing");
    });
  });
  /* The three-state chip model is gone site-wide. */
  if (C.availability !== undefined) fail("availability", "the availability chip map is superseded by the two badges — nothing renders it");
})();

/* ---- C1 · the case-study status chips ---- */
(function () {
  var st = C.shared && C.shared.caseStudyStatus;
  if (!st) return fail("shared.caseStudyStatus", "missing — the status chip reads its label from here, not from a class");
  CASE_STATUSES.forEach(function (k) {
    if (!st[k]) return fail("shared.caseStudyStatus." + k, "missing");
    ["chip", "tooltip"].forEach(function (f) {
      if (!str(st[k][f])) fail("shared.caseStudyStatus." + k, f + " missing");
    });
  });
  Object.keys(st).forEach(function (k) {
    if (CASE_STATUSES.indexOf(k) === -1) fail("shared.caseStudyStatus", 'carries "' + k + '", which is not ' + CASE_STATUSES.join(" / "));
  });
  if (!str(C.shared.sectionLabels && C.shared.sectionLabels.caseStudy)) {
    fail("shared.sectionLabels", "caseStudy missing — the block title on the Overview tab");
  }
  if (C.shared.sectionLabels && C.shared.sectionLabels.successStory !== undefined) {
    fail("shared.sectionLabels", "successStory is superseded by caseStudy");
  }
})();

/* ---- T2 · the Availability facet group ---- */
(function () {
  var f = C.facets || {};
  if (f.marketplace !== undefined) fail("facets.marketplace", "superseded by facets.availability — the single checkbox became a two-option group");
  var av = f.availability;
  if (!av) return fail("facets.availability", "missing — the rail's Availability group");
  if (!str(av.label)) fail("facets.availability", "label missing");
  if (!arr(av.options) || av.options.length !== 2) return fail("facets.availability", "options must hold exactly 2 checkboxes");
  ["demo", "marketplace"].forEach(function (id, i) {
    if (av.options[i].id !== id) fail("facets.availability", 'options[' + i + '].id is "' + av.options[i].id + '", expected "' + id + '"');
    if (!str(av.options[i].label)) fail("facets.availability", "options[" + i + "].label missing");
  });
})();

/* ---- T3 · the canonical technology set ---- */
(function () {
  var tech = (C.facets || {}).technology;
  if (!arr(tech) || tech.length !== FACET_IDS.length) {
    return fail("facets.technology", "must hold exactly " + FACET_IDS.length + " platforms, got " +
      (arr(tech) ? tech.length : "none"));
  }
  FACET_IDS.forEach(function (id, i) {
    var where = "facets.technology[" + i + "]";
    if (tech[i].id !== id) fail(where, 'id is "' + tech[i].id + '", expected "' + id + '"');
    if (tech[i].label !== FACET_LABELS[id]) {
      fail(where, 'label is "' + tech[i].label + '", expected "' + FACET_LABELS[id] + '"');
    }
    /* The rail carries the one-liner, the grid carries the empty state — a
       facet with no product today still has to say something in both places. */
    ["fullLabel", "description", "emptyState"].forEach(function (k) {
      if (!str(tech[i][k])) fail(where, k + " missing");
    });
  });
  /* "Other" was a catch-all that named no Oracle platform and read as a gap in
     the set. Oracle's product name is "Oracle AI for Fusion Applications". */
  tech.forEach(function (f, i) {
    if (/^other$/i.test(f.id) || /^other\b/i.test(f.label || "")) {
      fail("facets.technology[" + i + "]", 'the "Other" catch-all is retired — the set is the four named Oracle platforms');
    }
  });

  /* The Services platform cards are the same four platforms under another
     shape, so they carry the same labels in the same order — otherwise a reader
     meets one name on the Products rail and a different one on Services. Round
     5 left one such list: `overview.servicesTeaser` is retired, and the home
     page's four platform tiles derive their labels from `facets.technology`
     itself, so they cannot drift from it. */
  (function () {
    var where = "services.hero.platforms";
    var list = ((C.services || {}).hero || {}).platforms;
    if (!arr(list) || list.length !== FACET_IDS.length) {
      return fail(where, "must hold one card per canonical platform (" + FACET_IDS.length + ")");
    }
    FACET_IDS.forEach(function (id, i) {
      if (list[i].name !== FACET_LABELS[id]) {
        fail(where + "[" + i + "]", 'name is "' + list[i].name + '", expected the canonical label "' + FACET_LABELS[id] + '"');
      }
    });
  })();
})();

/* ---- C2 · the home-page case-study cards ---- */
(function () {
  var o = C.overview || {};
  if (o.evidence !== undefined) fail("overview.evidence", "superseded by overview.caseStudies — nothing renders it");
  if (o.evidenceIntro !== undefined) fail("overview.evidenceIntro", "superseded by overview.caseStudiesIntro");
  var intro = o.caseStudiesIntro;
  if (!intro || !str(intro.title) || !str(intro.body)) fail("overview.caseStudiesIntro", "needs { title, body }");
  var cards = o.caseStudies;
  /* The grid is one card per product that carries a case study — derived, not a
     fixed count, so adding or withdrawing a case study moves both surfaces
     together instead of failing the build on an arithmetic constant. */
  var withCase = (C.products || []).filter(function (p) {
    return p.overview && p.overview.caseStudy;
  });
  if (!arr(cards) || cards.length !== withCase.length) {
    return fail("overview.caseStudies", "must hold one card per product that carries a case study (" +
      withCase.length + "), got " + (arr(cards) ? cards.length : "none"));
  }
  var slugs = (C.products || []).map(function (p) { return p.slug; });
  /* …and the cover must be complete in the other direction too: a product with
     a case study the home page never shows is a case study nobody finds. */
  withCase.forEach(function (p) {
    var shown = cards.some(function (c) { return c.product && c.product.slug === p.slug; });
    if (!shown) {
      fail("overview.caseStudies", 'no card for "' + p.slug + '", which carries overview.caseStudy');
    }
  });
  cards.forEach(function (c, i) {
    var cw = "overview.caseStudies[" + i + "]";
    if (c.metricEyebrow !== undefined) {
      fail(cw, "metricEyebrow is retired — the status chip carries the word once");
    }
    ["id", "descriptor", "area", "industry", "status", "line", "footnote"].forEach(function (k) {
      if (!str(c[k])) fail(cw, k + " missing");
    });
    ["customer", "logo", "logoStacked", "band", "label"].forEach(function (k) {
      if (c[k] !== undefined) fail(cw, k + " is superseded — the card is an anonymized medallion card with no logo and no band");
    });
    if (CASE_STATUSES.indexOf(c.status) === -1) fail(cw, 'status "' + c.status + '" is not ' + CASE_STATUSES.join(" / "));
    if (INDUSTRIES.indexOf(c.industry) === -1) fail(cw, 'industry "' + c.industry + '" is not in the fixed set of 16');
    if (!c.metric || !str(c.metric.value) || !str(c.metric.label)) fail(cw, "metric needs { value, label }");
    else if (c.metric.value.length > 20) fail(cw, 'metric.value "' + c.metric.value + '" is too long to set large');
    /* A card whose headline value is words disclaims figures it never shows. */
    if (c.metric && str(c.metric.value) && !/\d/.test(c.metric.value) && /figures are illustrative/i.test(c.footnote || "")) {
      fail(cw, "footnote disclaims figures, but metric.value carries no number — trim the figures clause");
    }
    if (!c.product || !str(c.product.slug) || !str(c.product.name)) fail(cw, "product needs { slug, name }");
    else {
      if (slugs.indexOf(c.product.slug) === -1) fail(cw, 'product.slug "' + c.product.slug + '" is not one of the seven');
      var target = (C.products || []).filter(function (p) { return p.slug === c.product.slug; })[0];
      if (target && target.name !== c.product.name) {
        fail(cw, 'product.name "' + c.product.name + '" does not match products[' + c.product.slug + '].name "' + target.name + '"');
      }
      /* The home card and the product page tell one engagement. A card whose
         product has no case study would link a reader to an empty page. */
      if (target && !(target.overview && target.overview.caseStudy)) {
        fail(cw, 'product "' + c.product.slug + '" has overview.caseStudy null — the home card would link to a page with no case study');
      }
      if (target && target.overview && target.overview.caseStudy) {
        var full = target.overview.caseStudy;
        ["descriptor", "area", "industry", "status"].forEach(function (k) {
          if (full[k] !== c[k]) fail(cw, k + ' disagrees with products[' + c.product.slug + '].overview.caseStudy.' + k);
        });
      }
    }
  });
  /* Services no longer restates the engagements, one line each: since round 6
     the case-study footnotes here carry each engagement's evidence, and
     `services.proof` is checked with the rest of the Services page below. */
})();

/* ---- round 5 · the home page ----
   The seven-screen home page is not a product page, so none of the grammar
   above says anything about it. This block is its contract: one object per
   screen, every key a screen reads asserted here, and every key the old home
   page read failed outright. A retired key that still parses is how a dead
   block comes back — `overview.hero.image` and `overview.servicesTeaser` both
   had renderers a week ago. */
(function () {
  var s = C.site || {};
  var o = C.overview || {};

  function reqStr(where, obj, keys) {
    keys.forEach(function (k) {
      if (!str((obj || {})[k])) fail(where, k + " missing");
    });
  }
  function reqCta(where, cta) {
    if (!cta || !str(cta.label) || !str(cta.route)) fail(where, "needs { label, route }");
  }

  /* --- the shell: the name, the three-item bar and the three CTAs --- */
  ["name", "title", "tagline", "metaDescription"].forEach(function (k) {
    if (!str(s[k])) fail("site", k + " missing");
  });
  /* Two items and no "Overview": the logo is the home link. Case studies left
     the header on 2026-09-17 (Alex) — the home page still carries its
     case-study screen, and Services links to it. For sellers took the slot in
     round 8 and left it the same day (Alex): #/sellers stays, reached from the
     footer's link row and from the Get the full kit link in a product kit
     confirmation. */
  var NAV = [
    { label: "Products", route: "#/products" },
    { label: "Services", route: "#/services" }
  ];
  if (!arr(s.nav) || s.nav.length !== NAV.length) {
    fail("site.nav", "must hold exactly " + NAV.length + " items (Products · Services), got " +
      (arr(s.nav) ? s.nav.length : "none"));
  } else NAV.forEach(function (want, i) {
    var got = s.nav[i] || {};
    if (got.label !== want.label) fail("site.nav[" + i + "]", 'label is "' + got.label + '", expected "' + want.label + '"');
    if (got.route !== want.route) fail("site.nav[" + i + "]", 'route is "' + got.route + '", expected "' + want.route + '"');
  });
  /* Two CTAs, two jobs, and they are not interchangeable: `navCta` is the
     header button, `primaryCta` the label every product hero still carries.
     Round 6 retired `secondaryCta` with the Services hero's quiet button. */
  ["navCta", "primaryCta"].forEach(function (k) {
    reqCta("site." + k, s[k]);
  });
  if (s.secondaryCta !== undefined) fail("site.secondaryCta", "retired in round 6 — the Services hero carries one button");

  /* --- S1 · the hero --- */
  var h = o.hero || {};
  if (!str(h.eyebrow)) fail("overview.hero", "eyebrow missing");
  var hl = h.headline;
  if (!hl || !str(hl.lead) || !str(hl.accent)) {
    fail("overview.hero.headline", "needs { lead, accent } — the white lines, then the teal one that starts its own line");
  } else if (hl.rest !== undefined) {
    fail("overview.hero.headline", "carries the product-hero `rest` key — the home H1 is lead + accent");
  }
  if (!str(h.lead)) fail("overview.hero", "lead missing");
  else if (words(h.lead) > 45) {
    fail("overview.hero", "lead is " + words(h.lead) + " words (max 45 — it sits in a column beside the stack visual)");
  }
  if (!arr(h.ctas) || h.ctas.length !== 2) {
    fail("overview.hero.ctas", "must hold exactly 2 buttons, got " + (arr(h.ctas) ? h.ctas.length : "none"));
  } else h.ctas.forEach(function (c, i) {
    ["label", "route", "kind"].forEach(function (k) {
      if (!str((c || {})[k])) fail("overview.hero.ctas[" + i + "]", k + " missing");
    });
  });
  /* The built-on stack is the only illustration on this page, so its labels are
     copy rather than decoration. The pattern tiles and the platform tiles are
     derived — `facets.categories` and `facets.technology`, whose four labels the
     T3 block already owns — so only the three written strings are asserted. */
  var stack = h.stack;
  if (!stack) fail("overview.hero.stack", "missing — the built-on visual is this hero's only illustration");
  else {
    reqStr("overview.hero.stack", stack, ["ariaLabel", "patternsLabel", "platformsLabel"]);
    var ss = stack.softserve;
    if (!ss) fail("overview.hero.stack.softserve", "missing — the middle band of the three");
    else {
      if (!str(ss.label)) fail("overview.hero.stack.softserve", "label missing");
      if (!arr(ss.items) || ss.items.length !== 3) {
        fail("overview.hero.stack.softserve", "items must hold exactly 3 layer tiles, got " +
          (arr(ss.items) ? ss.items.length : "none"));
      } else ss.items.forEach(function (item, i) {
        if (!str(item)) fail("overview.hero.stack.softserve", "items[" + i + "] is not a string");
      });
    }
  }
  if (!arr(h.stats) || h.stats.length < 3 || h.stats.length > 4) {
    fail("overview.hero.stats", "must hold 3 or 4 tiles — the proof strip under the hero, got " +
      (arr(h.stats) ? h.stats.length : "none"));
  } else h.stats.forEach(function (st, i) {
    var sw = "overview.hero.stats[" + i + "]";
    if (!str((st || {}).value)) fail(sw, "value missing");
    else if (st.value.length > 20) fail(sw, 'value "' + st.value + '" is too long to set large');
    if (!str((st || {}).label)) fail(sw, "label missing");
  });

  /* --- S2 · two ways in --- */
  var tw = o.twoWays;
  if (!tw) fail("overview.twoWays", "missing — S2, the two joined panels");
  else {
    reqStr("overview.twoWays", tw, ["eyebrow", "title"]);
    if (!arr(tw.panels) || tw.panels.length !== 2) {
      fail("overview.twoWays.panels", "must hold exactly 2 panels — products and practice, got " +
        (arr(tw.panels) ? tw.panels.length : "none"));
    } else tw.panels.forEach(function (pn, i) {
      var pw = "overview.twoWays.panels[" + i + "]";
      reqStr(pw, pn, ["id", "icon", "title", "body"]);
      /* Peers: three bullets each, so the two panels are one shape and their
         CTAs land on one baseline. */
      if (!arr(pn.bullets) || pn.bullets.length !== 3) {
        fail(pw, "bullets must hold exactly 3 — the two panels are peers, got " +
          (arr(pn.bullets) ? pn.bullets.length : "none"));
      } else pn.bullets.forEach(function (b, j) {
        if (!str(b)) fail(pw, "bullets[" + j + "] is not a string");
      });
      reqCta(pw + ".cta", pn.cta);
    });
  }

  /* --- S3 · the product catalog, three columns --- */
  var cat = o.catalog;
  if (!cat) fail("overview.catalog", "missing — S3, the products screen");
  else {
    reqStr("overview.catalog", cat, ["eyebrow", "title", "lead"]);
    reqCta("overview.catalog.cta", cat.cta);
    /* One column per workflow pattern, in the order the rest of the site lists
       them. The rows inside a column are derived — the products whose
       `category` is this pattern, in `SITE_CONFIG.productOrder` — so the data
       carries the definition and nothing else. */
    if (!arr(cat.patterns) || cat.patterns.length !== PATTERN_IDS.length) {
      fail("overview.catalog.patterns", "must hold one column per workflow pattern (" + PATTERN_IDS.length + "), got " +
        (arr(cat.patterns) ? cat.patterns.length : "none"));
    } else PATTERN_IDS.forEach(function (id, i) {
      var col = cat.patterns[i] || {};
      var cw = "overview.catalog.patterns[" + i + "]";
      if (col.id !== id) fail(cw, 'id is "' + col.id + '", expected "' + id + '" — the columns render in facets.categories order');
      if (!str(col.definition)) fail(cw, "definition missing — the column header is the pattern name and this line");
    });
  }

  /* --- S4 · how we deliver --- */
  var d = o.delivery;
  if (!d) fail("overview.delivery", "missing — S4, the ladder and the three pillars");
  else {
    reqStr("overview.delivery", d, ["eyebrow", "title"]);
    if (d.anchor !== "how-we-deliver") {
      fail("overview.delivery", 'anchor is "' + d.anchor + '", expected "how-we-deliver" — the hero CTA and the S2 practice panel both link to it');
    }
    if (!arr(d.steps) || d.steps.length !== 3) {
      fail("overview.delivery.steps", "must hold exactly 3 steps — proof of value, integration, scale, got " +
        (arr(d.steps) ? d.steps.length : "none"));
    } else d.steps.forEach(function (st, i) {
      reqStr("overview.delivery.steps[" + i + "]", st, ["title", "body", "factLabel", "fact"]);
    });
    /* Rule 1 of VISUAL-GRAMMAR: every step's `fact` carries a duration and the
       first one carries a price, and this block has no other caveat row. */
    if (!str(d.footnote)) {
      fail("overview.delivery", "footnote missing — the step facts carry durations and a price, and a number never renders without its caveat in the same block");
    }
    var why = d.why;
    if (!why) fail("overview.delivery.why", "missing — the three pillars beside the ladder");
    else {
      if (!str(why.title)) fail("overview.delivery.why", "title missing");
      if (!arr(why.pillars) || why.pillars.length !== 3) {
        fail("overview.delivery.why.pillars", "must hold exactly 3 pillars, got " +
          (arr(why.pillars) ? why.pillars.length : "none"));
      } else why.pillars.forEach(function (p, i) {
        reqStr("overview.delivery.why.pillars[" + i + "]", p, ["icon", "title", "body"]);
      });
    }
    if (!arr(d.ctas) || d.ctas.length < 1 || d.ctas.length > 2) {
      fail("overview.delivery.ctas", "must hold 1 or 2 — the screen ends on one action, got " +
        (arr(d.ctas) ? d.ctas.length : "none"));
    } else d.ctas.forEach(function (c, i) {
      reqCta("overview.delivery.ctas[" + i + "]", c);
    });
  }

  /* --- S5 · the case-study rail (the cards themselves are checked in C2) --- */
  reqStr("overview.caseStudiesIntro", o.caseStudiesIntro, ["eyebrow", "title", "body", "ndaLine"]);
  reqCta("overview.caseStudiesIntro.cta", (o.caseStudiesIntro || {}).cta);

  /* --- S6 · about SoftServe, the page's one light band --- */
  var ab = o.about;
  if (!ab) fail("overview.about", "missing — S6, the light band");
  else {
    reqStr("overview.about", ab, ["eyebrow", "title", "body", "partnerLine"]);
    /* Corporate figures only where softserveinc.com prints them — a tile with
       no public source is left out rather than filled from memory. */
    if (!arr(ab.stats) || ab.stats.length < 1 || ab.stats.length > 4) {
      fail("overview.about.stats", "must hold 1–4 tiles, got " + (arr(ab.stats) ? ab.stats.length : "none"));
    } else ab.stats.forEach(function (st, i) {
      var aw = "overview.about.stats[" + i + "]";
      if (!str((st || {}).value)) fail(aw, "value missing");
      else if (st.value.length > 12) fail(aw, 'value "' + st.value + '" is too long for a tile in the 2×2 grid');
      if (!str((st || {}).label)) fail(aw, "label missing");
    });
    if (!arr(ab.partners) || !ab.partners.length) {
      fail("overview.about.partners", "needs at least one wordmark — the partner strip is what `partnerLine` labels");
    } else ab.partners.forEach(function (pt, i) {
      var pw = "overview.about.partners[" + i + "]";
      if (!str((pt || {}).name)) fail(pw, "name missing — it is the image's alt text");
      if (!str((pt || {}).file)) fail(pw, "file missing");
      else if (pt.file.indexOf("assets/img/") !== 0) {
        fail(pw, 'file "' + pt.file + '" must be a path under assets/img/');
      } else if (pt.file.indexOf("logos/") !== -1) {
        fail(pw, 'file "' + pt.file + '" is under assets/img/logos/ — those are customer marks and stay unreferenced');
      } else {
        checkAsset(pw, "partner wordmark", pt.file);
      }
      /* Both dimensions ship so the strip reserves its space and does not
         reflow the band when the SVGs arrive. */
      ["width", "height"].forEach(function (k) {
        if (typeof (pt || {})[k] !== "number") fail(pw, k + " must be a number");
      });
    });
    if (!ab.link || !str(ab.link.label) || !str(ab.link.url)) fail("overview.about.link", "needs { label, url }");
    else if (ab.link.url.indexOf("https://www.softserveinc.com") !== 0) {
      fail("overview.about.link", 'url "' + ab.link.url + '" must be on https://www.softserveinc.com — the block links to the site that prints the figures');
    }
  }

  /* --- S7 · contact --- */
  var ct = o.contact;
  if (!ct) fail("overview.contact", "missing — S7, the contact split");
  else {
    if (ct.anchor !== "request-a-demo") {
      fail("overview.contact", 'anchor is "' + ct.anchor + '", expected "request-a-demo" — every product page deep-links to #/#request-a-demo');
    }
    reqStr("overview.contact", ct, ["heading", "sub"]);
  }

  /* --- what the old home page carried, and must not carry again --- */
  [
    ["trustStrip", "the three-wordmark strip — the partner wordmarks sit inside the About band now"],
    ["productsIntro", "the products intro — S3's head is overview.catalog"],
    ["servicesTeaser", "the platform-card teaser — S4 is overview.delivery, and the four platform cards live on Services"]
  ].forEach(function (pair) {
    if (o[pair[0]] !== undefined) {
      fail("overview." + pair[0], "is superseded by the round-5 home page (" + pair[1] + ") — nothing renders it");
    }
  });
  [
    ["image", "the home hero carries no photograph — the built-on stack visual is its illustration"],
    ["subhead", "the hero's copy is headline + lead"]
  ].forEach(function (pair) {
    if (h[pair[0]] !== undefined) fail("overview.hero." + pair[0], "is superseded — " + pair[1]);
  });

  /* --- the catalog rows read one new string per product --- */
  (C.products || []).forEach(function (p) {
    var pw = "products[" + p.slug + "]";
    if (!str(p.shortLine)) return fail(pw, "shortLine missing — the home catalog row's one line under the product name");
    if (words(p.shortLine) > 12) {
      fail(pw, "shortLine is " + words(p.shortLine) + ' words (max 12): "' + p.shortLine + '"');
    }
    if (p.shortLine.trim().slice(-1) !== ".") {
      fail(pw, "shortLine does not end in a period — the seven rows are sentences and sit directly beneath each other");
    }
    if (str(p.oneLiner) && p.shortLine.trim() === p.oneLiner.trim()) {
      fail(pw, "shortLine repeats oneLiner — the row carries the short form, the tile and the hero keep the full one");
    }
  });

  /* --- every icon the two new screens name is in the registry --- */
  var namedIcons = [];
  ((tw || {}).panels || []).forEach(function (pn, i) {
    if (str((pn || {}).icon)) namedIcons.push(["overview.twoWays.panels[" + i + "]", pn.icon]);
  });
  (((d || {}).why || {}).pillars || []).forEach(function (p, i) {
    if (str((p || {}).icon)) namedIcons.push(["overview.delivery.why.pillars[" + i + "]", p.icon]);
  });
  /* CHANGE 6 — guarded: a tree without the renderer warns instead of throwing. */
  var appPath = path.join(SITE_DIR, "assets/app.js");
  if (!fs.existsSync(appPath)) return warn("icons", "assets/app.js not found at " + appPath + " — icon keys unchecked");
  var appSrc = fs.readFileSync(appPath, "utf8");
  var iconKeys = [];
  var iconRe = /^\s{4}"?([A-Za-z-]+)"?:\s*'/gm;
  var hit;
  while ((hit = iconRe.exec(appSrc))) iconKeys.push(hit[1]);
  /* The data layer has twice moved ahead of the icon registry (round 4's eight
     tag glyphs, round 5's `arrowDown` and `cube`). This list is where a key
     the renderer has not drawn yet is downgraded to a warning; it is EMPTY,
     because both round-5 icons are in assets/app.js. Put a key here only while
     it is genuinely in flight, and take it out in the same change that draws
     it — a name that stays here is an unchecked icon. */
  var PENDING_ICONS = [];
  if (!iconKeys.length) {
    warn("assets/app.js", "no ICONS entries matched — the registry's shape changed and this check is reading nothing");
  } else namedIcons.forEach(function (pair) {
    if (iconKeys.indexOf(pair[1]) !== -1) return;
    if (PENDING_ICONS.indexOf(pair[1]) !== -1) {
      warn(pair[0], 'icon "' + pair[1] + '" is not in the ICONS registry in site/assets/app.js yet — it lands with the round-5 renderer');
    } else {
      fail(pair[0], 'icon "' + pair[1] + '" is not a key of the ICONS registry in site/assets/app.js');
    }
  });

  /* --- HANDOFF §6.1: the words this page does not use ---
     Scoped to `overview` on purpose: the ban is for home-page marketing copy.
     (The seller gate that honestly "unlocked" a panel was retired in round 8 for
     the sales-kit request.) */
  var homeRaw = JSON.stringify(o).toLowerCase();
  ["cutting-edge", "seamless", "unlock", "empower", "revolutionary"].forEach(function (word) {
    if (homeRaw.indexOf(word) !== -1) {
      fail("overview", 'carries the banned word "' + word + '" (HANDOFF §6.1) — name the specific thing instead');
    }
  });
})();

/* ---- banned strings, site-wide ----
   CHANGE 4 — the generic bans stay inline: they carry no identity and they are
   true of any practice site. The identity-bearing ones the original listed here
   (an internal company name, internal deal vocabulary, three € figures out of a
   confidential business case, a third-party product named inside a customer's
   own estate, a personal mailbox) move into the deny-list file, where each site
   keeps its own. The practice mailbox is asserted structurally further up, so a
   personal address cannot quietly replace it. */
var raw = fs.readFileSync(CONTENT_PATH, "utf8");
[
  ["Framed scope", "packaging-internal disclaimer"],
  ["flexible add-ons", "packaging-internal disclaimer"],
  ["beyond the frame", "packaging-internal disclaimer"],
  ["set by specific constraints", "packaging-internal disclaimer"],
  ["TODO", "internal marker"],
  ["(assumed)", "internal marker"],
  ["AIDP", "internal abbreviation; write Oracle AI Data Platform"],
  ["modelled", "British spelling — the corpus is US English (modeled)"],
  ["minimis", "British spelling — the corpus is US English (minimize)"],
  ["optimis", "British spelling — the corpus is US English (optimize)"],
  ["organis", "British spelling — the corpus is US English (organize)"],
  ["normalis", "British spelling — the corpus is US English (normalize)"],
  ["enquir", "British spelling — the corpus is US English (inquiry)"],
  ["catalogue", "British spelling — the corpus is US English (catalog)"],
  ["prioritis", "British spelling — the corpus is US English (prioritize)"]
].concat(DENY.bannedStrings).forEach(function (pair) {
  if (!pair || !pair[0]) return;
  if (raw.indexOf(pair[0]) !== -1) {
    fail("content.js", 'contains banned string "' + pair[0] + '" (' + (pair[1] || "deny-list") + ")");
  }
});

/* ---- rounds 6–7 · the Services page (2026-09-16, 2026-09-17) ----
   Three screens and the contact block, one message each (round 7, Alex): AI
   depth with Oracle expertise — the practice (hero and band); it's all about
   ROI — every step ends in a number (the step track); a fast proof of value,
   no hassle (the light band and two panels). The steps the page shares with
   the home track carry the home page's names, Discovery may lead them, and the
   anchors other pages link to are asserted against the routes that point at
   them (PROVENANCE §21, §23). */
(function () {
  var s = C.services || {};
  var site = C.site || {};
  var shared = C.shared || {};

  ["whatWeDo", "whySoftServe"].forEach(function (k) {
    if (s[k] !== undefined) fail("services." + k, "retired in round 6 — its substance moved into the hero or left the page (PROVENANCE §21)");
  });
  ["afterGoLive", "proof"].forEach(function (k) {
    if (s[k] !== undefined) fail("services." + k, "retired in round 7 — after go-live folds into the Scale step, the measurement into the step track, the proof into proofOfValue (PROVENANCE §23)");
  });
  if (site.dividerLabels !== undefined) fail("site.dividerLabels", "retired in round 6 — nothing renders the rule–label–rule divider");
  if (shared.ladderColumns !== undefined) fail("shared.ladderColumns", "retired in round 6 — Services renders the home step track, not a ladder table");

  var h = s.hero || {};
  ["lead", "secondParagraph", "platformsTitle"].forEach(function (k) {
    if (!str(h[k])) fail("services.hero", k + " missing");
  });
  if (!h.headline || !str(h.headline.accent) || !str(h.headline.rest)) fail("services.hero.headline", "needs { accent, rest }");
  if (!arr(h.stats) || !h.stats.length) fail("services.hero.stats", "missing");
  (h.platforms || []).forEach(function (platform, i) {
    if (platform.short !== undefined || platform.long !== undefined) {
      fail("services.hero.platforms[" + i + "]", "short/long retired in round 6 — the platforms render as chips");
    }
  });
  if (!h.cta || !str(h.cta.label) || !str(h.cta.route)) fail("services.hero.cta", "needs { label, route }");

  var e = s.howWeEngage || {};
  ["anchor", "eyebrow", "title", "lead", "footnote"].forEach(function (k) {
    if (!str(e[k])) fail("services.howWeEngage", k + " missing");
  });
  ["ladder", "ladderRules", "ladderFootnote", "howAPovRuns"].forEach(function (k) {
    if (e[k] !== undefined) fail("services.howWeEngage." + k, "retired in round 6 — the step track replaces the ladder");
  });
  var homeSteps = ((C.overview || {}).delivery || {}).steps || [];
  var steps = arr(e.steps) ? e.steps : [];
  var offset = steps.length - homeSteps.length;
  if (offset < 0 || offset > 1 || (offset === 1 && (steps[0] || {}).title !== "Discovery")) {
    fail("services.howWeEngage.steps", "must be the home delivery steps (" + homeSteps.length + "), optionally led by Discovery");
  } else steps.forEach(function (step, i) {
    var where = "services.howWeEngage.steps[" + i + "]";
    ["title", "body", "factLabel", "fact"].forEach(function (k) {
      if (!str(step[k])) fail(where, k + " missing");
    });
    /* One word for one thing: the steps both pages show carry the same names. */
    var home = homeSteps[i - offset];
    if (home && step.title !== home.title) {
      fail(where, 'title is "' + step.title + '", but the home step is "' + home.title + '"');
    }
  });

  var pov = s.proofOfValue || {};
  ["anchor", "eyebrow", "title", "lead", "footnote"].forEach(function (k) {
    if (!str(pov[k])) fail("services.proofOfValue", k + " missing");
  });
  if (!pov.stat || !str(pov.stat.value) || !str(pov.stat.label)) {
    fail("services.proofOfValue", "stat needs { value, label } — the duration, set as the band's figure");
  }
  if (!pov.cta || !str(pov.cta.label) || !str(pov.cta.route)) {
    fail("services.proofOfValue", "cta needs { label, route } — the link to the case studies that carry the figures");
  }
  if (!arr(pov.panels) || pov.panels.length !== 2) {
    fail("services.proofOfValue.panels", "must hold two panels — what the customer brings, and what they leave with");
  } else pov.panels.forEach(function (panel, i) {
    var where = "services.proofOfValue.panels[" + i + "]";
    ["id", "icon", "title", "body"].forEach(function (k) {
      if (!str(panel[k])) fail(where, k + " missing");
    });
    if (!arr(panel.bullets) || !panel.bullets.length) fail(where, "bullets missing");
    if (panel.cta !== undefined) fail(where, "carries a cta — the contact block is the page's one ask");
  });

  /* The routes other pages use to land here must keep resolving. */
  var anchors = [e.anchor, pov.anchor, ((C.forms || {}).contact || {}).anchor];
  [
    ["shared.engageLink.route", (shared.engageLink || {}).route],
    ["overview.caseStudiesIntro.cta.route", (((C.overview || {}).caseStudiesIntro || {}).cta || {}).route],
    ["site.navCta.route", (site.navCta || {}).route]
  ].forEach(function (pair) {
    var m = /^#\/services#([a-z0-9-]+)$/.exec(pair[1] || "");
    if (m && anchors.indexOf(m[1]) === -1) fail(pair[0], '"' + pair[1] + '" points at an anchor the Services page no longer has');
  });
  if (/\bpackages?\b/i.test((shared.engageLink || {}).label || "")) {
    fail("shared.engageLink.label", "says package — packaging vocabulary stays internal");
  }
})();

/* ---- round 7 · one proof-of-value duration (Alex, 2026-09-17) ----
   "Make sure that we always mention 4–8 weeks PoV, consistently across the
   site": every Jumpstart states it in its promise, its short form (which the
   seller CTA interpolates) and its investment figure; the home hero tile, the
   home step track and the Services page carry it; and no other proof-of-value
   duration survives anywhere in the data (PROVENANCE §23). */
(function () {
  var POV = "4–8 weeks";
  (C.products || []).forEach(function (p) {
    var j = p.jumpstart || {};
    var where = "products[" + p.slug + "].jumpstart";
    if (j.durationShort !== POV) fail(where + ".durationShort", '"' + j.durationShort + '" — the proof of value is "' + POV + '" everywhere');
    if (!j.investment || j.investment.duration !== POV) fail(where + ".investment.duration", 'must be "' + POV + '"');
    if (!str(j.promise) || j.promise.indexOf(POV) === -1) fail(where + ".promise", 'must state "' + POV + '"');
    var fast = (j.pillars || []).filter(function (x) { return x.key === "fast"; })[0];
    if (fast && !/4–8 weeks|Four weeks/.test(fast.text || "")) fail(where + ".pillars[fast]", "must state the " + POV + " duration");
  });
  var o = C.overview || {};
  var step = ((o.delivery || {}).steps || [])[0];
  if (!step || step.fact !== POV) fail("overview.delivery.steps[0].fact", 'must be "' + POV + '"');
  if (!((o.hero || {}).stats || []).some(function (s) { return s.value === POV; })) {
    fail("overview.hero.stats", 'lost the "' + POV + '" tile');
  }
  if (JSON.stringify(C.services || {}).indexOf(POV) === -1) fail("services", 'never states the "' + POV + '" proof of value');
  var povStat = ((C.services || {}).proofOfValue || {}).stat;
  if (povStat && povStat.value !== POV) fail("services.proofOfValue.stat.value", 'must be "' + POV + '"');
  var other = raw.match(/30[–-]45 days|about two months|in 2 months|Two months from kickoff|\b12 weeks\b|two-week acceptance|duration is set at scoping/);
  if (other) fail("content.js", 'carries another proof-of-value duration ("' + other[0] + '") — it is "' + POV + '" across the site');
})();

/* ---- round 8 · the sales kit (Alex, 2026-09-17) ----
   The For sellers tab and the #/sellers page request the kit by work email;
   eligibility is the domain, not a declared role. Only the auto-send
   confirmation may say the kit was emailed (PROVENANCE §24). */
(function () {
  if (C.sellerGate !== undefined) fail("sellerGate", "retired in round 8 — the kit request copy lives in salesKit");
  var kit = C.salesKit || {};
  var page = kit.page || {};
  var tab = kit.tab || {};
  var form = kit.form || {};
  function need(where, obj, keys) {
    keys.forEach(function (k) { if (!str(obj[k])) fail(where, k + " missing"); });
  }
  function token(where, value, name) {
    if (str(value) && value.indexOf("{" + name + "}") === -1) fail(where, "must carry {" + name + "}");
  }
  need("salesKit.page", page, ["eyebrow", "title", "body", "again", "povTitle", "povBody", "povLink"]);
  if (!page.routeLink || !str(page.routeLink.label) || !str(page.routeLink.route)) fail("salesKit.page.routeLink", "needs { label, route }");
  need("salesKit.tab", tab, ["title", "body", "routeLabel", "nextDemo", "nextDemoLink", "nextAll", "nextAllLink"]);
  token("salesKit.tab.body", tab.body, "product");
  token("salesKit.tab.nextDemo", tab.nextDemo, "link");
  token("salesKit.tab.nextAll", tab.nextAll, "link");
  need("salesKit.form", form, ["emailLabel", "emailPlaceholder", "productLabel", "productAll", "submit", "submitting",
    "eligibility", "otherRoute", "kitName", "kitNameAll", "mailSubject", "mailSubjectAll", "mailBody"]);
  token("salesKit.form.otherRoute", form.otherRoute, "routeLink");
  token("salesKit.form.kitName", form.kitName, "product");
  token("salesKit.form.mailSubject", form.mailSubject, "product");
  need("salesKit.form.errors", form.errors || {}, ["email", "domain", "send"]);
  token("salesKit.form.errors.domain", (form.errors || {}).domain, "routeLink");
  var conf = form.confirmations || {};
  ["sent", "queued", "mailto"].forEach(function (k) {
    var c = conf[k] || {};
    if (!str(c.title) || !str(c.body)) return fail("salesKit.form.confirmations." + k, "needs { title, body }");
    token("salesKit.form.confirmations." + k, c.body, "kitName");
    if (k !== "sent" && /we[’']ve emailed|we have emailed|has been (sent|emailed)/i.test(c.body)) {
      fail("salesKit.form.confirmations." + k, "claims the kit was emailed — only `sent` may, and only when an auto-sender is configured");
    }
  });

  /* Sellers and partners are different readers: the kit goes to seller domains only. */
  var roles = (C.forms || {}).roles || [];
  ["oracle-seller", "oracle-partner"].forEach(function (value) {
    if (!roles.some(function (r) { return r.value === value; })) fail("forms.roles", 'missing "' + value + '"');
  });
  roles.forEach(function (r) {
    if (/or partner/i.test(r.label || "")) fail("forms.roles", '"' + r.label + '" lumps sellers and partners together');
  });

  var footerLink = (((C.site || {}).footer) || {}).sellersLink;
  if (!footerLink || footerLink.route !== "#/sellers" || !str(footerLink.label)) {
    fail("site.footer.sellersLink", 'needs { label, route: "#/sellers" }');
  }
  var sellersTab = (((C.shared || {}).productTabs) || []).filter(function (t) { return t.id === "sellers"; })[0];
  if (sellersTab && sellersTab.locked) fail("shared.productTabs[sellers]", "locked retired in round 8 — the tab is a request form, nothing is locked");
})();

/* Round 4 (Alex, 2026-09-16): NO customer may be named anywhere in the shipped
   data — not in copy, not in alt text, not in a caption — and no customer logo
   may be referenced. The logo files stay in the repo, unreferenced, pending
   customer approval — since 2026-09-17 in docs/asset-candidates/logos/, outside
   the deployable root, because whole-tree publishes had carried them onto the
   link-shared preview (PROVENANCE §25). */
if (fs.existsSync(path.join(SITE_DIR, "assets/img/logos"))) {
  fail("site/assets/img/logos/", "exists again — customer marks live in docs/asset-candidates/logos/, outside site/, so no publish or deploy can carry them");
}
CUSTOMER_NAMES.forEach(function (name) {
  if (new RegExp("\\b" + name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b").test(raw)) {
    fail("content.js", 'names the customer "' + name + '" — the site describes every customer by industry and scale only');
  }
});
if (/assets\/img\/logos\//.test(raw)) {
  fail("content.js", "references assets/img/logos/ — customer marks stay on disk, unreferenced, pending customer approval");
}

/* The Internal review panel (2026-09-17, docs/START-HERE.md §8) is temporary,
   for the prototype only. While index.html loads it, the list must be well
   formed and name no customer, and every run warns, so it cannot reach a
   launch unnoticed. */
(function () {
  /* CHANGE 6 — guarded. */
  var indexPath = path.join(SITE_DIR, "index.html");
  if (!fs.existsSync(indexPath)) return;
  var html = fs.readFileSync(indexPath, "utf8");
  var loadsData = html.indexOf('<script src="data/review.js"></script>') !== -1;
  var loadsPanel = html.indexOf('<script src="assets/review.js"></script>') !== -1;
  if (!loadsData && !loadsPanel) return;
  if (loadsData !== loadsPanel) {
    fail("index.html", "loads only one of data/review.js and assets/review.js — the Internal panel is added and removed as a pair");
    return;
  }
  var reviewRaw = fs.readFileSync(path.join(SITE_DIR, "data/review.js"), "utf8");
  var box = { window: {} };
  vm.createContext(box);
  try {
    vm.runInContext(reviewRaw, box, { filename: "site/data/review.js" });
  } catch (e) {
    fail("data/review.js", "does not load: " + e.message);
    return;
  }
  var R = box.window.SITE_REVIEW;
  if (!R || !Array.isArray(R.groups) || !R.groups.length) {
    fail("data/review.js", "window.SITE_REVIEW.groups must be a non-empty array");
    return;
  }
  /* Alex, 2026-09-17: "much less verbose (1-2 line items)". An item is a
     line to tick, not an analysis: id, text, and at most a short note on
     where the site does not match yet. The ticks themselves live in each
     viewer's browser, not in this file. */
  var ITEM_KEYS = ["id", "text", "note"];
  var TEXT_MAX = 70;
  var TEXT_WITH_NOTE_MAX = 47;
  var NOTE_MAX = 45;
  var ids = {};
  R.groups.forEach(function (group, gi) {
    var where = "review.groups[" + gi + "]";
    if (!group.title || !String(group.title).trim()) fail(where, "title is empty");
    if (!Array.isArray(group.items) || !group.items.length) { fail(where, "has no items"); return; }
    group.items.forEach(function (item, ii) {
      var at = where + ".items[" + ii + "]";
      Object.keys(item || {}).forEach(function (key) {
        if (ITEM_KEYS.indexOf(key) === -1) fail(at, 'key "' + key + '" — an item is only ' + ITEM_KEYS.join(", ") + " (1–2 lines; detail belongs in the docs)");
      });
      if (!item.id || !/^[a-z0-9-]+$/.test(item.id)) fail(at, "id must be kebab-case");
      else if (ids[item.id]) fail(at, 'duplicate id "' + item.id + '" — ticks are saved by id');
      else ids[item.id] = true;
      if (!item.text || !String(item.text).trim()) fail(at, "text is empty");
      else if (item.text.length > (item.note ? TEXT_WITH_NOTE_MAX : TEXT_MAX)) {
        fail(at, "text runs " + item.text.length + " characters — keep it to " + (item.note ? TEXT_WITH_NOTE_MAX + " beside a note (one line at the panel's width)" : TEXT_MAX));
      }
      if (item.note != null && (!String(item.note).trim() || item.note.length > NOTE_MAX)) {
        fail(at, "note must be non-empty and " + NOTE_MAX + " characters at most");
      }
    });
  });
  CUSTOMER_NAMES.forEach(function (name) {
    if (new RegExp("\\b" + name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "\\b").test(reviewRaw)) {
      fail("data/review.js", 'names the customer "' + name + '" — the panel is visible to anyone with the preview link');
    }
  });
  if (R.enabled !== false) {
    warn("Internal review panel", "on, " + Object.keys(ids).length + " items — delete data/review.js, assets/review.js and their script tags before launch");
  }
})();

/* CHANGE 4 — an unconfigured deny-list is the one failure mode that ships a
   customer name, so it says so on every run rather than passing in silence. */
if (!CUSTOMER_NAMES.length) {
  warn("deny-list", "no customer names configured" + (denyNote ? " (" + denyNote + ")" : "") +
    " — create <site-root>/tools/deny-list.json or pass --deny-list; the customer-name gate is not running");
}

if (warnings.length) {
  console.warn("check-grammar: " + warnings.length + " warning(s)");
  warnings.forEach(function (x) { console.warn("  ! " + x); });
  console.warn("");
}

if (failures.length) {
  console.error("check-grammar: " + failures.length + " failure(s)\n");
  failures.forEach(function (f) { console.error("  ✗ " + f); });
  process.exit(1);
}
/* CHANGE 5 — the count is read from the data, not written into the message. */
var okN = (C.products || []).length;
console.log("check-grammar: OK — " + okN + " product" + (okN === 1 ? "" : "s") + ", every grammar slot filled.");
