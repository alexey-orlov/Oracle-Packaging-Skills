// capture-demo-frames.mjs — drive an interactive walkthrough in headless Chrome
// over the DevTools protocol and capture PNGs. No dependencies: Node ≥ 22
// (built-in fetch + WebSocket) and a Chrome/Chromium binary.
//
//   node capture-demo-frames.mjs --demo <url-or-path> --out <dir> --scenario <json>
//   node capture-demo-frames.mjs --demo ./index.html --out ./shots --scenario tour.json
//
// PORTED from the practice site's tools/capture-demo-frames.mjs. Changes:
//   1. The Chrome path was hard-coded to one macOS install. It is now
//      $CHROME_BIN, defaulting to the standard macOS path, and the script says
//      what to set when the binary is not there.
//   2. Positional args became --demo / --out / --scenario, and a bare
//      filesystem path is turned into a file:// URL, so a demo can be captured
//      without a web server.
//   3. The per-demo scene lists (which knew one product's selectors) are gone.
//      Scenarios are data; this file is the driver.
//
// OPTIONS
//   --demo <url|path>   the walkthrough to open. A path is resolved to file://.
//   --out <dir>         where the PNGs go (created).
//   --scenario <json>   an array of steps (see below). Without one, the script
//                       opens the page, waits, shoots `00-open` and reports.
//   --width / --height  viewport in CSS px (default 1600 × 1000).
//   --dpr <n>           device scale factor (default 1; use 2 for shipped stills).
//   --port <n>          DevTools port (default 9333).
//   --allow-net         do NOT block webfont hosts (they are blocked by default
//                       so a slow network cannot stall a capture; system
//                       fallbacks render instead — expect different metrics).
//   --keep-open         leave Chrome running after the run (debugging).
//
// SCENARIO STEPS — a JSON array, executed in order:
//   { "click":  "<css selector>" }   SVG elements have no .click(); a bubbling
//                                    MouseEvent is dispatched for them.
//   { "sleep":  1200 }               milliseconds
//   { "shot":   "04-processing" }    writes <out>/04-processing.png
//   { "eval":   "<expression>" }     runs in the page; top-level await allowed
//   { "type":   { "sel": "#q", "text": "…" } }
//   { "assert": { "expr": "…", "name": "no overlap" } }  fails the run if falsy
//
// THE GATE: the run prints `LOGS: none`. Any console message or page exception
// is printed instead, and the process exits 1. A capture with console noise is
// not a passing capture — look at the shots only after the gate is green.
//
// TWO STANDARD RUNS
//   tour regression — the whole guided flow, guide visible, DPR 1:
//     node capture-demo-frames.mjs --demo ./index.html --out ./qa --scenario tour.json
//   step frames + poster — tour off, chrome hidden, DPR 2:
//     node capture-demo-frames.mjs --demo './index.html?tour=off&ui=clean&state=final' \
//       --out ./frames --dpr 2 --scenario frames.json
//   Then crop the frames to the listing's step-image spec before shipping them.

import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync, readFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const ARGV = process.argv.slice(2);
const opt = (n, d = "") => { const i = ARGV.indexOf("--" + n); return i !== -1 && i + 1 < ARGV.length ? ARGV[i + 1] : d; };
const has = (n) => ARGV.includes("--" + n);

if (has("help") || !ARGV.length) {
  console.log(readFileSync(new URL(import.meta.url), "utf8").split("\n").filter((l) => l.startsWith("//")).map((l) => l.slice(3)).join("\n"));
  process.exit(0);
}

const CH = process.env.CHROME_BIN || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
if (!existsSync(CH)) {
  console.error(
    `capture-demo-frames: no Chrome at ${CH}\n` +
    "  Set CHROME_BIN to a Chrome or Chromium binary. Common locations:\n" +
    "    macOS   /Applications/Google Chrome.app/Contents/MacOS/Google Chrome\n" +
    "    Linux   /usr/bin/google-chrome  ·  /usr/bin/chromium\n" +
    "  This is an environment condition, not a result: nothing was captured."
  );
  process.exit(3);
}
const [maj] = process.versions.node.split(".").map(Number);
if (maj < 22) {
  console.error(`capture-demo-frames: Node ${process.versions.node} — this script needs Node >= 22 (built-in fetch and WebSocket). Nothing was captured.`);
  process.exit(3);
}

const demoArg = opt("demo");
if (!demoArg) { console.error("capture-demo-frames: --demo <url-or-path> is required"); process.exit(2); }
// A filesystem path becomes file://…; a query string survives the conversion.
let URL_ = demoArg;
if (!/^[a-z]+:\/\//i.test(demoArg)) {
  const [p, q] = demoArg.split("?");
  if (!existsSync(resolve(p))) { console.error("capture-demo-frames: no such file: " + resolve(p)); process.exit(2); }
  URL_ = pathToFileURL(resolve(p)).href + (q ? "?" + q : "");
}

const OUT = resolve(opt("out", "./capture-out"));
mkdirSync(OUT, { recursive: true });
const SCENARIO = opt("scenario");
if (SCENARIO && !existsSync(resolve(SCENARIO))) { console.error("capture-demo-frames: no such scenario: " + resolve(SCENARIO)); process.exit(2); }

const W = +(opt("width") || process.env.W || 1600);
const H = +(opt("height") || process.env.H || 1000);
const DPR = +(opt("dpr") || process.env.DPR || 1);
const PORT = +(opt("port") || 9333);

const chrome = spawn(CH, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--disable-extensions", "--disable-sync", "--allow-file-access-from-files",
  `--remote-debugging-port=${PORT}`, `--user-data-dir=${OUT}/.chrome-profile`,
  `--window-size=${W},${H}`, "--hide-scrollbars", "about:blank"
], { stdio: "ignore" });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function targets() {
  for (let i = 0; i < 40; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json`); return await r.json(); }
    catch { await sleep(250); }
  }
  throw new Error("chrome did not start on port " + PORT);
}

const list = await targets();
const page = list.find((t) => t.type === "page");
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((r) => (ws.onopen = r));

let id = 0;
const pending = new Map();
const logs = [];
ws.onmessage = (m) => {
  const msg = JSON.parse(m.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  if (msg.method === "Runtime.consoleAPICalled") {
    logs.push(`[console.${msg.params.type}] ` + msg.params.args.map((a) => a.value ?? a.description).join(" "));
  }
  if (msg.method === "Runtime.exceptionThrown") {
    logs.push("[exception] " + (msg.params.exceptionDetails.exception?.description || msg.params.exceptionDetails.text));
  }
};

const send = (method, params = {}) => new Promise((res, rej) => {
  const i = ++id;
  pending.set(i, (m) => (m.error ? rej(new Error(method + ": " + JSON.stringify(m.error))) : res(m.result)));
  ws.send(JSON.stringify({ id: i, method, params }));
});

const ev = async (expr) => {
  const r = await send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) {
    throw new Error("eval: " + (r.exceptionDetails.exception?.description || r.exceptionDetails.text) + " in " + expr);
  }
  return r.result.value;
};

// SVG elements (map zones, markers) have no .click(); dispatch a bubbling MouseEvent.
const click = (sel) => ev(
  `(()=>{const el=document.querySelector(${JSON.stringify(sel)});` +
  `if(!el) throw new Error("no element "+${JSON.stringify(sel)});` +
  `if (typeof el.click === "function") el.click();` +
  `else el.dispatchEvent(new MouseEvent("click", {bubbles:true, cancelable:true}));return true;})()`
);

const type = (sel, text) => ev(
  `(()=>{const el=document.querySelector(${JSON.stringify(sel)});` +
  `if(!el) throw new Error("no element "+${JSON.stringify(sel)});` +
  `el.value=${JSON.stringify(text)};el.dispatchEvent(new Event('input',{bubbles:true}));return true;})()`
);

const shot = async (name) => {
  const r = await send("Page.captureScreenshot", { format: "png" });
  writeFileSync(`${OUT}/${name}.png`, Buffer.from(r.data, "base64"));
  console.log("shot", name);
};

await send("Page.enable");
await send("Runtime.enable");
await send("Network.enable");
if (!has("allow-net") && !process.env.ALLOW_NET) {
  await send("Network.setBlockedURLs", { urls: ["*://fonts.googleapis.com/*", "*://fonts.gstatic.com/*"] });
}
await send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: DPR, mobile: false });
await send("Page.navigate", { url: URL_ });
await sleep(1800);

const failures = [];
try {
  if (SCENARIO) {
    const steps = JSON.parse(readFileSync(resolve(SCENARIO), "utf8"));
    for (const s of steps) {
      if (s.click) await click(s.click);
      else if (s.sleep) await sleep(s.sleep);
      else if (s.shot) await shot(s.shot);
      else if (s.eval) await ev(s.eval);
      else if (s.type) await type(s.type.sel, s.type.text);
      else if (s.assert) {
        const ok = await ev("(()=>{ return !!(" + s.assert.expr + "); })()");
        if (!ok) failures.push("assert failed: " + (s.assert.name || s.assert.expr));
      }
    }
  } else {
    await shot("00-open");
  }
} catch (e) {
  failures.push("FAILED: " + e.message);
}

console.log(logs.length ? "LOGS:\n" + logs.join("\n") : "LOGS: none");
for (const f of failures) console.error(f);
ws.close();
if (!has("keep-open")) chrome.kill();
process.exit(logs.length || failures.length ? 1 : 0);
