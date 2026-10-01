#!/usr/bin/env node
/**
 * insert-product.mjs — splice one product entry into a practice site's data files.
 *
 *   node insert-product.mjs --entry entry.js --content <site>/site/data/content.js \
 *        --figure-alt "<one sentence describing the architecture figure>" \
 *        [--case-card card.js] \
 *        [--config <site>/site/data/config.js --config-entry entry.js] \
 *        [--links <site>/links.json [--demo-path demo/<slug>/index.html]] \
 *        [--before <slug>] [--dry-run]
 *
 * WHY A TOOL. The entry goes inside `products: [ … ]`, which is 2,000 lines into
 * a 190 KB file whose last element has no trailing comma. Hand-editing it is how
 * a build breaks silently: an entry pasted after the closing bracket parses fine
 * and renders nothing. This does the splice, then re-runs the file through a
 * sandbox and refuses to write unless the catalog actually grew by one. With
 * --links it also writes the product's kit-links entry (site round 12), because
 * the site's checker fails a product that has none, and a step done by hand is
 * the step a rebuild forgets.
 *
 * WHAT IT REFUSES TO DO
 *   - overwrite a slug that already exists (there is no --force: replacing an
 *     entry is an edit of the site's own copy, made in the site's own repo);
 *   - write anything when content.js, before or after the splice, does not
 *     evaluate — the site's assets/brand.js runs first, as in the site's own
 *     tools — or when the product count did not go up by exactly one;
 *   - touch config.js unless both --config and --config-entry are given;
 *   - write an entry with no `contactPerson`, or one that is not an id in the site's
 *     `shared.people` (site round 13), where the site defines `shared.people`;
 *   - insert a product with no `--figure-alt` where content.js has a `media` map: the
 *     product page draws its architecture figure only through `media["<slug>"]`, so a
 *     product without that entry renders with no figure and nothing reports it;
 *   - insert a product whose `overview.caseStudy` is not null, where content.js shows
 *     home case cards (`overview.caseStudies`), without `--case-card`: the site shows
 *     one home card per case study and its checker fails a missing one; and take a
 *     `--case-card` for a product with no case study, which would link to nothing;
 *   - add a kit-links entry that links.json already carries, or write to a
 *     links.json that is not valid JSON or has no `products` object. Every
 *     refusal comes before the first write: a refused run writes nothing anywhere.
 *
 * INPUTS
 *   --entry <file>         a file holding ONE product object literal. Leading and
 *                          trailing comments are fine, and so are the extra blocks
 *                          of an exemplar tools/exemplar.mjs wrote: the first balanced
 *                          {...} carrying a `slug:` key — bare, or JSON-quoted
 *                          `"slug":` as the generated exemplar writes it — is taken
 *                          and the rest ignored.
 *   --content <file>       the target site/data/content.js.
 *   --figure-alt <text>    the architecture figure's one-sentence description. Adds
 *                          `media["<slug>"] = { diagram: "<slug>", alt: <text> }`, which
 *                          is how the product page finds the figure in diagrams.js.
 *   --case-card <file>     the home case card's copy, for a product with a case study:
 *                          one object literal `{ line, metric: { label }, id? }`. The
 *                          card is appended to content.js `overview.caseStudies` with
 *                          everything else taken from the entry itself — descriptor,
 *                          area, industry, status, `metric.value` (its case study's
 *                          first figure) and `product { slug, name }` — so the two
 *                          surfaces cannot disagree. `id` defaults to "<slug>-case".
 *   --config <file>        the target site/data/config.js (optional).
 *   --config-entry <file>  a file holding ONE `"<slug>": { … }` switch block, or
 *                          the exemplar file, from which the block whose key is
 *                          this slug is taken (optional; requires --config).
 *                          The slug is also appended to `productOrder`.
 *   --links <file>         the site's links.json, at the repo root (optional).
 *                          Adds `products["<slug>"]` with the six kit keys in the
 *                          site's order, every one "" until its artifact exists.
 *   --demo-path <path>     the walkthrough's path inside the publish root, written
 *                          as `interactiveDemo` (optional; requires --links). Pass
 *                          it only once the walkthrough is on disk: the site's
 *                          sync-links step fails a path that is not.
 *   --before <slug>        insert before that entry instead of at the end of the array.
 *   --dry-run              report what would change; write nothing.
 *
 * BACKUPS. Every file a run changes is copied first, to
 * <site root>/.work/insert-product/<ISO timestamp, colons as dashes>/<its name>,
 * the site root being the nearest folder above --content that holds
 * site.manifest.json. The site repo autosyncs and git-ignores only .work/, so a
 * backup beside content.js would be committed. With no manifest above --content
 * (a scratch copy), each backup sits beside its file as <name>.bak. The run
 * prints where they went.
 *
 * After a --links run, run the site's paths.syncLinks from the site root: it
 * regenerates the two files that copy links.json, and the checker fails them stale.
 *
 * Exit 0 written (or dry-run clean) · 1 refused · 2 an input missing or not found.
 * Dependency-free: any Node ≥ 14.
 */

import { readFileSync, writeFileSync, existsSync, copyFileSync, mkdirSync } from "node:fs";
import { resolve, basename, dirname, join } from "node:path";
import vm from "node:vm";

const ARGV = process.argv.slice(2);
const opt = (n) => { const i = ARGV.indexOf("--" + n); return i !== -1 && i + 1 < ARGV.length ? ARGV[i + 1] : ""; };
const has = (n) => ARGV.indexOf("--" + n) !== -1;

if (has("help") || !ARGV.length) {
  /* The header comment is the help: every line from `/**` to its closing `*\/`. */
  const lines = readFileSync(new URL(import.meta.url)).toString().split("\n");
  const end = lines.findIndex((l, i) => i > 1 && /^\s*\*\/\s*$/.test(l));
  console.log(lines.slice(2, end === -1 ? lines.length : end).join("\n").replace(/^ ?\*\/?/gm, ""));
  process.exit(0);
}

const die = (code, msg) => { console.error("insert-product: " + msg); process.exit(code); };
const need = (p, what) => { if (!p) die(2, "missing --" + what); const a = resolve(p); if (!existsSync(a)) die(2, what + " not found: " + a); return a; };

const ENTRY = need(opt("entry"), "entry");
const CONTENT = need(opt("content"), "content");
const CONFIG = opt("config") ? need(opt("config"), "config") : "";
const CONFIG_ENTRY = opt("config-entry") ? need(opt("config-entry"), "config-entry") : "";
const LINKS = opt("links") ? need(opt("links"), "links") : "";
const DEMO_PATH = opt("demo-path");
const BEFORE = opt("before");
const DRY = has("dry-run");
const FIGURE_ALT = opt("figure-alt");
const CASE_CARD = opt("case-card") ? need(opt("case-card"), "case-card") : "";
if (has("figure-alt") && !FIGURE_ALT) die(2, "--figure-alt needs the figure's one-sentence description");
if (has("case-card") && !CASE_CARD) die(2, "--case-card needs a file: the home card's { line, metric: { label } }");
if (CONFIG && !CONFIG_ENTRY) die(2, "--config needs --config-entry");
if (CONFIG_ENTRY && !CONFIG) die(2, "--config-entry needs --config");
if (has("links") && !LINKS) die(2, "--links needs a file: the site's links.json");
if (has("demo-path") && !DEMO_PATH) die(2, "--demo-path needs a path, e.g. demo/<slug>/index.html");
if (DEMO_PATH && !LINKS) die(2, "--demo-path needs --links");

/* ---------------------------------------------------------------- scanning */
/* A source-aware bracket walk: it steps over strings, template literals and
   comments, so a `]` inside a sentence of body copy cannot end the array. */
function matchBracket(src, openIdx) {
  const open = src[openIdx];
  const close = open === "[" ? "]" : "}";
  let depth = 0;
  for (let i = openIdx; i < src.length; i++) {
    const c = src[i];
    if (c === '"' || c === "'" || c === "`") {
      const q = c;
      i++;
      while (i < src.length && src[i] !== q) { if (src[i] === "\\") i++; i++; }
      continue;
    }
    if (c === "/" && src[i + 1] === "/") { while (i < src.length && src[i] !== "\n") i++; continue; }
    if (c === "/" && src[i + 1] === "*") { i += 2; while (i < src.length && !(src[i] === "*" && src[i + 1] === "/")) i++; i++; continue; }
    if (c === open) depth++;
    else if (c === close) { depth--; if (depth === 0) return i; }
  }
  return -1;
}

/* The first balanced {...} that carries a `slug:` key — so the exemplar file,
   which also holds a config block and a diagram block, yields the right one.
   SLUG_KEY accepts the key bare (`slug:`) or JSON-quoted (`"slug":`): the site
   writes keys bare, tools/exemplar.mjs serializes the exemplar as JSON. */
const SLUG_KEY = "\\bslug[\"']?\\s*:\\s*";
function firstObjectWith(src, keyRe) {
  for (let i = 0; i < src.length; i++) {
    if (src[i] !== "{") continue;
    const end = matchBracket(src, i);
    if (end === -1) continue;
    const body = src.slice(i, end + 1);
    if (keyRe.test(body)) return { text: body, start: i, end };
    i = end;
  }
  return null;
}

function slugOf(text) {
  const m = text.match(new RegExp(SLUG_KEY + "[\"']([^\"']+)[\"']"));
  return m ? m[1] : "";
}

/* The site's content.js resolves logo paths through window.brandAsset(), which the
   site's assets/brand.js defines; the site's own tools (check-grammar.js, and
   sync-links.js loadSite()) run brand.js first, and so does this sandbox — without it
   the live content.js does not evaluate (2026-09-24). It is read where the site keeps
   it, assets/ beside data/, so a content.js copied out of its checkout has none. */
const BRAND_JS = join(dirname(CONTENT), "..", "assets", "brand.js");
const PRELUDE = existsSync(BRAND_JS) ? readFileSync(BRAND_JS, "utf8") : "";
function evalSite(src, filename) {
  const box = { window: {} };
  vm.createContext(box);
  if (PRELUDE) vm.runInContext(PRELUDE, box, { filename: "brand.js" });
  vm.runInContext(src, box, { filename });
  return box.window;
}
/* A site file that does not evaluate is a refusal that says why, never a stack trace;
   a missing brand.js is named, with where it was looked for (2026-09-29). */
function evalOrRefuse(src, filename) {
  try {
    return evalSite(src, filename);
  } catch (e) {
    const msg = e && e.message ? e.message : String(e);
    const noBrand = !existsSync(BRAND_JS) && /brandAsset/.test(msg);
    die(1, filename + " does not evaluate — nothing written: " + msg + (noBrand
      ? " (it needs the site's assets/brand.js, not found at " + BRAND_JS +
        ": pass the content.js inside a site checkout, or a full copy of one)"
      : ""));
  }
}

/* ------------------------------------------------------------------ entry */
const entrySrc = readFileSync(ENTRY, "utf8");
const found = firstObjectWith(entrySrc, new RegExp(SLUG_KEY + "[\"']"));
if (!found) die(1, "no product object literal (an object carrying a `slug:` key) found in " + basename(ENTRY));
const slug = slugOf(found.text);
if (!slug) die(1, "the entry has no readable slug");

/* ---------------------------------------------------------------- content */
const contentSrc = readFileSync(CONTENT, "utf8");
const before = evalOrRefuse(contentSrc, "content.js").SITE_CONTENT;
if (!before || !Array.isArray(before.products)) die(1, "content.js does not define window.SITE_CONTENT.products");
if (before.products.some((p) => p && p.slug === slug)) {
  die(1, 'slug "' + slug + '" is already in the catalog — edit that entry in the site repo instead; this tool never overwrites one');
}

const arrIdx = contentSrc.search(/\n\s*products\s*:\s*\[/);
if (arrIdx === -1) die(1, "no `products: [` array found in content.js");
const openIdx = contentSrc.indexOf("[", arrIdx);
const closeIdx = matchBracket(contentSrc, openIdx);
if (closeIdx === -1) die(1, "the `products: [` array is not balanced");

/* Keep the file's comma discipline: entries are separated by `,`, the last one
   carries none. The entry goes in verbatim — its own internal indentation is
   left alone, because reflowing someone's copy is how a diff stops being
   reviewable. Only the first line is re-indented to the array's depth. */
const indent = (contentSrc.slice(0, openIdx).match(/\n(\s*)products\s*:\s*\[?\s*$/) || ["", "    "])[1] + "  ";
const normalized = found.text.replace(/^\s+/, "");

let out;
let where;
if (BEFORE) {
  /* Walk the array's own items: a pattern over the whole file met the first `{` line of
     content.js, long before `products: [`, and refused every real --before (2026-09-29). */
  const keyRe = new RegExp(SLUG_KEY + "[\"']" + BEFORE.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "[\"']");
  let itemAt = -1;
  for (let i = openIdx + 1; i < closeIdx;) {
    const c = contentSrc[i];
    if (c === "/" && contentSrc[i + 1] === "/") { const nl = contentSrc.indexOf("\n", i); i = nl === -1 ? closeIdx : nl; continue; }
    if (c === "/" && contentSrc[i + 1] === "*") { const e = contentSrc.indexOf("*/", i + 2); i = e === -1 ? closeIdx : e + 2; continue; }
    if (c !== "{") { i++; continue; }
    const end = matchBracket(contentSrc, i);
    if (end === -1 || end > closeIdx) break;
    if (keyRe.test(contentSrc.slice(i, end + 1))) { itemAt = i; break; }
    i = end + 1;
  }
  if (itemAt === -1) die(1, '--before "' + BEFORE + '" names no entry inside the products array');
  const at = contentSrc.lastIndexOf("\n", itemAt) + 1;
  const lead = contentSrc.slice(at, itemAt);
  out = /^\s*$/.test(lead)
    ? contentSrc.slice(0, at) + lead + normalized + ",\n" + contentSrc.slice(at)   // its own line, its indentation
    : contentSrc.slice(0, itemAt) + normalized + ", " + contentSrc.slice(itemAt); // mid-line: just before it
  where = "before " + BEFORE;
} else {
  /* Append: the previous last entry needs the comma it does not have. */
  const head = contentSrc.slice(0, closeIdx).replace(/\s*$/, "");
  const tail = contentSrc.slice(closeIdx);
  const sep = head.endsWith(",") ? "" : ",";
  out = head + sep + "\n" + indent + normalized + "\n" + indent.slice(0, -2) + tail;
  where = "at the end of the array";
}

/* -------------------------------------------------------------- verify */
let after;
try {
  after = evalSite(out, "content.js (spliced)").SITE_CONTENT;
} catch (e) {
  die(1, "the spliced content.js does not evaluate — nothing written: " + e.message);
}
if (!after || !Array.isArray(after.products)) die(1, "the spliced file lost window.SITE_CONTENT.products — nothing written");
if (after.products.length !== before.products.length + 1) {
  die(1, "the spliced file holds " + after.products.length + " products, expected " + (before.products.length + 1) + " — nothing written");
}
if (!after.products.some((p) => p && p.slug === slug)) die(1, 'slug "' + slug + '" is not in the spliced catalog — nothing written');

/* Site round 13: every product names its lead, an id in shared.people, and the site's
   checker fails a missing or unknown one — so refuse here, before anything is written.
   A site (or a fixture) that defines no shared.people is left alone. */
const people = after.shared && after.shared.people;
if (people && typeof people === "object" && !Array.isArray(people)) {
  const inserted = after.products.find((p) => p && p.slug === slug) || {};
  const ids = Object.keys(people).join(", ");
  if (typeof inserted.contactPerson !== "string" || !inserted.contactPerson) {
    die(1, "the entry has no contactPerson — the site names each product's lead, an id in shared.people (" + ids + ") — nothing written");
  }
  if (!Object.prototype.hasOwnProperty.call(people, inserted.contactPerson)) {
    die(1, 'contactPerson "' + inserted.contactPerson + '" is not an id in shared.people (' + ids + ") — nothing written");
  }
}

/* ---------------------------------------------------------------- media */
/* The product page draws its figure only through content.js media["<slug>"] (the
   site's UI.figure), so the entry is written here, in the same run as the product,
   or the new product shows no architecture figure and nothing says so (2026-09-24).
   A content.js (or a fixture) with no media map is left alone. */
let mediaNote = "";
if (after.media && typeof after.media === "object" && !Array.isArray(after.media)) {
  if (!FIGURE_ALT) {
    die(1, 'the site draws a product\'s figure only through content.js media["' + slug +
      '"] — pass --figure-alt "<one sentence describing the figure>" — nothing written');
  }
  if (Object.prototype.hasOwnProperty.call(after.media, slug)) {
    die(1, 'content.js media already carries "' + slug + '" — nothing written');
  }
  const mIdx = out.search(/\n\s*media\s*:\s*\{/);
  if (mIdx === -1) die(1, "no `media: {` map found in content.js");
  const mOpen = out.indexOf("{", mIdx);
  const mClose = matchBracket(out, mOpen);
  if (mClose === -1) die(1, "the `media: {` map is not balanced");
  const mIndent = (out.slice(0, mOpen).match(/\n(\s*)media\s*:\s*\{?\s*$/) || ["", "  "])[1];
  const mHead = out.slice(0, mClose).replace(/\s*$/, "");
  const mSep = mHead.endsWith(",") || mHead.endsWith("{") ? "" : ",";
  const mEntry = JSON.stringify(slug) + ": {\n" + mIndent + "    diagram: " + JSON.stringify(slug) +
    ",\n" + mIndent + "    alt: " + JSON.stringify(FIGURE_ALT) + "\n" + mIndent + "  }";
  out = mHead + mSep + "\n" + mIndent + "  " + mEntry + "\n" + mIndent + out.slice(mClose);
  let withMedia;
  try {
    withMedia = evalSite(out, "content.js (media spliced)").SITE_CONTENT;
  } catch (e) {
    die(1, "content.js does not evaluate after the media entry — nothing written: " + e.message);
  }
  if (!withMedia || !withMedia.media || !withMedia.media[slug] || withMedia.media[slug].diagram !== slug ||
      withMedia.products.length !== after.products.length) {
    die(1, 'the media entry for "' + slug + '" did not land as expected — nothing written');
  }
  mediaNote = " · media entry added (the product page's figure)";
}

/* ------------------------------------------------------------ case card */
/* The home page shows one card per product that carries a case study, and the site's
   checker fails a product whose case study has no card, and a card whose descriptor,
   area, industry, status or figure disagrees with its product (site round 11). Only the
   card's two lines are copy; everything else is read from the entry, so the two surfaces
   cannot drift. A content.js (or a fixture) with no overview.caseStudies is left alone. */
let cardNote = "";
{
  const site = evalSite(out, "content.js (before the case card)").SITE_CONTENT;
  const product = site.products.find((p) => p && p.slug === slug) || {};
  const cs = product.overview && product.overview.caseStudy;
  const cards = site.overview && site.overview.caseStudies;
  if (!Array.isArray(cards)) {
    if (CASE_CARD) die(1, "content.js has no overview.caseStudies — there is no home card grid for --case-card — nothing written");
  } else if (!cs) {
    if (CASE_CARD) {
      die(1, 'the entry\'s overview.caseStudy is null — a home card would link to a page with no case study; drop --case-card — nothing written');
    }
  } else {
    if (!CASE_CARD) {
      die(1, 'the entry carries overview.caseStudy, and the home page shows one card per case study (overview.caseStudies) — pass --case-card <file> with its { line, metric: { label } } — nothing written');
    }
    const cardSrc = readFileSync(CASE_CARD, "utf8");
    const open = cardSrc.indexOf("{");
    const close = open === -1 ? -1 : matchBracket(cardSrc, open);
    if (close === -1) die(1, "no object literal found in " + basename(CASE_CARD));
    let given;
    try {
      given = vm.runInNewContext("(" + cardSrc.slice(open, close + 1) + ")", {});
    } catch (e) {
      die(1, basename(CASE_CARD) + " does not evaluate — nothing written: " + e.message);
    }
    const text = (v) => typeof v === "string" && v.trim() !== "";
    if (!text(given.line)) die(1, basename(CASE_CARD) + " has no line — the card's one sentence: the customer's old way and what changes — nothing written");
    if (!given.metric || !text(given.metric.label)) {
      die(1, basename(CASE_CARD) + " has no metric.label — the small line under the figure: what it measures, against what — nothing written");
    }
    const lead = (Array.isArray(cs.metrics) && cs.metrics[0]) || {};
    if (!text(lead.value)) die(1, "the entry's overview.caseStudy.metrics[0].value is empty — the card states that figure — nothing written");
    const id = text(given.id) ? given.id : slug + "-case";
    if (cards.some((c) => c && (c.id === id || (c.product && c.product.slug === slug)))) {
      die(1, 'overview.caseStudies already carries "' + id + '" or a card for "' + slug + '" — nothing written');
    }
    const card = {
      id, descriptor: cs.descriptor, area: cs.area, industry: cs.industry, status: cs.status,
      metric: { value: lead.value, label: given.metric.label }, line: given.line,
      product: { slug, name: product.name }
    };
    const cIdx = out.search(/\n\s*caseStudies\s*:\s*\[/);
    if (cIdx === -1) die(1, "no `caseStudies: [` array found in content.js");
    const cOpen = out.indexOf("[", cIdx);
    const cClose = matchBracket(out, cOpen);
    if (cClose === -1) die(1, "the `caseStudies: [` array is not balanced");
    const cIndent = (out.slice(0, cOpen).match(/\n(\s*)caseStudies\s*:\s*\[?\s*$/) || ["", "    "])[1] + "  ";
    const cHead = out.slice(0, cClose).replace(/\s*$/, "");
    const cSep = cHead.endsWith(",") || cHead.endsWith("[") ? "" : ",";
    const body = JSON.stringify(card, null, 2).split("\n").join("\n" + cIndent);
    out = cHead + cSep + "\n" + cIndent + body + "\n" + cIndent.slice(0, -2) + out.slice(cClose);
    let withCard;
    try {
      withCard = evalSite(out, "content.js (case card spliced)").SITE_CONTENT;
    } catch (e) {
      die(1, "content.js does not evaluate after the case card — nothing written: " + e.message);
    }
    const now = withCard.overview && withCard.overview.caseStudies;
    if (!Array.isArray(now) || now.length !== cards.length + 1 || !now.some((c) => c && c.id === id) ||
        withCard.products.length !== after.products.length) {
      die(1, 'the home case card for "' + slug + '" did not land as expected — nothing written');
    }
    cardNote = ' · home case card "' + id + '" added (overview.caseStudies)';
  }
}

/* --------------------------------------------------------------- config */
let cfgOut = "", cfgNote = "";
if (CONFIG) {
  const cfgEntrySrc = readFileSync(CONFIG_ENTRY, "utf8");
  const keyRe = new RegExp('["\']' + slug.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + '["\']\\s*:\\s*\\{');
  const km = cfgEntrySrc.match(keyRe);
  if (!km) die(1, 'no `"' + slug + '": { … }` switch block found in ' + basename(CONFIG_ENTRY));
  const blockOpen = cfgEntrySrc.indexOf("{", km.index + km[0].length - 1);
  const blockEnd = matchBracket(cfgEntrySrc, blockOpen);
  if (blockEnd === -1) die(1, "the config switch block is not balanced");
  const block = '"' + slug + '": ' + cfgEntrySrc.slice(blockOpen, blockEnd + 1);

  const cfgSrc = readFileSync(CONFIG, "utf8");
  const cfgBefore = evalOrRefuse(cfgSrc, "config.js").SITE_CONFIG;
  if (cfgBefore && cfgBefore.products && cfgBefore.products[slug]) {
    die(1, 'config.js already carries "' + slug + '" — nothing written');
  }
  const pIdx = cfgSrc.search(/\n\s*products\s*:\s*\{/);
  if (pIdx === -1) die(1, "no `products: {` map found in config.js");
  const pOpen = cfgSrc.indexOf("{", pIdx);
  const pClose = matchBracket(cfgSrc, pOpen);
  if (pClose === -1) die(1, "the `products: {` map is not balanced");
  const cHead = cfgSrc.slice(0, pClose).replace(/\s*$/, "");
  const cTail = cfgSrc.slice(pClose);
  const cSep = cHead.endsWith(",") ? "" : ",";
  cfgOut = cHead + cSep + "\n    " + block + "\n  " + cTail;

  /* productOrder is owner-controlled: a new slug joins the end, and the owner
     moves it. An absent productOrder is left absent. */
  const orderRe = /(productOrder\s*:\s*\[)([^\]]*)(\])/;
  if (orderRe.test(cfgOut)) {
    cfgOut = cfgOut.replace(orderRe, (all, a, body, z) => {
      if (new RegExp('["\']' + slug + '["\']').test(body)) return all;
      const trimmed = body.replace(/\s*$/, "");
      const sep2 = trimmed.replace(/\s*$/, "").endsWith(",") ? "" : ",";
      return a + trimmed + sep2 + '\n    "' + slug + '"\n  ' + z;
    });
    cfgNote = " · appended to productOrder";
  }
  try {
    const cfgAfter = evalSite(cfgOut, "config.js (spliced)").SITE_CONFIG;
    if (!cfgAfter || !cfgAfter.products || !cfgAfter.products[slug]) throw new Error("slug not present after splice");
  } catch (e) {
    die(1, "the spliced config.js does not evaluate — nothing written: " + e.message);
  }
}

/* ---------------------------------------------------------------- links */
/* The kit-links entry (site round 12): the six keys in the site's own order,
   each "" until its artifact exists. links.json is JSON, so it is parsed and
   re-serialized rather than spliced; a round trip keeps its key order. */
const LINK_KEYS = ["onePager", "salesDeck", "featureList", "interactiveDemo", "interactiveDemoArtifact", "video"];
let linksOut = "", linksNote = "";
if (LINKS) {
  let links;
  try {
    links = JSON.parse(readFileSync(LINKS, "utf8"));
  } catch (e) {
    die(1, basename(LINKS) + " is not valid JSON — nothing written: " + e.message);
  }
  const isMap = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
  if (!isMap(links) || !isMap(links.products)) die(1, basename(LINKS) + " has no `products` object — nothing written");
  if (Object.prototype.hasOwnProperty.call(links.products, slug)) {
    die(1, basename(LINKS) + ' already carries "' + slug + '" — nothing written');
  }
  const linkEntry = {};
  for (const key of LINK_KEYS) linkEntry[key] = key === "interactiveDemo" ? DEMO_PATH : "";
  links.products[slug] = linkEntry;
  linksOut = JSON.stringify(links, null, 2) + "\n";
  linksNote = " · links.json kit-links entry added (" +
    (DEMO_PATH ? "interactiveDemo " + DEMO_PATH + ", the other five empty" : "all six keys empty") + ")";
}

/* ---------------------------------------------------------------- write */
const summary =
  'insert-product: "' + slug + '" ' + where + " — content.js " +
  before.products.length + " → " + after.products.length + " products" + mediaNote + cardNote +
  (CONFIG ? " · config.js switch block added" + cfgNote : "") + linksNote;

if (DRY) { console.log("[dry-run] " + summary); console.log("[dry-run] nothing written"); process.exit(0); }

/* Backups leave the site's tree (header, BACKUPS): into the git-ignored
   .work/ of the nearest folder above --content that holds site.manifest.json,
   else beside each file as <name>.bak. */
function siteRootOf(file) {
  for (let dir = dirname(file); ; dir = dirname(dir)) {
    if (existsSync(join(dir, "site.manifest.json"))) return dir;
    if (dirname(dir) === dir) return "";
  }
}
const SITE_ROOT = siteRootOf(CONTENT);
const BACKUP_DIR = SITE_ROOT
  ? join(SITE_ROOT, ".work", "insert-product", new Date().toISOString().replace(/:/g, "-"))
  : "";
function backup(file) {
  const to = BACKUP_DIR ? join(BACKUP_DIR, basename(file)) : file + ".bak";
  if (BACKUP_DIR) mkdirSync(BACKUP_DIR, { recursive: true });
  copyFileSync(file, to);
  return to;
}

const backups = [backup(CONTENT)];
writeFileSync(CONTENT, out, "utf8");
if (CONFIG) {
  backups.push(backup(CONFIG));
  writeFileSync(CONFIG, cfgOut, "utf8");
}
if (LINKS) {
  backups.push(backup(LINKS));
  writeFileSync(LINKS, linksOut, "utf8");
}
console.log(summary);
console.log(BACKUP_DIR
  ? "insert-product: backups in " + BACKUP_DIR + "/ (" + backups.map((b) => basename(b)).join(", ") + "), inside the site's git-ignored .work/"
  : "insert-product: no site.manifest.json above " + basename(CONTENT) + ", so the backups sit beside the files: " + backups.join(", "));
if (LINKS) {
  console.log("insert-product: now run, from the site root, the manifest's paths.syncLinks (it regenerates the files copied from links.json), then its checker.run.");
} else {
  console.log("insert-product: now run the site's own checker (site.manifest.json, checker.run) before anything else.");
}
