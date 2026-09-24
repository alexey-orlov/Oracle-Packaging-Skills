/* Workforce optimization — interactive walkthrough.
   Plain JS, no dependencies. State → render; the tour engine sits on top and
   only ever lets the designated control through while it is active. A plan is
   the uploaded current allocation plus a set of named changes, each carrying
   its assignments and its KPI effect — so the value of the optimization is
   always visible as before → after, every change can be drilled into, and a
   change the dispatcher undoes takes its numbers with it. */
(function () {
  "use strict";
  var D = window.WFO_DATA;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  var params = new URLSearchParams(location.search);
  var USER = D.user.name;
  var ICON = {
    clock: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.5 2"/></svg>',
    pin: '<svg viewBox="0 0 24 24"><path d="M12 21s6-5.4 6-10a6 6 0 0 0-12 0c0 4.6 6 10 6 10Z"/><circle cx="12" cy="11" r="2.2"/></svg>',
    gauge: '<svg viewBox="0 0 24 24"><path d="M4 16a8 8 0 1 1 16 0"/><path d="M12 16l3.5-4.5"/></svg>',
    bolt: '<svg viewBox="0 0 24 24"><path d="M13 3 5 14h6l-1 7 8-11h-6z"/></svg>',
    warn: '<svg viewBox="0 0 24 24"><path d="M10.3 3.9 2.7 17a2 2 0 0 0 1.7 3h15.2a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 8.5v5M12 16.6v.4"/></svg>',
    check: '<svg viewBox="0 0 24 24"><path d="m5 12 4.5 4.5L19 7"/></svg>',
    x: '<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18"/></svg>',
    chat: '<svg viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4z"/></svg>',
    chev: '<svg class="chev" viewBox="0 0 24 24"><path d="m9 6 6 6-6 6"/></svg>',
    user: '<svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/></svg>',
    users: '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3.5"/><path d="M3 20a6 6 0 0 1 12 0"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 20a4.5 4.5 0 0 1 5.5-4.3"/></svg>',
    cal: '<svg viewBox="0 0 24 24"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>',
    undo: '<svg viewBox="0 0 24 24"><path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-3"/></svg>',
    eye: '<svg viewBox="0 0 24 24"><path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6Z"/><circle cx="12" cy="12" r="2.5"/></svg>',
    up: '<svg viewBox="0 0 24 24"><path d="M12 19V5M6 11l6-6 6 6"/></svg>',
    down: '<svg viewBox="0 0 24 24"><path d="M12 5v14M6 13l6 6 6-6"/></svg>',
    flag: '<svg viewBox="0 0 24 24"><path d="M5 21V4h11l-1.5 3.5L16 11H5"/></svg>'
  };
  var WD = D.days.filter(function (d) { return d.working; });
  var ZI = {}; D.zones.forEach(function (z) { ZI[z.id] = z; });
  var TI = {}; D.techs.forEach(function (t) { TI[t.id] = t; });
  var CI = {}; D.changes.forEach(function (c) { CI[c.id] = c; });
  function dayOf(k) { return D.days.filter(function (d) { return d.d === k; })[0]; }
  function fmtShort(k) { var d = dayOf(k); return d ? d.n + " " + d.mon : k; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function r2(x) { return Math.round(x * 100) / 100; }

  /* ---------------- state ---------------- */
  var S = { ran: false, version: "", applied: [], undone: [], notes: {}, view: "opt", sched: "zone", week: 1, filters: { zones: [], techs: [] }, sel: { cur: null, opt: null }, decisions: {}, history: [], exported: false, sent: false, pickedFile: null, runFile: null, busy: false, changesOnly: false, focus: null };
  function applied() { return S.ran ? S.applied : []; }
  function on(id) { return S.applied.indexOf(id) >= 0; }
  function resetDecisions() { S.decisions = {}; D.zones.forEach(function (z) { S.decisions[z.id] = { status: "pending", comment: "" }; }); }
  resetDecisions();
  function now() { var d = new Date(); return ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2); }
  function log(text, sub, kind) { S.history.unshift({ time: now(), text: text, sub: sub || "", kind: kind || "" }); }
  function planLabel() { if (!S.ran) return "current"; if (S.version === "v2") return "v2"; return S.undone.length ? "v1 + " + S.undone.length + (S.undone.length === 1 ? " fix" : " fixes") : "v1"; }

  /* ---------------- allocation ---------------- */
  var memo = {};
  function keyOf(list) { return list.slice().sort().join("|"); }
  function absentOn(t, k) { for (var i = 0; i < t.absent.length; i++) { var a = t.absent[i]; if (k >= a.from && k <= a.to) return a.kind; } return ""; }
  function alloc(list) {
    var key = keyOf(list); if (memo[key]) return memo[key];
    var A = { byTech: {}, byZone: {}, absent: {} };
    D.techs.forEach(function (t) { A.byTech[t.id] = {}; A.absent[t.id] = {}; });
    D.zones.forEach(function (z) { A.byZone[z.id] = {}; });
    var ov = {};
    D.changes.forEach(function (c) { if (list.indexOf(c.id) < 0) return; c.overrides.forEach(function (o) { o.dates.forEach(function (k) { (ov[o.tech + "|" + k] = ov[o.tech + "|" + k] || []).push(o); }); }); });
    D.techs.forEach(function (t) {
      WD.forEach(function (d) {
        var k = d.d, ab = absentOn(t, k);
        if (ab) { A.absent[t.id][k] = ab; return; }
        var rows = t.zones.map(function (z) { return { zone: z, kind: "default" }; });
        (ov[t.id + "|" + k] || []).forEach(function (o) {
          if (o.kind === "moved") rows = [{ zone: o.zone, kind: "moved", ov: o }];
          else if (o.kind === "temp") rows.push({ zone: o.zone, kind: "temp", partial: !!o.partial, ov: o });
          else if (o.kind === "off") rows = [{ zone: o.zone, kind: "off", ov: o }];
          else rows.forEach(function (e) { if (e.zone === o.zone) { e.kind = o.kind; e.ov = o; } });
        });
        A.byTech[t.id][k] = rows;
        rows.forEach(function (e) { (A.byZone[e.zone][k] = A.byZone[e.zone][k] || []).push({ tech: t.id, kind: e.kind, partial: e.partial, ov: e.ov }); });
      });
    });
    memo[key] = A; return A;
  }
  function cellSig(list) { return list.map(function (e) { return (e.tech || e.zone) + ":" + e.kind + (e.partial ? "p" : ""); }).sort().join(","); }
  function zoneCellChanged(list, zid, k) { return cellSig(alloc(list).byZone[zid][k] || []) !== cellSig(alloc([]).byZone[zid][k] || []); }
  function techCellChanged(list, tid, k) { return cellSig(alloc(list).byTech[tid][k] || []) !== cellSig(alloc([]).byTech[tid][k] || []); }
  function zoneChanged(list, zid) { return WD.some(function (d) { return zoneCellChanged(list, zid, d.d); }); }
  function techChanged(list, tid) { return WD.some(function (d) { return techCellChanged(list, tid, d.d); }); }
  function changedZones(list) { return D.zones.filter(function (z) { return zoneChanged(list, z.id); }).map(function (z) { return z.id; }); }
  function techZones(list, tid) {
    var A = alloc(list), out = {}, order = [];
    Object.keys(A.byTech[tid]).forEach(function (k) { A.byTech[tid][k].forEach(function (e) { if (!out[e.zone]) { out[e.zone] = { zone: e.zone, days: 0, kind: e.kind, dates: [], ov: e.ov }; order.push(e.zone); } out[e.zone].days++; out[e.zone].dates.push(k); if (e.kind !== "default" && e.kind !== "off") { out[e.zone].kind = e.kind; out[e.zone].ov = e.ov; } }); });
    return order.map(function (z) { return out[z]; });
  }
  function zoneTechs(list, zid) {
    var A = alloc(list), out = {}, order = [];
    Object.keys(A.byZone[zid]).sort().forEach(function (k) { A.byZone[zid][k].forEach(function (e) { if (!out[e.tech]) { out[e.tech] = { tech: e.tech, days: 0, kind: e.kind, dates: [], ov: e.ov }; order.push(e.tech); } out[e.tech].days++; out[e.tech].dates.push(k); if (e.kind !== "default" && e.kind !== "off") { out[e.tech].kind = e.kind; out[e.tech].ov = e.ov; } }); });
    return order.map(function (t) { return out[t]; });
  }
  function visitsFor(list, zid, tid) {
    var rows = zoneTechs(list, zid), total = 0, mine = 0;
    rows.forEach(function (e) { var w = e.kind === "temp" && e.ov && e.ov.partial ? 0.5 : 1; total += e.days * w; if (e.tech === tid) mine = e.days * w; });
    if (!total) return 0;
    return Math.round(ZI[zid].demand * mine / total);
  }
  function sampleVisits(list, zid, tid) {
    var e = zoneTechs(list, zid).filter(function (x) { return x.tech === tid; })[0]; if (!e) return { rows: [], more: 0 };
    var n = visitsFor(list, zid, tid), dates = e.dates.filter(function (k) { return !(ZI[zid].backfillDates || []).length || ZI[zid].backfillDates.indexOf(k) < 0; }), rows = [], i = 0;
    var seed = (parseInt(tid.slice(2), 10) * 7 + parseInt(zid.slice(3), 10)) % 5;
    for (var d = 0; d < dates.length && rows.length < 6; d++) {
      var per = Math.min(3, Math.max(1, Math.round(n / Math.max(1, dates.length))));
      for (var j = 0; j < per && rows.length < 6; j++) {
        var pinned = zid === "HV-11" && tid === "T-1057" && dates[d] === "2026-10-08" && j < 3;
        rows.push({ date: dates[d], type: D.jobTypes[(seed + i) % D.jobTypes.length], dur: "1 h", sla: pinned ? "Confirmed · parts allocated" : D.slaTypes[(seed + i) % D.slaTypes.length], pinned: pinned }); i++;
      }
    }
    return { rows: rows, more: Math.max(0, n - rows.length) };
  }

  /* ---------------- KPIs (methodology) ---------------- */
  var kmemo = {};
  function kpis(list) {
    var key = keyOf(list); if (kmemo[key]) return kmemo[key];
    var A = alloc(list), ch = D.changes.filter(function (c) { return list.indexOf(c.id) >= 0; }), out = { techs: {}, zones: {}, fleet: {} }, sumProd = 0, sumJobs = 0, sumWD = 0;
    D.techs.forEach(function (t) {
      var wd = WD.length - Object.keys(A.absent[t.id]).length, off = 0, jobs = t.jobs;
      Object.keys(A.byTech[t.id]).forEach(function (k) { if (A.byTech[t.id][k].some(function (e) { return e.kind === "off"; })) off++; });
      ch.forEach(function (c) { if (c.effects.jobs && c.effects.jobs[t.id]) jobs += c.effects.jobs[t.id]; });
      var dwj = Math.max(1, wd - off), prod = r2(jobs / dwj), cap = Math.min(100, Math.round(jobs / (wd * D.capacityPerDay) * 100));
      out.techs[t.id] = { workingDays: wd, daysWithJobs: dwj, jobs: jobs, prod: prod, cap: cap };
      sumProd += prod; sumJobs += jobs; sumWD += wd;
    });
    var wsum = 0, dsum = 0;
    D.zones.forEach(function (z) { var w = z.wait; ch.forEach(function (c) { if (c.effects.waits && c.effects.waits[z.id]) w += c.effects.waits[z.id]; }); w = r1(w); out.zones[z.id] = { wait: w }; wsum += w * z.demand; dsum += z.demand; });
    var prods = Object.keys(out.techs).map(function (k) { return out.techs[k].prod; });
    out.fleet = { prodRaw: sumProd / D.techs.length, prod: r2(sumProd / D.techs.length), cap: Math.round(sumJobs / (sumWD * D.capacityPerDay) * 100), wait: r1(wsum / dsum), jobs: sumJobs, techDays: sumWD, spread: r2(Math.max.apply(null, prods) - Math.min.apply(null, prods)) };
    kmemo[key] = out; return out;
  }
  function pct(a, b) { return Math.round((b - a) / a * 1000) / 10; }
  function signed(x, dp, unit) { var v = dp ? Math.abs(x).toFixed(dp) : String(Math.abs(x)); return (x > 0 ? "+" : x < 0 ? "−" : "±") + v + (unit || ""); }
  function delta(before, after, opts) { /* opts: {unit, dp, lowerIsBetter, diff} */
    opts = opts || {};
    var dp = opts.dp === undefined ? 1 : opts.dp, u = opts.unit || "";
    if (after === undefined || after === null) return "<b>" + before.toFixed(dp) + u + "</b>";
    var cls = after === before ? "flat" : (after > before ? (opts.lowerIsBetter ? "up-bad" : "up-good") : (opts.lowerIsBetter ? "down-good" : "down-bad"));
    var diff = opts.diff && after !== before ? ' <em class="diff ' + cls + '">' + signed(r2(after - before), dp, u) + "</em>" : "";
    return before.toFixed(dp) + u + ' <span class="delta ' + cls + '">→ ' + after.toFixed(dp) + u + "</span>" + diff;
  }
  function flagsFor(list) { return D.flagsFor(list); }
  function zoneFlag(list, zid) { return flagsFor(list).filter(function (f) { return f.zone === zid && !f.tech; })[0]; }
  function techFlag(list, tid) { return flagsFor(list).filter(function (f) { return f.tech === tid; })[0]; }

  /* ---------------- rendering: shell + KPI band ---------------- */
  function renderPlanState() {
    var el = $("#plan-state");
    if (!S.ran) { el.innerHTML = '<span class="chip chip--muted">Current allocation · from the field-service system</span><span>No optimized plan for this period yet · ' + flagsFor([]).length + " open problems flagged</span>"; $("#version-chip").textContent = "v1.0"; return; }
    var acc = D.zones.filter(function (z) { return S.decisions[z.id].status === "accepted"; }).length, rej = D.zones.filter(function (z) { return S.decisions[z.id].status === "rejected"; }).length;
    el.innerHTML = '<span class="chip chip--live">Plan ' + esc(planLabel()) + (S.version === "v2" ? " · with feedback" : " · optimized") + "</span><span>" + acc + " accepted · " + rej + " rejected · " + (D.zones.length - acc - rej) + " pending</span>";
    $("#version-chip").textContent = "v1.0 · plan " + planLabel();
  }
  function renderKpiBand() {
    var el = $("#kpi-band");
    if (!S.ran) { el.hidden = true; return; }
    var B = kpis([]), K = kpis(S.applied), ch = changedZones(S.applied).length, fl = flagsFor(S.applied), n = S.applied.length;
    function tile(cls, label, big, sub, act) { return '<button class="kpi-tile ' + cls + '" type="button"' + (act ? ' data-kpi="' + act + '"' : "") + '><span class="kpi-label">' + label + '</span><span class="kpi-big">' + big + '</span><span class="kpi-sub">' + sub + "</span></button>"; }
    var pp = pct(B.fleet.prodRaw, K.fleet.prodRaw), cp = K.fleet.cap - B.fleet.cap, wd = r1(K.fleet.wait - B.fleet.wait), jd = K.fleet.jobs - B.fleet.jobs;
    el.innerHTML = '<div class="kpi-band-head"><span class="eyebrow">What improved · plan ' + esc(planLabel()) + ' vs today\'s allocation</span><span class="muted">same formulas on both plans · ' + esc(D.period.short) + "</span></div><div class=\"kpi-tiles\">" +
      tile(pp > 0 ? "good" : pp < 0 ? "bad" : "", "Jobs per technician per day", signed(pp, 1, "%"), B.fleet.prod.toFixed(2) + " → <b>" + K.fleet.prod.toFixed(2) + "</b>", "tech") +
      tile(cp > 0 ? "good" : cp < 0 ? "bad" : "", "Capacity used", signed(cp, 0, " pts"), B.fleet.cap + "% → <b>" + K.fleet.cap + "%</b>", "tech") +
      tile(wd < 0 ? "good" : wd > 0 ? "bad" : "", "Avg wait, booking → visit", signed(wd, 1, " d"), B.fleet.wait.toFixed(1) + " d → <b>" + K.fleet.wait.toFixed(1) + " d</b>", "zone") +
      tile(jd > 0 ? "good" : jd < 0 ? "bad" : "", "Visits placed in the period", signed(jd, 0), B.fleet.jobs.toLocaleString("en-US") + " → <b>" + K.fleet.jobs.toLocaleString("en-US") + "</b> of " + D.zones.reduce(function (a, z) { return a + z.demand; }, 0).toLocaleString("en-US") + " booked", "zone") +
      '<div class="kpi-tile kpi-tile--changes"><span class="kpi-label">What changed</span><span class="kpi-big">' + n + '</span><span class="kpi-sub"><b>' + n + " changes</b> in " + ch + " zones · " + fl.length + (fl.length === 1 ? " flag" : " flags") + (S.undone.length ? " · " + S.undone.length + " undone by you" : "") + '</span><button class="btn btn--primary btn--xs" id="btn-review-changes" type="button">Review changes' + ICON.chev + "</button></div></div>";
    el.hidden = false;
  }
  $("#kpi-band").addEventListener("click", function (e) {
    var t;
    if ((t = e.target.closest("#btn-review-changes"))) { reviewChanges(); return; }
    if ((t = e.target.closest("[data-kpi]"))) { setSched(t.dataset.kpi); $("#schedule").scrollIntoView({ behavior: "smooth", block: "start" }); }
  });
  function reviewChanges() {
    $("#changes").hidden = false;
    var first = $("#chg-list li"); if (first) first.scrollIntoView({ behavior: "smooth", block: "nearest" });
    $("#changes").classList.add("is-lit"); setTimeout(function () { $("#changes").classList.remove("is-lit"); }, 1200);
    tour.after("review");
  }
  $("#avatar").textContent = D.user.initials; $("#avatar").title = D.user.name + " · " + D.user.role;

  /* ---------------- rendering: changes list ---------------- */
  function changeEffect(c) {
    /* live effect text from the KPI engine: the zones the change touches, before → after */
    var B = kpis([]), K = kpis(S.applied), parts = [];
    if (c.effects.waits) Object.keys(c.effects.waits).forEach(function (z) { if (c.effects.waits[z]) parts.push(z + " wait " + B.zones[z].wait.toFixed(1) + " → " + (on(c.id) ? K.zones[z].wait.toFixed(1) : r1(B.zones[z].wait + c.effects.waits[z]).toFixed(1)) + " d"); });
    return parts.length && c.id !== "packing" ? parts.join(" · ") : c.effect;
  }
  function renderChanges() {
    var el = $("#changes");
    if (!S.ran) { el.hidden = true; return; }
    var rows = D.changes.filter(function (c) { return on(c.id) || S.undone.indexOf(c.id) >= 0; });
    var fl = flagsFor(S.applied);
    $("#chg-title").textContent = S.applied.length + " changes · " + changedZones(S.applied).length + " zones · " + fl.length + (fl.length === 1 ? " flag" : " flags");
    $("#btn-changes-only").classList.toggle("is-on", S.changesOnly); $("#btn-changes-only").setAttribute("aria-pressed", String(S.changesOnly));
    $("#btn-reopt").hidden = !canReopt();
    $("#chg-list").innerHTML = rows.map(function (c) {
      var undone = S.undone.indexOf(c.id) >= 0, flagged = !undone && (c.kind === "worsens" || c.flagged);
      var glyph = undone ? ICON.undo : c.kind === "worsens" ? ICON.down : c.kind === "improves" ? ICON.up : flagged ? ICON.flag : ICON.check;
      var cls = undone ? "undone" : c.kind === "worsens" ? "worsens" : c.kind === "improves" ? "improves" : "neutral";
      var note = S.notes[c.id] ? '<span class="chg-note">“' + esc(S.notes[c.id]) + "”</span>" : "";
      return '<li class="chg ' + cls + (S.focus === c.id ? " is-focus" : "") + (flagged ? " is-flag" : "") + '" data-change="' + c.id + '"><div class="chg-main" data-open="' + c.id + '"><span class="chg-glyph">' + glyph + '</span><div class="chg-text"><span class="chg-rule">' + esc(c.rule) + (flagged ? ' <i class="chg-flagtag">' + (c.kind === "worsens" ? "made it worse" : "confirm") + "</i>" : "") + (undone ? ' <i class="chg-flagtag chg-flagtag--undo">undone · manual fix</i>' : "") + '</span><b>' + esc(c.title) + '</b><span class="chg-effect">' + esc(changeEffect(c)) + "</span>" + note + "</div></div>" +
        '<div class="chg-actions"><button class="btn btn--ghost btn--xs" type="button" data-open="' + c.id + '" title="Show on the map and in the schedule">' + ICON.eye + "Show</button>" +
        (undone ? '<button class="btn btn--ghost btn--xs" type="button" data-restore="' + c.id + '">Restore</button>' : '<button class="btn btn--ghost btn--xs" type="button" data-undo="' + c.id + '" title="Undo this change — a manual fix">' + ICON.undo + "Undo</button>") +
        '<button class="btn btn--ghost btn--xs" type="button" data-note="' + c.id + '">' + ICON.chat + (S.notes[c.id] ? "Edit note" : "Note") + "</button></div></li>";
    }).join("");
    el.hidden = false;
  }
  $("#changes").addEventListener("click", function (e) {
    var t;
    if ((t = e.target.closest("[data-undo]"))) { undoChange(t.dataset.undo); return; }
    if ((t = e.target.closest("[data-restore]"))) { restoreChange(t.dataset.restore); return; }
    if ((t = e.target.closest("[data-note]"))) { openComment({ kind: "change", id: t.dataset.note }); return; }
    if ((t = e.target.closest("[data-open]"))) { openChange(t.dataset.open); return; }
    if ((t = e.target.closest("#btn-changes-only"))) { S.changesOnly = !S.changesOnly; renderMaps(); renderSchedule(); renderChanges(); return; }
    if ((t = e.target.closest("#btn-reopt"))) { reoptimize(); tour.after("reopt"); }
  });
  var FOCUS = { packing: null, vacation: { kind: "zone", id: "HV-04" }, sick: { kind: "zone", id: "HV-10" }, coverage: { kind: "zone", id: "HV-02" }, capacity: { kind: "tech", id: "T-1048" }, "marsh-move": { kind: "zone", id: "HV-09" }, "marsh-keep": { kind: "zone", id: "HV-10" }, specialist: { kind: "zone", id: "HV-12" }, pinned: { kind: "zone", id: "HV-11" }, backfill: { kind: "zone", id: "HV-07" }, spare: { kind: "tech", id: "T-1058" } };
  function openChange(id) {
    var c = CI[id]; if (!c) return;
    S.focus = id; S.week = c.week;
    var f = FOCUS[id] || null;
    if (f) { S.sel.opt = f; if (S.view === "compare") S.sel.cur = f; } else { S.sel = { cur: null, opt: null }; }
    var want = f && f.kind === "tech" ? "tech" : "zone";
    if (S.sched !== want) { S.sched = want; $$("#view-seg button").forEach(function (b) { b.classList.toggle("is-active", b.dataset.view === want); }); }
    renderMaps(); renderSchedule(); renderChanges();
    var row = $("#grid tr.is-focus"); if (row) row.scrollIntoView({ behavior: "smooth", block: "nearest" });
    tour.after(id === "vacation" ? "change-vacation" : "");
  }
  function undoChange(id) {
    if (!on(id)) return;
    var c = CI[id], before = kpis(S.applied);
    S.applied = S.applied.filter(function (x) { return x !== id; }); S.undone.push(id); S.focus = id;
    var after = kpis(S.applied), fl = flagsFor(S.applied).filter(function (f) { return c.zones.indexOf(f.zone) >= 0 && !(f.kind === "backfill"); });
    log("Undone: " + c.title, "Manual fix · " + c.rule + " · " + USER, "warn");
    var eff = c.effects.waits ? Object.keys(c.effects.waits).filter(function (z) { return c.effects.waits[z]; }).map(function (z) { return ZI[z].name + " wait " + before.zones[z].wait.toFixed(1) + " → " + after.zones[z].wait.toFixed(1) + " d"; }).join(" · ") : "";
    toast("<b>Undone.</b> " + (eff ? eff + ". " : "") + "Fleet " + before.fleet.prod.toFixed(2) + " → " + after.fleet.prod.toFixed(2) + " jobs/day." + (fl.length ? " Flagged: " + fl.map(function (f) { return f.title.toLowerCase(); }).join(", ") + "." : ""), 6000);
    renderAll();
    tour.after(id === "marsh-move" ? "undo" : "");
  }
  function restoreChange(id) {
    if (on(id)) return;
    S.applied.push(id); S.undone = S.undone.filter(function (x) { return x !== id; }); S.focus = id;
    log("Restored: " + CI[id].title, "The solver's change is back in the plan · " + USER, "");
    renderAll();
  }
  function canReopt() { return S.ran && S.version !== "v2" && (S.undone.length > 0 || D.zones.some(function (z) { return S.decisions[z.id].status === "rejected"; })); }

  /* ---------------- rendering: maps ---------------- */
  function pillW(s) { return Math.round(s.length * 6.3 + 22); }
  function mapSvg(card, list) {
    var m = D.map, fz = S.filters.zones, ft = S.filters.techs, sel = S.sel[card], isOpt = card === "opt" && S.ran;
    var B = kpis([]), K = kpis(list);
    var s = '<svg class="map" viewBox="0 -30 ' + m.w + " " + (m.h + 30) + '" preserveAspectRatio="xMidYMid meet" aria-label="Schematic map of the region">';
    s += '<rect x="-400" y="-200" width="1800" height="700" fill="#F6F7F9"/>';
    s += '<polygon class="sea" points="' + m.sea.map(function (p) { return p.join(","); }).join(" ") + '"/>';
    D.zones.forEach(function (z) {
      var changed = isOpt && zoneChanged(list, z.id);
      var dim = (fz.length && fz.indexOf(z.id) < 0) || (S.changesOnly && isOpt && !changed), isSel = sel && sel.kind === "zone" && sel.id === z.id;
      s += '<path class="zone' + (dim ? " is-dim" : "") + (isSel ? " is-selected" : "") + (changed ? " is-changed" : "") + '" data-zone="' + z.id + '" data-card="' + card + '" fill="' + z.color + '" d="M' + z.poly.map(function (p) { return p[0] + "," + p[1]; }).join("L") + 'Z"><title>' + esc(z.label) + "</title></path>";
    });
    s += '<path class="river" d="' + m.river + '"/><path class="river-in" d="' + m.river + '"/>';
    m.roads.forEach(function (r) { s += '<line class="road" x1="' + r[0][0] + '" y1="' + r[0][1] + '" x2="' + r[1][0] + '" y2="' + r[1][1] + '"/><line class="road-in" x1="' + r[0][0] + '" y1="' + r[0][1] + '" x2="' + r[1][0] + '" y2="' + r[1][1] + '"/>'; });
    s += '<ellipse class="road" cx="' + m.ring.cx + '" cy="' + m.ring.cy + '" rx="' + m.ring.rx + '" ry="' + m.ring.ry + '"/><ellipse class="road-in" cx="' + m.ring.cx + '" cy="' + m.ring.cy + '" rx="' + m.ring.rx + '" ry="' + m.ring.ry + '"/>';
    s += '<text class="place" x="' + m.harbourLabel[0] + '" y="' + m.harbourLabel[1] + '" text-anchor="middle">HARBOUR</text>';
    var selTech = sel && sel.kind === "tech" ? sel.id : null;
    var routeFor = function (tid) { var t = TI[tid]; techZones(list, tid).forEach(function (e) { var z = ZI[e.zone]; s += '<line class="route ' + (e.kind === "temp" || e.kind === "moved" ? e.kind : "") + '" x1="' + t.home[0] + '" y1="' + t.home[1] + '" x2="' + z.c[0] + '" y2="' + z.c[1] + '"/>'; }); };
    if (selTech) routeFor(selTech); else if (ft.length) ft.forEach(routeFor);
    D.zones.forEach(function (z) {
      var changed = isOpt && zoneChanged(list, z.id);
      if ((fz.length && fz.indexOf(z.id) < 0) || (S.changesOnly && isOpt && !changed)) return;
      var rows = zoneTechs(list, z.id), n = rows.filter(function (e) { return e.kind !== "off"; }).length, fl = zoneFlag(list, z.id);
      var w0 = B.zones[z.id].wait, w1 = K.zones[z.id].wait, dw = isOpt ? r1(w1 - w0) : 0;
      var txt = n + " tech · " + w1.toFixed(1) + " d" + (dw ? " ▼" + Math.abs(dw).toFixed(1) : "") + (fl ? " ⚑" : ""), w = pillW(txt) + 8;
      s += '<text class="zlabel" x="' + z.c[0] + '" y="' + (z.c[1] - 14) + '" text-anchor="middle">' + esc(z.label) + "</text>";
      s += '<g class="zpill' + (fl ? " is-warn" : "") + '" transform="translate(' + (z.c[0] - w / 2) + "," + (z.c[1] - 6) + ')"><rect width="' + w + '" height="20" rx="10"/><text x="10" y="14"><tspan class="k">' + n + "</tspan> tech · " + w1.toFixed(1) + " d" + (dw ? '<tspan class="' + (dw < 0 ? "dgood" : "dbad") + '">' + (dw < 0 ? " ▼" : " ▲") + Math.abs(dw).toFixed(1) + "</tspan>" : "") + (fl ? '<tspan class="dbad"> ⚑</tspan>' : "") + "</text></g>";
    });
    D.techs.forEach(function (t) {
      var dim = (ft.length && ft.indexOf(t.id) < 0) || (fz.length && !t.zones.some(function (z) { return fz.indexOf(z) >= 0; })) || (S.changesOnly && isOpt && !techChanged(list, t.id));
      var isSel = selTech === t.id, sp = t.skill === "Specialist";
      s += '<g class="home' + (dim ? " is-dim" : "") + (isSel ? " is-selected" : "") + '" data-tech="' + t.id + '" data-card="' + card + '" transform="translate(' + t.home[0] + "," + t.home[1] + ')">' + (isSel ? '<circle class="ring" r="13"/>' : "") + '<circle class="o' + (sp ? " sp" : "") + '" r="7"/><path d="M-3.2 0.6 0 -2.6 3.2 0.6M-2.4 0v2.9h4.8V0"/><title>' + t.id + " · " + t.skill + "</title></g>";
    });
    s += "</svg>";
    return s;
  }
  function mapCard(card, list, title) {
    var banner = "";
    if (card === "opt" && !S.ran) banner = '<div class="banner">No optimized plan yet — <b>run the optimization</b> to see the proposal</div>';
    var changed = card === "opt" && S.ran ? changedZones(list).length : 0;
    return '<div class="mapcard" data-card="' + card + '"><div class="map-head"><h2>' + esc(title) + " <span>— " + D.zones.length + " zones" + (changed ? " · " + changed + " changed" : "") + "</span></h2>" +
      '<div class="map-tools"><button class="icon-btn" type="button" title="Fit to region" aria-label="Fit to region"><svg viewBox="0 0 24 24"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg></button></div></div>' +
      '<div class="map-wrap">' + banner + '<div class="zoom"><button type="button" aria-label="Zoom in">+</button><button type="button" aria-label="Zoom out">−</button></div>' + mapSvg(card, list) + '<span class="map-note">Schematic map · ' + esc(D.region.name) + "</span>" + detailsHtml(card, list) + "</div>" +
      '<div class="legend"><span><i class="sw"></i>Service zone</span>' + (card === "opt" && S.ran ? '<span><i class="sw sw--changed"></i>Changed by the solver</span>' : "") + '<span><i class="dot"></i>Technician home</span><span><i class="ln"></i>Default zone route</span><span><i class="ln ln--dash"></i>Temporary zone route</span><span><i class="home"></i>Specialist</span></div></div>';
  }
  function renderMaps() {
    var el = $("#maps");
    el.classList.toggle("is-compare", S.view === "compare");
    $("#plan-row").classList.toggle("is-single", !S.ran);
    if (S.view === "compare") el.innerHTML = mapCard("cur", [], "Current allocation") + mapCard("opt", applied(), "Optimized allocation");
    else if (S.view === "cur") el.innerHTML = mapCard("cur", [], "Current allocation");
    else el.innerHTML = mapCard("opt", applied(), S.ran ? "Optimized allocation" : "Service zones");
    tour.reposition();
  }
  $("#maps").addEventListener("click", function (e) {
    var t;
    if ((t = e.target.closest("[data-close-details]"))) { S.sel[t.dataset.closeDetails] = null; renderMaps(); renderSchedule(); return; }
    if ((t = e.target.closest("[data-toggle-item]"))) { t.closest(".d-item").classList.toggle("is-open"); tour.reposition(); return; }
    if ((t = e.target.closest("[data-jump-zone]"))) { selectZone(t.dataset.card, t.dataset.jumpZone); return; }
    if ((t = e.target.closest("[data-jump-tech]"))) { selectTech(t.dataset.card, t.dataset.jumpTech); return; }
    if ((t = e.target.closest(".zone[data-zone]"))) { selectZone(t.dataset.card, t.dataset.zone); return; }
    if ((t = e.target.closest(".home[data-tech]"))) { selectTech(t.dataset.card, t.dataset.tech); return; }
    if ((t = e.target.closest(".zoom button, .map-tools button"))) { toast("The schematic map has one zoom level in this walkthrough."); }
  });
  function selectZone(card, zid) { S.sel[card] = { kind: "zone", id: zid }; renderMaps(); renderSchedule(); }
  function selectTech(card, tid) { S.sel[card] = { kind: "tech", id: tid }; renderMaps(); renderSchedule(); tour.after(card === "opt" && tid === "T-1048" ? "tech-row" : ""); }

  /* ---------------- rendering: details ---------------- */
  function kindLabel(k, partial) { return k === "temp" ? (partial ? "temporary · part of the day" : "temporary") : k === "moved" ? "moved here" : k === "pinned" ? "non-movable kept" : k === "backfill" ? "historical demand" : k === "off" ? "no visits" : "default"; }
  function whyBox(o, cls) { if (!o) return ""; return '<div class="why' + (cls ? " " + cls : "") + '"><b>' + esc(o.rule) + "</b>" + esc(o.why) + (o.alts ? '<ul class="alts">' + o.alts.map(function (a) { return "<li" + (a.chosen ? ' class="is-chosen"' : "") + "><b>" + esc(a.name) + "</b> " + esc(a.effect) + "</li>"; }).join("") + "</ul>" : "") + "</div>"; }
  function visitsTable(list, zid, tid) {
    var v = sampleVisits(list, zid, tid); if (!v.rows.length) return '<div class="muted" style="font-size:11.5px;padding:4px 0">No booked visits on these dates — allocated on historical demand.</div>';
    return '<table class="visits">' + v.rows.map(function (r) { return "<tr><td>" + esc(fmtShort(r.date)) + "</td><td>" + esc(r.type) + "</td><td>" + esc(r.dur) + "</td><td" + (r.pinned ? ' class="pin"' : "") + ">" + (r.pinned ? "⚑ " : "") + esc(r.sla) + "</td></tr>"; }).join("") + (v.more ? '<tr><td colspan="4" class="more">+ ' + v.more + " more booked visits</td></tr>" : "") + "</table>";
  }
  function detailsHtml(card, list) {
    var sel = S.sel[card]; if (!sel) return "";
    var B = kpis([]), K = kpis(list), after = card === "opt" && S.ran, body = "";
    if (sel.kind === "zone") {
      var z = ZI[sel.id], rows = zoneTechs(list, z.id), fl = zoneFlag(list, z.id);
      body += '<div class="d-title"><span class="zdot" style="background:' + z.color + '"></span><b>' + esc(z.label) + "</b></div><div class=\"d-kind\">" + esc(z.kind) + "</div>";
      body += '<div class="pcs">' + z.postcodes.map(function (p) { return "<span>" + esc(p) + "</span>"; }).join("") + "</div>";
      body += '<div class="d-kpi"><div><span>Avg wait, booking → visit</span><b>' + delta(B.zones[z.id].wait, after ? K.zones[z.id].wait : undefined, { unit: " d", lowerIsBetter: true, diff: true }) + "</b></div><div><span>Booked visits</span><b>" + z.demand + (z.backfill ? ' <span class="muted">+ ' + z.backfill + " on history</span>" : "") + "</b></div></div>";
      if (fl) body += '<div class="why ' + (fl.kind === "backfill" ? "warn" : "bad") + '"><b>' + esc(fl.title) + "</b>" + esc(fl.text) + "</div>";
      body += '<span class="eyebrow">Technicians · ' + rows.filter(function (e) { return e.kind !== "off"; }).length + "</span><ul class=\"d-list\">";
      rows.forEach(function (e) {
        var t = TI[e.tech], n = visitsFor(list, z.id, e.tech);
        body += '<li class="d-item' + (e.kind === "temp" || e.kind === "moved" ? " is-temp" : "") + '"><div class="d-item-head" data-toggle-item><b>' + ICON.user + esc(t.id) + ' <span class="chip chip--skill' + (t.skill === "Specialist" ? " chip--specialist" : "") + '">' + esc(t.skill) + '</span></b><span class="meta">' + n + " visits · " + e.days + (e.days === 1 ? " day" : " days") + " · " + kindLabel(e.kind, e.ov && e.ov.partial) + "</span>" + ICON.chev + '</div><div class="d-item-body">' + visitsTable(list, z.id, e.tech) + '<div style="margin-top:6px"><button class="btn btn--ghost btn--xs" type="button" data-jump-tech="' + t.id + '" data-card="' + card + '">Show ' + esc(t.id) + " on the map</button></div></div></li>";
      });
      body += "</ul>";
      var whys = []; rows.forEach(function (e) { if (e.ov && whys.indexOf(e.ov) < 0) whys.push(e.ov); });
      if (whys.length) { body += '<span class="eyebrow">Why this allocation</span>' + whys.map(function (o) { return whyBox(o, o.kind === "moved" ? "warn" : ""); }).join(""); }
    } else {
      var t2 = TI[sel.id], zl = techZones(list, t2.id), tb = B.techs[t2.id], tk = after ? K.techs[t2.id] : null, tf = techFlag(list, t2.id), tf0 = techFlag([], t2.id);
      body += '<div class="d-title">' + ICON.user + "<b>" + esc(t2.id) + '</b><span class="chip chip--skill' + (t2.skill === "Specialist" ? " chip--specialist" : "") + '">' + esc(t2.skill) + "</span></div>";
      body += '<div class="d-kind">Home: ' + esc(ZI[t2.zones[0]].label) + " · " + esc(t2.homePostcode) + " · default zone" + (t2.zones.length > 1 ? "s" : "") + ": " + t2.zones.join(", ") + (t2.absent.length ? " · " + t2.absent.map(function (a) { return a.kind.toLowerCase() + " " + fmtShort(a.from) + (a.to !== a.from ? " – " + fmtShort(a.to) : ""); }).join(", ") : "") + "</div>";
      body += '<div class="d-kpi"><div><span>Capacity used</span><b>' + delta(tb.cap, tk ? tk.cap : undefined, { unit: "%", dp: 0, diff: true }) + "</b></div><div><span>Jobs per working day</span><b>" + delta(tb.prod, tk ? tk.prod : undefined, { dp: 2, diff: true }) + "</b></div><div><span>Visits in the period</span><b>" + (tk ? tb.jobs + ' <span class="delta ' + (tk.jobs > tb.jobs ? "up-good" : tk.jobs < tb.jobs ? "down-bad" : "flat") + '">→ ' + tk.jobs + "</span>" : tb.jobs) + "</b></div><div><span>Working days</span><b>" + tb.workingDays + " of " + WD.length + "</b></div></div>";
      if (tf) body += '<div class="why bad"><b>' + esc(tf.title) + "</b>" + esc(tf.text) + "</div>";
      else if (after && tf0) body += '<div class="why ok"><b>Fixed in the optimized plan</b>' + esc(tf0.text) + " Two movable visits now go to T-1050 on that day, so T-1048 is at 7.</div>";
      body += '<span class="eyebrow">Zones · ' + zl.filter(function (e) { return e.kind !== "off"; }).length + "</span><ul class=\"d-list\">";
      zl.forEach(function (e) {
        var z2 = ZI[e.zone], n2 = visitsFor(list, z2.id, t2.id);
        body += '<li class="d-item' + (e.kind === "temp" || e.kind === "moved" ? " is-temp" : "") + '"><div class="d-item-head" data-toggle-item><b><span class="zdot" style="background:' + z2.color + '"></span>' + esc(z2.label) + '</b><span class="meta">' + n2 + " visits · " + e.days + (e.days === 1 ? " day" : " days") + " · " + kindLabel(e.kind, e.ov && e.ov.partial) + "</span>" + ICON.chev + '</div><div class="d-item-body">' + visitsTable(list, z2.id, t2.id) + '<div style="margin-top:6px"><button class="btn btn--ghost btn--xs" type="button" data-jump-zone="' + z2.id + '" data-card="' + card + '">Show ' + esc(z2.label) + " on the map</button></div></div></li>";
      });
      body += "</ul>";
      var whys2 = []; zl.forEach(function (e) { if (e.ov && whys2.indexOf(e.ov) < 0) whys2.push(e.ov); });
      if (whys2.length) { body += '<span class="eyebrow">Why this allocation</span>' + whys2.map(function (o) { return whyBox(o, o.kind === "moved" ? "warn" : ""); }).join(""); }
    }
    return '<div class="details" data-details="' + card + '"><div class="details-head"><div><strong>Details</strong><span class="sub">' + ICON.cal + esc(D.period.short) + " · plan " + (card === "cur" ? "current" : esc(planLabel())) + '</span></div><button class="icon-btn" type="button" aria-label="Close" data-close-details="' + card + '">' + ICON.x + '</button></div><div class="details-body">' + body + "</div></div>";
  }

  /* ---------------- rendering: schedule ---------------- */
  function pill(label, kind, extra, isZone) {
    var g = kind === "temp" ? "↓ " : kind === "moved" ? "↑ " : kind === "off" ? "— " : kind === "backfill" ? "≈ " : "";
    return '<span class="pill pill--' + kind + (isZone ? " pill--zone" : "") + '" title="' + esc(kindLabel(kind)) + '">' + g + esc(label) + (extra ? " <i>" + esc(extra) + "</i>" : "") + "</span>";
  }
  function renderSchedule() {
    var list = applied(), A = alloc(list), B = kpis([]), K = S.ran ? kpis(list) : null, wk = D.days.filter(function (d) { return d.week === S.week; }), fc = S.focus ? CI[S.focus] : null;
    $("#sched-week").textContent = "Week " + S.week + " of " + D.weeks.length + " · " + D.weeks[S.week - 1].label;
    $("#week-prev").disabled = S.week === 1; $("#week-next").disabled = S.week === D.weeks.length;
    $("#btn-accept-remaining").hidden = !S.ran;
    var fz = S.filters.zones, ft = S.filters.techs;
    var head = "", body = "";
    var dayHead = wk.map(function (d) { return "<th" + (d.working ? "" : ' class="nonwork"') + ">" + d.dow + "<b>" + d.n + "</b>" + (d.holiday ? '<span class="hol">' + esc(d.holiday) + "</span>" : "") + "</th>"; }).join("");
    if (S.sched === "zone") {
      head = '<tr><th class="first"><b>Zone</b><span class="muted">' + esc(D.period.short) + '</span><span class="kpi-line">' + ICON.clock + delta(B.fleet.wait, K ? K.fleet.wait : undefined, { unit: " d", lowerIsBetter: true, diff: true }) + " avg wait</span></th>" + dayHead + '<th class="dec">Decision<span class="muted" style="display:block;text-transform:none;letter-spacing:0;margin-top:2px">whole period · ' + esc(D.period.short) + "</span></th></tr>";
      var rows = D.zones.filter(function (z) { return (!fz.length || fz.indexOf(z.id) >= 0) && (!ft.length || zoneTechs(list, z.id).some(function (e) { return ft.indexOf(e.tech) >= 0; })) && (!S.changesOnly || !S.ran || zoneChanged(list, z.id) || zoneFlag(list, z.id)); });
      rows.forEach(function (z) {
        var fl = zoneFlag(list, z.id), dec = S.decisions[z.id], sel = S.sel[S.view === "cur" ? "cur" : "opt"], isSel = sel && sel.kind === "zone" && sel.id === z.id, isFocus = fc && fc.id !== "packing" && fc.zones.indexOf(z.id) >= 0;
        var first = '<td class="first"><div class="row-name"><span class="zdot" style="background:' + z.color + '"></span>' + esc(z.label) + '</div><div class="row-sub">' + esc(D.period.short) + '</div><div class="row-kpi">' + ICON.clock + "<span>" + delta(B.zones[z.id].wait, K ? K.zones[z.id].wait : undefined, { unit: " d", lowerIsBetter: true, diff: true }) + ' avg wait</span></div><div class="row-kpi">' + ICON.pin + "<span>" + z.postcodes.length + " postcodes</span></div>" + (fl ? '<div class="row-flag' + (fl.kind === "backfill" ? "" : " bad") + '">' + ICON.warn + esc(fl.title) + "</div>" : "") + "</td>";
        var cells = wk.map(function (d) {
          if (!d.working) return '<td class="nonwork"></td>';
          var cl = (A.byZone[z.id][d.d] || []).filter(function (e) { return !ft.length || ft.indexOf(e.tech) >= 0; }), chg = S.ran && zoneCellChanged(list, z.id, d.d);
          return "<td" + (chg ? ' class="is-changed"' : "") + '><div class="cell-pills">' + cl.map(function (e) { return pill(e.tech, e.kind, e.kind === "pinned" ? "3 fixed" : e.kind === "temp" && e.partial ? "part" : ""); }).join("") + "</div></td>";
        }).join("");
        var decision;
        if (!S.ran) decision = '<td class="dec"><span class="muted">—</span></td>';
        else if (dec.status === "pending" || dec.status === "reproposed") decision = '<td class="dec"><div class="decision">' + (dec.status === "reproposed" ? '<span class="status status--reproposed">Re-proposed</span>' : "") + '<button class="btn btn--ok" type="button" data-decide="accepted" data-zone="' + z.id + '">' + ICON.check + 'Accept</button><button class="btn btn--danger" type="button" data-decide="rejected" data-zone="' + z.id + '">' + ICON.x + 'Reject</button><button class="btn btn--ghost" type="button" data-comment="' + z.id + '">' + ICON.chat + "Note</button>" + (dec.comment ? '<span class="cmt">“' + esc(dec.comment) + "”</span>" : "") + "</div></td>";
        else decision = '<td class="dec"><div class="decision"><span class="status status--' + dec.status + '">' + (dec.status === "accepted" ? ICON.check + "Accepted" : ICON.x + "Rejected") + '</span><button class="btn btn--ghost" type="button" data-comment="' + z.id + '">' + ICON.chat + 'Note</button><button class="btn btn--ghost btn--xs" type="button" data-decide="pending" data-zone="' + z.id + '">Reopen</button>' + (dec.comment ? '<span class="cmt">“' + esc(dec.comment) + "”</span>" : "") + "</div></td>";
        body += '<tr class="clickable' + (isSel ? " is-selected" : "") + (fl ? " is-flag" : "") + (isFocus ? " is-focus" : "") + '" data-zone="' + z.id + '">' + first + cells + decision + "</tr>";
      });
      if (!rows.length) body = '<tr><td colspan="' + (wk.length + 2) + '" class="empty-plan">No zone matches the filters.</td></tr>';
    } else {
      head = '<tr><th class="first"><b>Technician</b><span class="muted">' + esc(D.period.short) + '</span><span class="kpi-line">' + ICON.gauge + delta(B.fleet.cap, K ? K.fleet.cap : undefined, { unit: "%", dp: 0, diff: true }) + ' capacity</span><span class="kpi-line">' + ICON.bolt + delta(B.fleet.prod, K ? K.fleet.prod : undefined, { dp: 2, diff: true }) + ' jobs/day</span><span class="kpi-line">' + ICON.users + delta(B.fleet.spread, K ? K.fleet.spread : undefined, { dp: 2, lowerIsBetter: true }) + " jobs/day spread</span></th>" + dayHead + "</tr>";
      var trows = D.techs.filter(function (t) { return (!ft.length || ft.indexOf(t.id) >= 0) && (!fz.length || t.zones.some(function (z) { return fz.indexOf(z) >= 0; }) || techZones(list, t.id).some(function (e) { return fz.indexOf(e.zone) >= 0; })) && (!S.changesOnly || !S.ran || techChanged(list, t.id) || techFlag(list, t.id)); });
      trows.forEach(function (t) {
        var tb = B.techs[t.id], tk = K ? K.techs[t.id] : null, tf = techFlag(list, t.id), tf0 = techFlag([], t.id), sel = S.sel[S.view === "cur" ? "cur" : "opt"], isSel = sel && sel.kind === "tech" && sel.id === t.id, isFocus = fc && fc.id !== "packing" && fc.techs.indexOf(t.id) >= 0;
        var first = '<td class="first"><div class="row-name">' + esc(t.id) + ' <span class="chip chip--skill' + (t.skill === "Specialist" ? " chip--specialist" : "") + '">' + esc(t.skill) + '</span></div><div class="row-kpi">' + ICON.gauge + "<span>" + delta(tb.cap, tk ? tk.cap : undefined, { unit: "%", dp: 0, diff: true }) + ' capacity</span></div><div class="row-kpi">' + ICON.bolt + "<span>" + delta(tb.prod, tk ? tk.prod : undefined, { dp: 2, diff: true }) + ' jobs/day</span></div><div class="row-zones">' + t.zones.map(function (z) { return '<span><i class="zdot" style="background:' + ZI[z].color + '"></i>' + esc(ZI[z].label) + "</span>"; }).join("") + "</div>" + (tf ? '<div class="row-flag bad">' + ICON.warn + esc(tf.title) + " · " + esc(fmtShort(tf.date)) + "</div>" : (S.ran && tf0 ? '<div class="row-flag">' + ICON.check + "Capacity fixed on " + esc(fmtShort(tf0.date)) + "</div>" : "")) + "</td>";
        var cells = wk.map(function (d) {
          if (!d.working) return '<td class="nonwork"></td>';
          var ab = A.absent[t.id][d.d]; if (ab) return '<td class="absent">ABSENT<small>' + esc(ab) + "</small></td>";
          var cl = (A.byTech[t.id][d.d] || []).filter(function (e) { return !fz.length || fz.indexOf(e.zone) >= 0 || e.kind === "off"; }), chg = S.ran && techCellChanged(list, t.id, d.d);
          return "<td" + (chg ? ' class="is-changed"' : "") + '><div class="cell-pills">' + cl.map(function (e) { return pill(ZI[e.zone].label, e.kind, e.kind === "pinned" ? "3 fixed" : e.kind === "temp" && e.partial ? "part" : "", true); }).join("") + "</div></td>";
        }).join("");
        body += '<tr class="clickable' + (isSel ? " is-selected" : "") + (tf ? " is-flag" : "") + (isFocus ? " is-focus" : "") + '" data-tech="' + t.id + '">' + first + cells + "</tr>";
      });
      if (!trows.length) body = '<tr><td colspan="' + (wk.length + 1) + '" class="empty-plan">No technician matches the filters.</td></tr>';
    }
    $("#grid thead").innerHTML = head; $("#grid tbody").innerHTML = body;
    tour.reposition();
  }
  $("#grid").addEventListener("click", function (e) {
    var t;
    if ((t = e.target.closest("[data-decide]"))) { decide(t.dataset.zone, t.dataset.decide); return; }
    if ((t = e.target.closest("[data-comment]"))) { openComment({ kind: "zone", id: t.dataset.comment }); return; }
    if ((t = e.target.closest("tr[data-zone]"))) { selectZone(S.view === "cur" ? "cur" : "opt", t.dataset.zone); return; }
    if ((t = e.target.closest("tr[data-tech]"))) { selectTech(S.view === "cur" ? "cur" : "opt", t.dataset.tech); }
  });
  $("#view-seg").addEventListener("click", function (e) { var b = e.target.closest("[data-view]"); if (b) setSched(b.dataset.view); });
  function setSched(v) { S.sched = v; $$("#view-seg button").forEach(function (b) { b.classList.toggle("is-active", b.dataset.view === v); }); renderSchedule(); tour.after(v === "tech" ? "techview" : "zoneview"); }
  $("#week-prev").addEventListener("click", function () { if (S.week > 1) { S.week--; renderSchedule(); } });
  $("#week-next").addEventListener("click", function () { if (S.week < D.weeks.length) { S.week++; renderSchedule(); } });
  $("#plan-seg").addEventListener("click", function (e) { var b = e.target.closest("[data-plan]"); if (b) setView(b.dataset.plan); });
  function setView(v) { S.view = v; if (v === "compare" && S.sel.opt && !S.sel.cur) S.sel.cur = S.sel.opt; $$("#plan-seg button").forEach(function (b) { b.classList.toggle("is-active", b.dataset.plan === v); }); renderMaps(); renderSchedule(); tour.after(v === "compare" ? "compare" : ""); }

  /* ---------------- decisions + notes ---------------- */
  function decide(zid, status) {
    var dec = S.decisions[zid], z = ZI[zid];
    dec.status = status;
    if (status !== "pending") log((status === "accepted" ? "Accepted" : "Rejected") + " the allocation for " + z.label, "Plan " + planLabel() + " · " + USER, status === "accepted" ? "ok" : "warn");
    renderSchedule(); renderPlanState(); renderChanges();
  }
  function acceptRemaining() {
    var n = 0, skipped = [];
    D.zones.forEach(function (z) { var d = S.decisions[z.id]; if (d.status === "pending" || d.status === "reproposed") { if (zoneFlag(S.applied, z.id)) skipped.push(z); else { d.status = "accepted"; n++; } } });
    log("Accepted " + n + " remaining zone allocations", "Accept remaining · " + USER, "ok");
    toast("Accepted " + n + " zones." + (skipped.length ? " " + skipped.map(function (z) { return z.label; }).join(", ") + (skipped.length === 1 ? " is" : " are") + " flagged and still need" + (skipped.length === 1 ? "s" : "") + " your decision — Accept remaining never touches a flag." : " Every zone is decided — the plan is ready to export."), 5200);
    renderSchedule(); renderPlanState();
    tour.after("accept-all");
  }
  $("#btn-accept-remaining").addEventListener("click", acceptRemaining);
  var commentTarget = null;
  function openComment(target) {
    commentTarget = target;
    var label = target.kind === "change" ? CI[target.id].title : ZI[target.id].label;
    $("#comment-title").textContent = "Note — " + label;
    var existing = target.kind === "change" ? S.notes[target.id] : S.decisions[target.id].comment;
    var ta = $("#comment-text"); ta.value = existing || (tour.active && (target.id === "marsh-move" || target.id === "HV-09") ? D.suggestedComment : ""); $("#comment-count").textContent = ta.value.length + "/300";
    $("#comment").hidden = false; setTimeout(function () { ta.focus(); }, 50);
    tour.after(target.kind === "change" && target.id === "marsh-move" ? "note" : "");
  }
  $("#comment-text").addEventListener("input", function (e) { $("#comment-count").textContent = e.target.value.length + "/300"; });
  function saveComment() {
    if (!commentTarget) return;
    var v = $("#comment-text").value.trim(), tg = commentTarget;
    if (tg.kind === "change") S.notes[tg.id] = v; else S.decisions[tg.id].comment = v;
    $("#comment").hidden = true;
    if (v) log("Note on " + (tg.kind === "change" ? CI[tg.id].title : ZI[tg.id].label), "“" + v + "” · " + USER, "");
    renderSchedule(); renderChanges();
    commentTarget = null;
    tour.after(tg.kind === "change" && tg.id === "marsh-move" ? "save" : "");
  }
  $("#comment-save").addEventListener("click", saveComment);
  $("#comment-cancel").addEventListener("click", function () { $("#comment").hidden = true; commentTarget = null; });
  $("#comment-close").addEventListener("click", function () { $("#comment").hidden = true; commentTarget = null; });

  /* ---------------- run + re-run ---------------- */
  var runModal = $("#run"), runForm = $("#run-form"), runProg = $("#run-progress");
  function openRun() {
    runForm.hidden = false; runProg.hidden = true; $("#run-title").textContent = "Run optimization";
    var sel = $("#run-region"); sel.innerHTML = [D.region.name].concat(D.region.others).map(function (r) { return "<option>" + esc(r) + "</option>"; }).join("");
    $("#sources").innerHTML = "<span>Sources</span>" + D.sources.map(function (s) { return '<span class="chip ' + (s.ok ? "chip--ok" : "chip--muted") + '">' + esc(s.name) + " · " + esc(s.state) + "</span>"; }).join("");
    setRunFile(S.runFile);
    runModal.hidden = false;
    tour.after("run");
  }
  function setRunFile(f) {
    S.runFile = f; var fb = $("#run-file");
    fb.classList.toggle("is-set", !!f);
    $(".fb-text", fb).innerHTML = f ? "<strong>" + esc(f.name) + "</strong><em>" + esc(f.kind) + " · " + esc(f.size) + " · sheets " + D.inputSheets.join(", ") + "</em>" : "<strong>Click to upload</strong><em>XLSX only · sheets: " + D.inputSheets.join(", ") + "</em>";
    $("#run-go").disabled = !f;
  }
  $("#btn-run").addEventListener("click", openRun);
  $("#run-close").addEventListener("click", function () { if (!S.busy) runModal.hidden = true; });
  $("#run-example").addEventListener("click", function (e) { e.preventDefault(); toast("<b>example-input.xlsx</b> downloaded · the seven sheets the optimizer expects, with two rows each"); });
  $("#run-region").addEventListener("change", function (e) { if (e.target.value !== D.region.name) { toast("Only " + D.region.name + " is loaded in this walkthrough — the other regions run on their own rule sets."); e.target.value = D.region.name; } });
  $("#run-file").addEventListener("click", function () { openPicker(); tour.after("file"); });

  var picker = $("#picker"), pickerList = $("#picker-list"), pickerOpen = $("#picker-open");
  function openPicker() {
    S.pickedFile = null; pickerOpen.disabled = true;
    pickerList.innerHTML = D.pickerFiles.map(function (f, i) { return '<li data-file="' + i + '"' + (f.main ? ' class="is-main"' : "") + '><span class="file-ico"><svg viewBox="0 0 24 24"><path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5"/></svg></span><div class="doc-name"><strong>' + esc(f.name) + "</strong><span>" + esc(f.kind) + '</span></div><span class="size">' + esc(f.size) + "</span></li>"; }).join("");
    picker.hidden = false;
  }
  function selectFile(i) {
    S.pickedFile = D.pickerFiles[i];
    $$("li", pickerList).forEach(function (li) { li.classList.toggle("is-selected", +li.dataset.file === i); });
    pickerOpen.disabled = false;
    if (S.pickedFile.main) tour.after("pick");
  }
  function openFile() {
    if (!S.pickedFile) return;
    if (!S.pickedFile.main) { toast("This walkthrough follows one prepared period — pick the Harborview file for 5 Oct."); return; }
    picker.hidden = true; setRunFile(S.pickedFile);
    tour.after("open");
  }
  pickerList.addEventListener("click", function (e) { var li = e.target.closest("li[data-file]"); if (li) selectFile(+li.dataset.file); });
  $("#picker-cancel").addEventListener("click", function () { picker.hidden = true; });
  pickerOpen.addEventListener("click", openFile);

  function runStages(list, onDone) {
    var bar = $("#proc-bar"), ol = $("#stages");
    ol.innerHTML = list.map(function (s) { return "<li><i></i><span>" + esc(s.name) + "</span><em></em></li>"; }).join("");
    var lis = $$("li", ol); bar.style.width = "0%"; $("#proc-chip").textContent = "Processing"; $("#proc-chip").className = "chip chip--live";
    var t = 0, sum = list.reduce(function (a, p) { return a + p.ms; }, 0), acc = 0;
    list.forEach(function (p, i) {
      setTimeout(function () { lis[i].classList.add("is-running"); if (p.tick) tickSolve(lis[i], p.ms); }, t);
      acc += p.ms; t += p.ms;
      (function (i, pc, p) { setTimeout(function () { lis[i].classList.remove("is-running"); lis[i].classList.add("is-done"); if (p.warn) { lis[i].classList.add("has-warn"); warnToast(D.uploadWarning); } $("em", lis[i]).textContent = p.done; bar.style.width = pc + "%"; }, t); })(i, Math.round(acc / sum * 100), p);
    });
    setTimeout(function () { $("#proc-chip").textContent = "Done"; $("#proc-chip").className = "chip chip--ok"; }, t);
    setTimeout(onDone, t + 600);
  }
  function tickSolve(li, ms) { var em = $("em", li), n = 0, steps = 10, iv = setInterval(function () { n++; em.textContent = "iteration " + (n * 40) + " · objective " + (0.62 + n * 0.031).toFixed(2); if (n >= steps) clearInterval(iv); }, ms / steps); }
  function applyPlan(version) {
    S.ran = true; S.version = version; S.applied = D.plans[version].slice(); S.undone = []; S.notes = {}; resetDecisions(); S.exported = false; S.sent = false; S.sel = { cur: null, opt: null }; S.focus = null; S.changesOnly = false; S.week = 1;
  }
  function startProcessing() {
    if (!S.runFile || S.busy) return;
    S.busy = true; runForm.hidden = true; runProg.hidden = false;
    $("#proc-file").textContent = S.runFile.name; $("#proc-sub").textContent = D.region.name + " · " + D.period.label; $("#proc-note").hidden = false;
    runStages(D.stages, function () {
      S.busy = false; applyPlan("v1"); S.view = "opt";
      $$("#plan-seg button").forEach(function (b) { b.classList.toggle("is-active", b.dataset.plan === "opt"); });
      var K = kpis(S.applied), B = kpis([]);
      log("Plan v1 optimized: " + D.region.name + ", " + D.period.label, D.zones.length + " zones · " + D.techs.length + " technicians · " + K.fleet.jobs.toLocaleString("en-US") + " visits placed · " + S.applied.length + " changes · " + flagsFor(S.applied).length + " flags", "");
      log("Input validated: " + S.runFile.name, "7 sheets · 1 warning (home location missing for 2 technicians)", "warn");
      runModal.hidden = true; hideWarn();
      renderAll();
      toast("<b>Plan v1 is ready.</b> " + signed(pct(B.fleet.prodRaw, K.fleet.prodRaw), 1, "%") + " jobs per technician per day · " + S.applied.length + " changes in " + changedZones(S.applied).length + " zones · " + flagsFor(S.applied).length + " flags to look at.", 5200);
      tour.next();
    });
  }
  $("#run-go").addEventListener("click", function () { startProcessing(); tour.after("optimize"); });
  function reoptimize() {
    if (S.busy) return;
    if (!canReopt()) { toast("Nothing to re-plan yet — undo a change or reject a zone first, then re-optimize around it."); return; }
    S.busy = true; $("#run-title").textContent = "Re-optimize with feedback"; runForm.hidden = true; runProg.hidden = false; $("#proc-note").hidden = true;
    var notes = Object.keys(S.notes).filter(function (k) { return S.notes[k]; }).length;
    $("#proc-file").textContent = "Plan " + planLabel() + " + your fixes and notes"; $("#proc-sub").textContent = S.undone.length + " manual fix" + (S.undone.length === 1 ? "" : "es") + " · " + notes + " note" + (notes === 1 ? "" : "s") + " · minimal disruption on";
    runModal.hidden = false;
    var before = kpis(S.applied);
    runStages(D.reoptStages, function () {
      S.busy = false; S.version = "v2";
      S.applied = S.applied.filter(function (x) { return x !== "marsh-move"; }); if (S.undone.indexOf("marsh-move") < 0) S.undone.push("marsh-move");
      if (!on("marsh-keep")) S.applied.push("marsh-keep");
      ["HV-09", "HV-10"].forEach(function (z) { S.decisions[z].status = "reproposed"; });
      var after = kpis(S.applied);
      log("Plan v2 re-optimized around your fixes", "HV-09 Marsh End keeps its Wednesday coverage · HV-10 Southbank overflow → T-1053 · 2 zones re-proposed · " + USER, "ok");
      runModal.hidden = true; S.sel = { cur: null, opt: null }; S.focus = "marsh-keep";
      renderAll();
      toast("<b>Plan v2.</b> Marsh End keeps its technician (wait " + after.zones["HV-09"].wait.toFixed(1) + " d) and Southbank's overflow goes to T-1053 (wait " + before.zones["HV-10"].wait.toFixed(1) + " → " + after.zones["HV-10"].wait.toFixed(1) + " d). Fleet " + before.fleet.prod.toFixed(2) + " → " + after.fleet.prod.toFixed(2) + " jobs/day · two zones re-proposed for your decision.", 6500);
      tour.next();
    });
  }

  /* ---------------- export ---------------- */
  function exportRows(list) {
    var rows = [];
    D.techs.forEach(function (t) {
      techZones(list, t.id).forEach(function (e) {
        if (e.kind === "off") return;
        var dows = { Mon: 0, Tue: 0, Wed: 0, Thu: 0, Fri: 0, Sat: 0, Sun: 0 };
        e.dates.forEach(function (k) { dows[dayOf(k).dow] = 1; });
        var dec = S.decisions[e.zone];
        rows.push([t.id, "", e.zone, D.period.start, D.period.end, "100", "weekly", "1", e.kind === "default" || e.kind === "pinned" || e.kind === "backfill" ? "regular" : "temporary", dows.Mon, dows.Tue, dows.Wed, dows.Thu, dows.Fri, dows.Sat, dows.Sun, dec.status === "accepted" ? "Accepted" : dec.status === "rejected" ? "Rejected" : "Not decided", dec.comment || ""]);
      });
    });
    return rows;
  }
  function openExport() {
    if (!S.ran) { toast("Run the optimization first — the export carries the optimized plan and your decisions."); return; }
    var rows = exportRows(S.applied), acc = D.zones.filter(function (z) { return S.decisions[z.id].status === "accepted"; }).length, rej = D.zones.filter(function (z) { return S.decisions[z.id].status === "rejected"; }).length;
    $("#export-meta").innerHTML = '<span class="chip chip--muted">Template: work-zone assignment import v2</span><span class="chip chip--muted">Plan ' + esc(planLabel()) + '</span><span class="chip chip--muted">' + esc(D.period.label) + '</span><span class="chip ' + (acc === D.zones.length ? "chip--ok" : "chip--warn") + '">' + acc + " accepted · " + rej + " rejected · " + (D.zones.length - acc - rej) + " pending</span>";
    $("#export-table thead").innerHTML = "<tr>" + D.exportColumns.map(function (c) { return "<th>" + esc(c) + "</th>"; }).join("") + "</tr>";
    $("#export-table tbody").innerHTML = rows.slice(0, 16).map(function (r) { return "<tr>" + r.map(function (c, i) { return "<td" + (i >= 9 && i <= 15 ? ' class="num"' : "") + ">" + esc(c) + "</td>"; }).join("") + "</tr>"; }).join("") + (rows.length > 16 ? '<tr><td colspan="' + D.exportColumns.length + '" class="muted">… ' + (rows.length - 16) + " more rows</td></tr>" : "");
    $("#export-count").textContent = rows.length + " rows · " + D.techs.length + " technicians · " + D.zones.length + " zones · decisions and notes included";
    $("#export").hidden = false;
    tour.after("download");
  }
  $("#btn-download").addEventListener("click", openExport);
  $("#export-close").addEventListener("click", function () { $("#export").hidden = true; });
  $("#export-download").addEventListener("click", function () {
    var rows = exportRows(S.applied), file = "work-zone-assignment_harborview_" + D.period.start + "_" + planLabel().replace(/[^a-z0-9]+/gi, "-") + ".xlsx";
    S.exported = true; log("Exported the plan", file + " · " + rows.length + " rows · " + USER, "ok");
    $("#export").hidden = true;
    toast(ICON.check + "<span><b>" + esc(file) + "</b> downloaded · " + rows.length + " rows in the field-service import format, with every decision and note</span>", 4600);
    tour.after("export-dl");
  });
  $("#export-send").addEventListener("click", function () {
    var acc = D.zones.filter(function (z) { return S.decisions[z.id].status === "accepted"; }).length;
    if (!acc) { toast("Nothing accepted yet — accept zone allocations first; only accepted zones are written back."); return; }
    S.sent = true; log("Sent " + acc + " accepted zone allocations to the field-service system", "Connector: field-service system · rejected and pending zones stay on the current plan · " + USER, "ok");
    $("#export").hidden = true;
    toast(ICON.check + "<span>Queued for the field-service system · <b>" + acc + " accepted zone allocations</b> · rejected and pending zones stay on the current plan</span>", 4600);
  });

  /* ---------------- filters ---------------- */
  function renderFilters() {
    var fz = S.filters.zones, ft = S.filters.techs;
    $("#filter-zone .select-label").textContent = fz.length ? fz.length + " selected" : "All zones";
    $("#filter-tech .select-label").textContent = ft.length ? ft.length + " selected" : "All technicians";
    $("#filter-zone .chips-sel").innerHTML = fz.map(function (z) { return '<span class="chip chip--muted">' + esc(ZI[z].label) + '<button type="button" data-unsel="zone" data-id="' + z + '" aria-label="Remove">×</button></span>'; }).join("");
    $("#filter-tech .chips-sel").innerHTML = ft.map(function (t) { return '<span class="chip chip--muted">' + esc(t) + '<button type="button" data-unsel="tech" data-id="' + t + '" aria-label="Remove">×</button></span>'; }).join("");
  }
  function ddList(kind) {
    var wrap = $("#filter-" + kind), q = ($("input", wrap).value || "").toLowerCase(), sel = S.filters[kind === "zone" ? "zones" : "techs"];
    var items = kind === "zone" ? D.zones.map(function (z) { return { id: z.id, label: z.label, color: z.color }; }) : D.techs.map(function (t) { return { id: t.id, label: t.id + " · " + t.skill }; });
    var shown = items.filter(function (i) { return !q || i.label.toLowerCase().indexOf(q) >= 0; });
    $(".dd-list", wrap).innerHTML = '<li class="dd-all' + (sel.length === items.length ? " is-on" : sel.length ? " is-some" : "") + '" data-all="1"><i></i>Select all</li>' + shown.map(function (i) { return '<li data-id="' + i.id + '"' + (sel.indexOf(i.id) >= 0 ? ' class="is-on"' : "") + "><i></i>" + (i.color ? '<span class="zdot" style="background:' + i.color + '"></span>' : "") + esc(i.label) + "</li>"; }).join("");
  }
  $$(".filter").forEach(function (wrap) {
    var kind = wrap.id === "filter-zone" ? "zone" : "tech", btn = $(".select", wrap), dd = $(".dropdown", wrap);
    btn.addEventListener("click", function () { var open = dd.hidden; $$(".dropdown").forEach(function (d) { d.hidden = true; }); $$(".select").forEach(function (s) { s.classList.remove("is-open"); }); if (open) { ddList(kind); dd.hidden = false; btn.classList.add("is-open"); } });
    $("input", wrap).addEventListener("input", function () { ddList(kind); });
    $(".dd-list", wrap).addEventListener("click", function (e) {
      var li = e.target.closest("li"); if (!li) return;
      var key = kind === "zone" ? "zones" : "techs", all = kind === "zone" ? D.zones.map(function (z) { return z.id; }) : D.techs.map(function (t) { return t.id; });
      if (li.dataset.all) S.filters[key] = S.filters[key].length === all.length ? [] : all.slice();
      else { var i = S.filters[key].indexOf(li.dataset.id); if (i >= 0) S.filters[key].splice(i, 1); else S.filters[key].push(li.dataset.id); }
      ddList(kind); renderFilters(); renderMaps(); renderSchedule();
    });
    wrap.addEventListener("click", function (e) { var b = e.target.closest("[data-unsel]"); if (!b) return; var key = b.dataset.unsel === "zone" ? "zones" : "techs"; S.filters[key] = S.filters[key].filter(function (x) { return x !== b.dataset.id; }); renderFilters(); renderMaps(); renderSchedule(); });
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".filter")) { $$(".dropdown").forEach(function (d) { d.hidden = true; }); $$(".select").forEach(function (s) { s.classList.remove("is-open"); }); } });
  $("#btn-filters").addEventListener("click", function () { var f = $("#filters"); f.hidden = !f.hidden; $("#btn-filters").setAttribute("aria-expanded", String(!f.hidden)); tour.reposition(); });
  $("#btn-reset").addEventListener("click", function () { S.filters = { zones: [], techs: [] }; S.sel = { cur: null, opt: null }; S.week = 1; S.changesOnly = false; S.focus = null; setView("opt"); setSched("zone"); renderFilters(); renderChanges(); toast("Filters, selection and views reset — the plan, your fixes and your decisions are kept."); });

  /* ---------------- drawers: runs, settings ---------------- */
  function timeline(items) { return '<ol class="timeline">' + items.map(function (h) { return "<li" + (h.kind ? ' class="' + h.kind + '"' : "") + "><time>" + esc(h.time) + "</time><i></i><div><strong>" + esc(h.text) + "</strong><span>" + esc(h.sub) + "</span></div></li>"; }).join("") + "</ol>"; }
  function openDrawer(panel) {
    var body = "";
    if (panel === "runs") {
      $("#drawer-eyebrow").textContent = "Runs and history"; $("#drawer-title").textContent = D.region.name;
      body = timeline(S.history.concat(D.priorHistory));
    } else {
      var st = D.settings;
      $("#drawer-eyebrow").textContent = "Optimization settings"; $("#drawer-title").textContent = D.region.name + " · rule set";
      body = '<div class="set-block"><h3>Planning</h3><dl class="set-kv"><dt>Mode</dt><dd>' + esc(st.mode) + "</dd><dt>Horizon</dt><dd>" + esc(st.horizon) + "</dd><dt>Capacity</dt><dd>" + esc(st.capacity) + '</dd><dt>Disruption</dt><dd><span class="toggle"><i></i>Minimal disruption of the current allocation</span></dd></dl></div>';
      body += '<div class="set-block"><h3>Objectives and weights</h3>' + st.objectives.map(function (o) { return '<div class="obj"><span><b>' + esc(o.name) + "</b><em>" + esc(o.desc) + '</em></span><i><b style="width:' + o.weight + '%"></b></i><span class="w">' + o.weight + "</span></div>"; }).join("") + "</div>";
      body += '<div class="set-block"><h3>Rules and guardrails</h3><ul class="rules">' + st.rules.map(function (r) { return "<li><b>" + esc(r.name) + '</b><span class="chip ' + (r.type === "Hard" ? "chip--bad" : "chip--muted") + '">' + esc(r.type) + "</span><span>" + esc(r.desc) + "</span></li>"; }).join("") + "</ul></div>";
      body += '<div class="set-block"><h3>Regions</h3><ul class="set-list">' + st.regions.map(function (r) { return "<li><b>" + esc(r.name) + "</b><span>" + esc(r.state) + " · " + r.zones + " zones · " + r.techs + " technicians</span></li>"; }).join("") + "</ul></div>";
      body += '<div class="set-block"><h3>Connectors</h3><ul class="set-list">' + st.connectors.map(function (c) { return "<li><b>" + esc(c.name) + '</b><span class="chip ' + (c.state === "Connected" ? "chip--ok" : "chip--muted") + '">' + esc(c.state) + "</span><span>" + esc(c.dir) + "</span></li>"; }).join("") + "</ul></div>";
      body += '<p class="muted" style="font-size:12px">Read-only in this walkthrough. Rule sets, weights and connectors are configured per region during roll-out.</p>';
    }
    $("#drawer-body").innerHTML = body; $("#drawer").hidden = false;
    $$(".rail-item").forEach(function (b) { b.classList.toggle("is-active", b.dataset.panel === panel); });
  }
  function closeDrawer() { $("#drawer").hidden = true; $$(".rail-item").forEach(function (b) { b.classList.toggle("is-active", b.dataset.panel === "dashboard"); }); }
  $$(".rail-item").forEach(function (b) { b.addEventListener("click", function () { if (b.dataset.panel === "dashboard") closeDrawer(); else openDrawer(b.dataset.panel); }); });
  $("#drawer-close").addEventListener("click", closeDrawer);
  $("#drawer").addEventListener("click", function (e) { if (e.target === $("#drawer")) closeDrawer(); });

  /* ---------------- toasts ---------------- */
  var toastT;
  function toast(html, ms) {
    var t = $("#toast"); t.innerHTML = /^<(svg|span)/.test(html) ? html : "<span>" + html + "</span>"; t.hidden = false;
    clearTimeout(toastT); toastT = setTimeout(function () { t.hidden = true; }, ms || 3400);
  }
  var warnT;
  function warnToast(w) { var t = $("#warn-toast"); t.innerHTML = "<strong>" + ICON.warn + esc(w.title) + "</strong>" + esc(w.text) + '<button class="icon-btn" type="button" aria-label="Dismiss" data-dismiss-warn>' + ICON.x + "</button>"; t.hidden = false; clearTimeout(warnT); warnT = setTimeout(hideWarn, 9000); }
  function hideWarn() { $("#warn-toast").hidden = true; }
  $("#warn-toast").addEventListener("click", function (e) { if (e.target.closest("[data-dismiss-warn]")) hideWarn(); });

  function renderAll() { renderPlanState(); renderKpiBand(); renderFilters(); renderMaps(); renderChanges(); renderSchedule(); }

  /* ---------------- tour ---------------- */
  var STEPS = [
    { id: "run", major: 1, side: "bottom", title: "Run the optimization", body: "The dashboard shows today's allocation from the field-service system, with its open problems flagged. Click Run optimization to plan the next four weeks.", target: function () { return $("#btn-run"); }, auto: openRun },
    { id: "file", major: 1, side: "right", title: "Attach the period's file", body: "Region and period are set. The technicians, skills, calendars, zones and booked visits come in one XLSX — click the file field and choose the prepared one. Nothing is really uploaded.", target: function () { return $("#run-file"); }, anchor: function () { return $("#run-file"); }, auto: function () { openPicker(); } },
    { id: "pick", major: 1, side: "right", title: "Choose the Harborview file", body: "Pick the highlighted file.", target: function () { return $("#picker-list li.is-main"); }, auto: function () { selectFile(0); } },
    { id: "open", major: 1, side: "top", title: "Open it", body: "The file is attached to the run.", target: function () { return $("#picker-open"); }, auto: openFile },
    { id: "optimize", major: 1, side: "top", title: "Optimize", body: "The input is validated, the travel matrix and the rules are loaded, the GPU solver places every visit, and the KPIs are computed before and after — watch the stages.", target: function () { return $("#run-go"); }, auto: startProcessing },
    { id: "kpis", major: 2, side: "bottom", passive: true, title: "Review the improved metrics", body: "This is the result of the run, before you touch anything: every KPI is computed the same way for today's allocation and the proposal, over the same four weeks — jobs per technician per day, capacity used, average wait from booking to visit, and visits placed in the period. Read the four deltas, then continue.", target: function () { return $(".kpi-tiles"); }, anchor: function () { return $(".kpi-tile"); }, auto: function () { tour.next(); } },
    { id: "review", major: 2, side: "bottom", title: "See where the gain comes from", body: "Click Review changes: the list beside the map holds every change the solver made, each with the rule that produced it and its effect on these numbers.", target: function () { return $("#btn-review-changes"); }, anchor: function () { return $(".kpi-tile--changes"); }, auto: reviewChanges },
    { id: "change-vacation", major: 3, side: "left", title: "Drill into a change", body: "Each row is one change, with the rule that produced it and its effect on the KPIs. Click the Eastfield row: the map opens the zone and the schedule jumps to the week of the vacation.", target: function () { return $('#changes [data-change="vacation"] .chg-main'); }, auto: function () { openChange("vacation"); } },
    { id: "compare", major: 3, side: "bottom", title: "Compare with today's plan", body: "Details show who covers the zone now and why. Switch to Compare: current on the left, optimized on the right — Eastfield had no technician for five days, now two neighbours split it.", target: function () { return $('#plan-seg [data-plan="compare"]'); }, auto: function () { setView("compare"); } },
    { id: "techview", major: 4, side: "top", title: "Check the numbers per technician", body: "Capacity and jobs per day per technician, before and after, with every changed day tinted. Switch the schedule to Technician view.", target: function () { return $('#view-seg [data-view="tech"]'); }, auto: function () { setSched("tech"); } },
    { id: "tech-row", major: 4, side: "top", title: "Open an over-capacity day", body: "T-1048 had 8 visits on one day against a capacity of 7. Click the row — the details on the map explain how the plan fixed it.", target: function () { return $('#grid tr[data-tech="T-1048"]'); }, auto: function () { selectTech("opt", "T-1048"); } },
    { id: "undo", major: 5, side: "left", title: "Fix what the solver got wrong", body: "One change made a zone worse: Marsh End's wait rose 1.3 days because its technician was moved to Southbank on Wednesdays. Click Undo — the KPIs update at once.", target: function () { return $('#changes [data-change="marsh-move"] [data-undo]'); }, anchor: function () { return $('#changes [data-change="marsh-move"]'); }, auto: function () { undoChange("marsh-move"); } },
    { id: "note", major: 5, side: "left", title: "Tell the solver why", body: "Your fix is applied, but Southbank is back over its Wednesday capacity. Leave a note — it travels with the fix into the next run and the export.", target: function () { return $('#changes [data-change="marsh-move"] [data-note]'); }, anchor: function () { return $('#changes [data-change="marsh-move"]'); }, auto: function () { openComment({ kind: "change", id: "marsh-move" }); } },
    { id: "save", major: 5, side: "top", title: "Save the note", body: "The note is drafted for you. Save it.", target: function () { return $("#comment-save"); }, anchor: function () { return $("#comment-save"); }, auto: saveComment },
    { id: "reopt", major: 5, side: "left", title: "Re-optimize around your fix", body: "The solver re-plans with your fix as a constraint and minimal disruption to the ten zones you did not touch.", target: function () { return $("#btn-reopt"); }, auto: reoptimize },
    { id: "accept-all", major: 6, side: "bottom", title: "Accept everything else", body: "Plan v2 keeps Marsh End covered and sends Southbank's overflow to a neighbour. Accept remaining takes every pending zone that carries no flag — a flagged zone always waits for a person.", target: function () { return $("#btn-accept-remaining"); }, auto: acceptRemaining },
    { id: "download", major: 6, side: "bottom", title: "Export the plan", body: "Click Download to see the work-zone assignment file in the field-service system's import format.", target: function () { return $("#btn-download"); }, auto: openExport },
    { id: "export-dl", major: 6, side: "top", title: "Download the file", body: "One row per technician and zone, the weekdays it applies to, and every decision and note. The same rows can be sent to the connected field-service system directly.", target: function () { return $("#export-download"); }, anchor: function () { return $("#export-download"); }, auto: function () { $("#export-download").click(); } }
  ];
  var MAJORS = 6;
  var tour = {
    active: false, i: 0, el: $("#tour"), target: null, tries: 0,
    start: function () { this.active = true; this.i = 0; document.body.classList.add("tour-on"); $("#tour-pill").hidden = false; $("#tour-toggle").textContent = "Exit guide"; this.show(); },
    show: function () {
      var st = STEPS[this.i], self = this, t = st.target();
      if (!t) { if (this.tries++ < 60) return void requestAnimationFrame(function () { self.show(); }); return; }
      this.tries = 0;
      if (this.target) this.target.classList.remove("tour-target");
      this.target = t; t.classList.add("tour-target");
      $("#tour-step").textContent = "Step " + st.major + " of " + MAJORS;
      $("#tour-title").textContent = st.title; $("#tour-body").textContent = st.body;
      var bars = ""; for (var k = 1; k <= MAJORS; k++) bars += '<i class="' + (k <= st.major ? "is-done" : "") + '"></i>';
      $("#tour-progress").innerHTML = bars;
      /* a passive step asks for nothing on the page — Next is its way forward, so Skip makes no sense there */
      $("#tour-next").hidden = !st.passive; $("#tour-skip").hidden = !!st.passive;
      this.el.hidden = false; this.el.dataset.side = st.side;
      try { t.scrollIntoView({ block: "center", behavior: "smooth", inline: "nearest" }); } catch (e) {}
      this.reposition(); setTimeout(function () { self.reposition(); }, 350); setTimeout(function () { self.reposition(); }, 750);
    },
    after: function (id) { if (!this.active || !id) return; if (STEPS[this.i].id === id) this.next(); },
    next: function () {
      if (!this.active) return;
      var cur = STEPS[this.i].id;
      if ((cur === "optimize" || cur === "reopt") && S.busy) { this.el.hidden = true; if (this.target) { this.target.classList.remove("tour-target"); this.target = null; } return; }
      this.i++;
      if (this.i >= STEPS.length) return this.finish();
      var self = this; setTimeout(function () { self.show(); }, 260);
    },
    skip: function () { var st = STEPS[this.i]; if (st && st.auto) st.auto(); },
    exit: function () { this.active = false; this.el.hidden = true; if (this.target) this.target.classList.remove("tour-target"); this.target = null; document.body.classList.remove("tour-on"); $("#tour-pill").hidden = true; $("#tour-toggle").textContent = "Restart walkthrough"; },
    finish: function () {
      this.exit();
      var g = $("#gate");
      $("#gate-title").textContent = "That is the whole loop";
      $("#gate-body").innerHTML = "Four weeks planned in one run, the gain shown before → after and traced to the changes that produced it, one change undone by hand and re-planned around, and a dispatcher decided every zone that left. Still open for you: Stonebridge (HV-07) is allocated on last year's demand for three dates and waits for a decision; undo or restore any other change and watch the KPIs follow; Changes only narrows the map and the schedule to what moved; Filters, the Runs panel and Settings (rules, objectives, regions, connectors) are there too; and the export can be sent straight to the field-service system.<ol><li>Run the optimization on the period's data</li><li>See what improved, and by how much</li><li>Drill into each change and compare with today</li><li>Check the KPIs per technician</li><li>Undo what the solver got wrong, re-optimize around it</li><li>Accept and export to the field-service system</li></ol>";
      $("#gate-start").textContent = "Replay the walkthrough"; $("#gate-free").textContent = "Keep exploring";
      $("#gate-start").onclick = function () { location.href = location.pathname; };
      $("#gate-free").onclick = function () { g.hidden = true; };
      g.hidden = false;
    },
    reposition: function () {
      if (!this.active || !this.target || this.el.hidden) return;
      if (!document.body.contains(this.target)) { var t = STEPS[this.i].target(); if (t) { this.target.classList.remove("tour-target"); this.target = t; t.classList.add("tour-target"); } else return; }
      var anchor = (STEPS[this.i].anchor && STEPS[this.i].anchor()) || this.target;
      var r = anchor.getBoundingClientRect(), w = 300, h = this.el.offsetHeight || 150, gap = 16, s = STEPS[this.i].side, top, left;
      var fits = { right: r.right + gap + w < innerWidth, left: r.left - gap - w > 0, bottom: r.bottom + gap + h < innerHeight, top: r.top - gap - h > 0 };
      if (!fits[s]) s = ["right", "left", "bottom", "top"].filter(function (k) { return fits[k]; })[0] || "bottom";
      if (s === "right") { left = r.right + gap; top = r.top - 10; }
      if (s === "left") { left = r.left - gap - w; top = r.top - 10; }
      if (s === "bottom") { left = r.left; top = r.bottom + gap; }
      if (s === "top") { left = r.left; top = r.top - gap - h; }
      top = Math.max(8, Math.min(innerHeight - h - 8, top)); left = Math.max(8, Math.min(innerWidth - w - 8, left));
      this.el.style.top = top + "px"; this.el.style.left = left + "px"; this.el.dataset.side = s;
    },
    nudge: function () { var self = this; this.el.classList.remove("is-nudge"); void this.el.offsetWidth; this.el.classList.add("is-nudge"); setTimeout(function () { self.el.classList.remove("is-nudge"); }, 400); }
  };
  document.addEventListener("click", function (e) {
    if (!tour.active || !tour.target) return;
    if (e.target.closest("#tour, #tour-toggle, #gate, #warn-toast")) return;
    var el = e.target.closest("button, a, tr.clickable, .zone, .home, li[data-file], .dd-list li, .select, input, label, select, textarea, .d-item-head, .chg-main");
    /* a passive step asks for no click at all: the target is a container (the KPI grid), so its own
       children must NOT act either — everything outside the callout is blocked, Next is the way on */
    if (STEPS[tour.i] && STEPS[tour.i].passive) { e.preventDefault(); e.stopPropagation(); if (el) tour.nudge(); return; }
    if (!el) return;
    if (tour.target.contains(el) || el.contains(tour.target)) return;
    e.preventDefault(); e.stopPropagation(); tour.nudge();
  }, true);
  window.addEventListener("resize", function () { tour.reposition(); });
  document.addEventListener("scroll", function () { tour.reposition(); }, true);
  $("#tour-skip").addEventListener("click", function () { tour.skip(); });
  $("#tour-next").addEventListener("click", function () { tour.next(); });
  $("#tour-toggle").addEventListener("click", function () { if (tour.active) tour.exit(); else location.href = location.pathname; });

  /* ---------------- keyboard ---------------- */
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape" || tour.active) return;
    if (!picker.hidden) { picker.hidden = true; return; }
    if (!$("#comment").hidden) { $("#comment").hidden = true; return; }
    if (!$("#export").hidden) { $("#export").hidden = true; return; }
    if (!runModal.hidden && !S.busy) { runModal.hidden = true; return; }
    if (!$("#drawer").hidden) { closeDrawer(); return; }
    if (!$("#gate").hidden) { $("#gate").hidden = true; return; }
    if (S.sel.cur || S.sel.opt) { S.sel = { cur: null, opt: null }; renderMaps(); renderSchedule(); }
  });

  /* ---------------- boot ---------------- */
  function primeSolved(version, decided) {
    applyPlan("v1");
    log("Plan v1 optimized: " + D.region.name + ", " + D.period.label, D.zones.length + " zones · " + D.techs.length + " technicians · " + kpis(S.applied).fleet.jobs.toLocaleString("en-US") + " visits placed · " + S.applied.length + " changes · " + flagsFor(S.applied).length + " flags", "");
    if (version === "v2") { S.version = "v2"; S.applied = D.plans.v2.slice(); S.undone = ["marsh-move"]; S.notes["marsh-move"] = D.suggestedComment; S.decisions["HV-09"].status = "reproposed"; S.decisions["HV-10"].status = "reproposed"; log("Plan v2 re-optimized around your fixes", "HV-09 Marsh End keeps its Wednesday coverage · 2 zones re-proposed · " + USER, "ok"); }
    if (decided) D.zones.forEach(function (z) { if (!zoneFlag(S.applied, z.id)) S.decisions[z.id].status = "accepted"; });
  }
  if (params.get("ui") === "clean") { $("#tour-toggle").hidden = true; } /* screenshot mode: product UI only */
  var state = params.get("state");
  if (params.get("tour") === "off") {
    tour.exit(); $("#gate").hidden = true;
    if (state !== "start") primeSolved(state === "final" || state === "v2" ? "v2" : "v1", state === "final");
  } else {
    $("#gate").hidden = false;
    $("#gate-start").addEventListener("click", function () { $("#gate").hidden = true; tour.start(); });
    $("#gate-free").addEventListener("click", function () { $("#gate").hidden = true; tour.exit(); if (!S.ran) { primeSolved("v1", false); renderAll(); } });
  }
  if (params.get("view") === "tech") S.sched = "tech";
  if (params.get("plan")) S.view = params.get("plan");
  if (params.get("week")) S.week = Math.max(1, Math.min(D.weeks.length, +params.get("week") || 1));
  $$("#view-seg button").forEach(function (b) { b.classList.toggle("is-active", b.dataset.view === S.sched); });
  $$("#plan-seg button").forEach(function (b) { b.classList.toggle("is-active", b.dataset.plan === S.view); });
  if (params.get("filters") === "open") { $("#filters").hidden = false; $("#btn-filters").setAttribute("aria-expanded", "true"); }
  renderAll();
  if (params.get("focus") && CI[params.get("focus")] && S.ran) openChange(params.get("focus"));
  window.DEMO = { state: S, tour: tour, selectZone: selectZone, selectTech: selectTech, setView: setView, setSched: setSched, kpis: kpis, alloc: alloc, openRun: openRun, openExport: openExport, openDrawer: openDrawer, openChange: openChange, undoChange: undoChange, restoreChange: restoreChange, reoptimize: reoptimize };
})();
