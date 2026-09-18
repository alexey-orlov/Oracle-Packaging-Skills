#!/usr/bin/env node
/**
 * insert-product.mjs — splice one product entry into a practice site's data files.
 *
 *   node insert-product.mjs --entry entry.js --content <site>/site/data/content.js \
 *        [--config <site>/site/data/config.js --config-entry entry.js] \
 *        [--before <slug>] [--dry-run]
 *
 * WHY A TOOL. The entry goes inside `products: [ … ]`, which is 2,000 lines into
 * a 190 KB file whose last element has no trailing comma. Hand-editing it is how
 * a build breaks silently: an entry pasted after the closing bracket parses fine
 * and renders nothing. This does the splice, then re-runs the file through a
 * sandbox and refuses to write unless the catalog actually grew by one.
 *
 * WHAT IT REFUSES TO DO
 *   - overwrite a slug that already exists (there is no --force: replacing an
 *     entry is an edit of the site's own copy, made in the site's own repo);
 *   - write anything when the spliced file does not evaluate, or when the
 *     product count did not go up by exactly one;
 *   - touch config.js unless both --config and --config-entry are given.
 *
 * INPUTS
 *   --entry <file>         a file holding ONE product object literal. Leading and
 *                          trailing comments are fine, and so are the extra blocks
 *                          of assets/exemplar-product-entry.js: the first balanced
 *                          {...} carrying a `slug:` key is taken and the rest ignored.
 *   --content <file>       the target site/data/content.js.
 *   --config <file>        the target site/data/config.js (optional).
 *   --config-entry <file>  a file holding ONE `"<slug>": { … }` switch block, or
 *                          the exemplar file, from which the block whose key is
 *                          this slug is taken (optional; requires --config).
 *                          The slug is also appended to `productOrder`.
 *   --before <slug>        insert before that entry instead of at the end of the array.
 *   --dry-run              report what would change; write nothing.
 *
 * Exit 0 written (or dry-run clean) · 1 refused · 2 inputs not found.
 * Dependency-free: any Node ≥ 14.
 */

import { readFileSync, writeFileSync, existsSync, copyFileSync } from "node:fs";
import { resolve, basename } from "node:path";
import vm from "node:vm";

const ARGV = process.argv.slice(2);
const opt = (n) => { const i = ARGV.indexOf("--" + n); return i !== -1 && i + 1 < ARGV.length ? ARGV[i + 1] : ""; };
const has = (n) => ARGV.indexOf("--" + n) !== -1;

if (has("help") || !ARGV.length) {
  console.log(readFileSync(new URL(import.meta.url)).toString().split("\n").slice(1, 40).join("\n").replace(/^ ?\*\/?/gm, ""));
  process.exit(0);
}

const die = (code, msg) => { console.error("insert-product: " + msg); process.exit(code); };
const need = (p, what) => { if (!p) die(2, "missing --" + what); const a = resolve(p); if (!existsSync(a)) die(2, what + " not found: " + a); return a; };

const ENTRY = need(opt("entry"), "entry");
const CONTENT = need(opt("content"), "content");
const CONFIG = opt("config") ? need(opt("config"), "config") : "";
const CONFIG_ENTRY = opt("config-entry") ? need(opt("config-entry"), "config-entry") : "";
const BEFORE = opt("before");
const DRY = has("dry-run");
if (CONFIG && !CONFIG_ENTRY) die(2, "--config needs --config-entry");
if (CONFIG_ENTRY && !CONFIG) die(2, "--config-entry needs --config");

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
   which also holds a config block and a diagram block, yields the right one. */
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
  const m = text.match(/\bslug\s*:\s*["']([^"']+)["']/);
  return m ? m[1] : "";
}

function evalSite(src, filename) {
  const box = { window: {} };
  vm.createContext(box);
  vm.runInContext(src, box, { filename });
  return box.window;
}

/* ------------------------------------------------------------------ entry */
const entrySrc = readFileSync(ENTRY, "utf8");
const found = firstObjectWith(entrySrc, /\bslug\s*:\s*["']/);
if (!found) die(1, "no product object literal (an object carrying a `slug:` key) found in " + basename(ENTRY));
const slug = slugOf(found.text);
if (!slug) die(1, "the entry has no readable slug");

/* ---------------------------------------------------------------- content */
const contentSrc = readFileSync(CONTENT, "utf8");
const before = evalSite(contentSrc, "content.js").SITE_CONTENT;
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
  const target = new RegExp("\\n(\\s*)\\{[^]*?slug\\s*:\\s*[\"']" + BEFORE.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "[\"']");
  const m = contentSrc.match(target);
  if (!m || m.index === undefined || m.index > closeIdx || m.index < openIdx) {
    die(1, '--before "' + BEFORE + '" names no entry inside the products array');
  }
  const at = m.index + 1;
  out = contentSrc.slice(0, at) + m[1] + normalized + ",\n" + contentSrc.slice(at);
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
  const cfgBefore = evalSite(cfgSrc, "config.js").SITE_CONFIG;
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

/* ---------------------------------------------------------------- write */
const summary =
  'insert-product: "' + slug + '" ' + where + " — content.js " +
  before.products.length + " → " + after.products.length + " products" +
  (CONFIG ? " · config.js switch block added" + cfgNote : "");

if (DRY) { console.log("[dry-run] " + summary); console.log("[dry-run] nothing written"); process.exit(0); }

copyFileSync(CONTENT, CONTENT + ".bak");
writeFileSync(CONTENT, out, "utf8");
if (CONFIG) { copyFileSync(CONFIG, CONFIG + ".bak"); writeFileSync(CONFIG, cfgOut, "utf8"); }
console.log(summary);
console.log("insert-product: backups at " + basename(CONTENT) + ".bak" + (CONFIG ? " and " + basename(CONFIG) + ".bak" : ""));
console.log("insert-product: now run check-grammar.js --site-root <site-repo> before anything else.");
