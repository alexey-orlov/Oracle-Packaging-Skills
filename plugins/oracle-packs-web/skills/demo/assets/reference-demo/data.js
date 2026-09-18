/* Demo data — a fictional coastal metro ("Harborview"), twelve work zones,
   eighteen technicians, one four-week planning period, the uploaded current
   allocation, the optimized plan and the plan re-run after dispatcher
   feedback. Everything here is synthetic: invented districts and postcodes,
   synthetic technician ids, deltas inside the band the product is cleared to
   claim. The map is a schematic drawn from a jittered grid — no tiles, no
   real geography. */
window.WFO_DATA = (function () {
  /* ------------------------------------------------------------ calendar */
  var DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  var MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  var holidays = { "2026-10-26": "Public holiday" };
  function iso(d) { return d.getUTCFullYear() + "-" + ("0" + (d.getUTCMonth() + 1)).slice(-2) + "-" + ("0" + d.getUTCDate()).slice(-2); }
  var days = [], weeks = [];
  var start = new Date(Date.UTC(2026, 9, 5));
  for (var i = 0; i < 28; i++) {
    var d = new Date(start.getTime() + i * 86400000), k = iso(d), dow = d.getUTCDay(), w = Math.floor(i / 7) + 1;
    var weekend = dow === 0 || dow === 6, hol = holidays[k] || "";
    days.push({ d: k, n: d.getUTCDate(), dow: DOW[dow], mon: MON[d.getUTCMonth()], week: w, working: !weekend && !hol, weekend: weekend, holiday: hol });
    if (i % 7 === 0) weeks.push({ n: w, start: k, label: "" });
  }
  weeks.forEach(function (w) { var f = days[(w.n - 1) * 7], l = days[w.n * 7 - 1]; w.label = f.n + (f.mon === l.mon ? "" : " " + f.mon) + " – " + l.n + " " + l.mon; });
  var period = { start: "2026-10-05", end: "2026-10-30", label: "5 Oct 2026 — 30 Oct 2026", short: "5 – 30 Oct", weeksLabel: "4 weeks · Mon–Fri" };

  /* ------------------------------------------------------- map geometry */
  /* A 4×3 grid of cells on a 1000×420 canvas, corners and edge midpoints
     jittered by a seeded generator so the zones tile the land like real
     districts do. The bottom edge is the coastline; the notch in it is the
     harbour inlet. */
  var seed = 7;
  function rnd() { seed = (seed * 9301 + 49297) % 233280; return seed / 233280 - 0.5; }
  var V = [
    [[-40, -40], [250, -32], [520, -44], [770, -36], [1040, -40]],
    [[-40, 78], [240, 90], [510, 66], [750, 96], [1040, 80]],
    [[-40, 168], [220, 180], [535, 158], [730, 188], [1040, 166]],
    [[-40, 262], [245, 248], [505, 268], [765, 240], [1040, 258]]
  ];
  var H = [], W = [];
  for (var r = 0; r < 4; r++) { H[r] = []; for (var c = 0; c < 4; c++) { var a = V[r][c], b = V[r][c + 1]; H[r][c] = [(a[0] + b[0]) / 2 + rnd() * 30, (a[1] + b[1]) / 2 + (r === 0 || r === 3 ? rnd() * 10 : rnd() * 50)]; } }
  for (var r2 = 0; r2 < 3; r2++) { W[r2] = []; for (var c2 = 0; c2 < 5; c2++) { var a2 = V[r2][c2], b2 = V[r2 + 1][c2]; W[r2][c2] = [(a2[0] + b2[0]) / 2 + (c2 === 0 || c2 === 4 ? rnd() * 10 : rnd() * 50), (a2[1] + b2[1]) / 2 + rnd() * 30]; } }
  H[3][2] = [640, 212]; /* the harbour inlet */
  function cellPoly(r, c) { return [V[r][c], H[r][c], V[r][c + 1], W[r][c + 1], V[r + 1][c + 1], H[r + 1][c], V[r + 1][c], W[r][c]]; }
  function centroid(p) { var x = 0, y = 0; p.forEach(function (q) { x += q[0]; y += q[1]; }); return [x / p.length, y / p.length]; }
  var coast = [V[3][0], H[3][0], V[3][1], H[3][1], V[3][2], H[3][2], V[3][3], H[3][3], V[3][4]];
  var map = {
    w: 1000, h: 300,
    sea: coast.concat([[1040, 400], [-40, 400]]),
    river: "M310,-40 C335,20 330,80 400,115 C470,150 520,175 575,205 C600,215 620,212 640,212",
    ring: { cx: 500, cy: 118, rx: 330, ry: 105 },
    roads: [[[500, 118], [300, -40]], [[500, 118], [740, -40]], [[500, 118], [120, 262]], [[500, 118], [880, 256]], [[-40, 132], [1040, 112]]],
    harbourLabel: [640, 252]
  };

  /* --------------------------------------------------------------- zones */
  function pcs(k, n) { var out = []; for (var i = 1; i <= n; i++) out.push("HV" + k + " " + i); return out; }
  var zoneDefs = [
    ["HV-01", "Northgate", 0, 0, "#5B8DEF", 14, 190, { cur: 7.2, v1: 6.5, v2: 6.5 }],
    ["HV-02", "Millbrook", 0, 1, "#8E6CE0", 9, 90, { cur: 8.1, v1: 6.9, v2: 6.9 }],
    ["HV-03", "Hillcrest", 0, 2, "#2FB07E", 12, 185, { cur: 6.4, v1: 6.0, v2: 6.0 }],
    ["HV-04", "Eastfield", 0, 3, "#E3A72F", 11, 80, { cur: 9.3, v1: 7.4, v2: 7.4 }],
    ["HV-05", "Westhaven", 1, 0, "#E36B8B", 8, 110, { cur: 6.9, v1: 6.6, v2: 6.6 }],
    ["HV-06", "Kingsbridge", 1, 1, "#3FA7D6", 15, 182, { cur: 5.8, v1: 5.4, v2: 5.5 }],
    ["HV-07", "Stonebridge", 1, 2, "#B58ADB", 7, 69, { cur: 6.1, v1: 5.9, v2: 5.9 }],
    ["HV-08", "Ridgeway", 1, 3, "#62B36F", 13, 180, { cur: 6.2, v1: 5.7, v2: 5.8 }],
    ["HV-09", "Marsh End", 2, 0, "#F28C38", 6, 92, { cur: 5.1, v1: 6.4, v2: 5.0 }],
    ["HV-10", "Southbank", 2, 1, "#2C9E9E", 12, 184, { cur: 7.6, v1: 6.2, v2: 6.4 }],
    ["HV-11", "Old Harbour", 2, 2, "#D64F73", 10, 172, { cur: 6.3, v1: 6.0, v2: 6.0 }],
    ["HV-12", "Ferry Point", 2, 3, "#7A8AA6", 5, 97, { cur: 8.4, v1: 7.1, v2: 7.1 }]
  ];
  var zones = zoneDefs.map(function (z, i) {
    var poly = cellPoly(z[2], z[3]), c = centroid(poly);
    return { id: z[0], name: z[1], label: z[0] + " " + z[1], color: z[4], postcodes: pcs(i + 1, z[5]), demand: z[6], backfill: 0, wait: z[7].cur, poly: poly, c: c, specialistOnly: false, kind: "Residential" };
  });
  function zone(id) { return zones.filter(function (z) { return z.id === id; })[0]; }
  zone("HV-07").backfill = 9; zone("HV-07").backfillDates = ["2026-10-19", "2026-10-22", "2026-10-27"];
  zone("HV-12").specialistOnly = true; zone("HV-12").kind = "Industrial units · specialist skill required";
  zone("HV-11").kind = "Mixed · 3 non-movable appointments on Thu 8 Oct";
  zone("HV-02").kind = "Residential · single technician";
  zone("HV-09").kind = "Coastal · single technician";
  /* neighbours: cells sharing an edge */
  zones.forEach(function (z, i) {
    var r = zoneDefs[i][2], c = zoneDefs[i][3];
    z.neighbours = zones.filter(function (o, j) { var r2 = zoneDefs[j][2], c2 = zoneDefs[j][3]; return (Math.abs(r - r2) + Math.abs(c - c2)) === 1; }).map(function (o) { return o.id; });
  });

  /* --------------------------------------------------------- technicians */
  /* [id, skill, default zones, home offset from the zone centroid, jobs in the
     period for the current plan / plan v1 / plan v2, absences] */
  var techDefs = [
    ["T-1041", "Specialist", ["HV-12"], [-72, -22], 84, 88, 88],
    ["T-1042", "Standard", ["HV-01"], [-72, -20], 91, 95, 95],
    ["T-1043", "Standard", ["HV-01"], [64, -28], 88, 92, 92],
    ["T-1044", "Standard", ["HV-02"], [-72, -20], 79, 82, 82, [{ from: "2026-10-09", to: "2026-10-09", kind: "Leave" }]],
    ["T-1045", "Standard", ["HV-03"], [-72, -20], 93, 96, 96],
    ["T-1046", "Standard", ["HV-03"], [64, -28], 86, 91, 91],
    ["T-1047", "Standard", ["HV-04"], [-72, -20], 62, 65, 65, [{ from: "2026-10-12", to: "2026-10-16", kind: "Vacation" }]],
    ["T-1048", "Standard", ["HV-05"], [-66, 30], 97, 99, 99],
    ["T-1049", "Specialist", ["HV-06"], [-66, 30], 80, 86, 86],
    ["T-1050", "Standard", ["HV-06"], [62, 28], 85, 92, 90],
    ["T-1051", "Standard", ["HV-07"], [-66, 30], 82, 87, 87],
    ["T-1052", "Standard", ["HV-08"], [-66, 30], 90, 93, 93],
    ["T-1053", "Standard", ["HV-08"], [62, 28], 83, 89, 90],
    ["T-1054", "Standard", ["HV-09"], [-72, -22], 88, 93, 89],
    ["T-1055", "Standard", ["HV-10"], [-72, -22], 81, 84, 84, [{ from: "2026-10-06", to: "2026-10-06", kind: "Sick leave" }]],
    ["T-1056", "Standard", ["HV-10"], [62, 28], 89, 94, 92],
    ["T-1057", "Standard", ["HV-11"], [-72, -22], 87, 90, 90],
    ["T-1058", "Specialist", ["HV-11"], [70, 2], 78, 79, 79]
  ];
  var techs = techDefs.map(function (t) {
    var z = zone(t[2][0]);
    return { id: t[0], skill: t[1], zones: t[2], home: [z.c[0] + t[3][0], z.c[1] + t[3][1]], homePostcode: z.postcodes[2 + (t[3][0] > 0 ? 1 : 0)], jobs: t[4], absent: t[7] || [] };
  });
  function tech(id) { return techs.filter(function (t) { return t.id === id; })[0]; }

  /* --------------------------------------------------- what the solver changed */
  /* Every plan is the uploaded current allocation plus a set of named changes.
     A change carries the pill-level assignments it adds (overrides), the KPI
     effect it has (jobs per technician, wait time per zone — additive, so an
     undone change takes its effect with it), the rule that produced it and
     the explanation the UI shows. Plan v1 = all of the solver's changes; plan
     v2 = v1 with the dispatcher's fix and the alternative the re-run found. */
  var WED = ["2026-10-07", "2026-10-14", "2026-10-21", "2026-10-28"];
  var ALLZ = zones.map(function (z) { return z.id; }), ALLT = techs.map(function (t) { return t.id; });
  var vacationWhy = "T-1047 is on vacation 12–16 Oct (5 days, over the 2-day threshold), so HV-04 Eastfield is covered as whole-zone temporary assignments: T-1046 (Hillcrest, adjacent, 18 min from home) Mon–Wed and T-1051 (Stonebridge, adjacent) Thu–Fri. T-1047's usual allocation resumes on 19 Oct.";
  var changes = [
    { id: "packing", rule: "Multi-objective packing", kind: "improves", title: "Movable visits packed tighter in every zone",
      what: "Movable visits are regrouped by day so a technician's day fills up before another day opens; nothing moves across zones for this.",
      why: "The objective weights favour productivity and waiting time; packing the movable visits of each zone is the solver's first lever and touches no rule.",
      zones: ALLZ, techs: ALLT, week: 1, overrides: [],
      effects: { jobs: { "T-1041": 4, "T-1042": 3, "T-1043": 3, "T-1044": 3, "T-1045": 2, "T-1046": 3, "T-1047": 3, "T-1048": 4, "T-1049": 3, "T-1050": 5, "T-1051": 4, "T-1052": 2, "T-1053": 4, "T-1054": 1, "T-1055": 3, "T-1056": 3, "T-1057": 3, "T-1058": 1 },
        waits: { "HV-01": -0.7, "HV-02": -0.4, "HV-03": -0.4, "HV-04": -0.3, "HV-05": -0.2, "HV-06": -0.4, "HV-07": -0.1, "HV-08": -0.5, "HV-09": 0, "HV-10": -0.3, "HV-11": -0.3, "HV-12": -0.3 } },
      effect: "+54 visits placed in the period · avg wait −0.4 d across the region" },
    { id: "vacation", rule: "Availability · long absence", kind: "improves", title: "Eastfield covered during T-1047's vacation, 12–16 Oct",
      what: "Two neighbouring technicians take the zone for the week instead of leaving it empty.", why: vacationWhy,
      zones: ["HV-04"], techs: ["T-1047", "T-1046", "T-1051"], week: 2,
      overrides: [
        { tech: "T-1046", zone: "HV-04", dates: ["2026-10-12", "2026-10-13", "2026-10-14"], kind: "temp" },
        { tech: "T-1051", zone: "HV-04", dates: ["2026-10-15", "2026-10-16"], kind: "temp" }
      ],
      effects: { jobs: { "T-1046": 2, "T-1051": 1 }, waits: { "HV-04": -1.6 } },
      effect: "HV-04 wait 9.3 → 7.4 d · 5 days that had no technician are covered" },
    { id: "sick", rule: "Availability · short absence", kind: "improves", title: "Southbank's sick day split to a neighbour, Tue 6 Oct",
      what: "A one-day absence does not reassign the zone: part of the day's visits go to a neighbour with free slots.",
      why: "T-1055 is on sick leave on Tue 6 Oct (1 day, under the 2-day threshold), so the zone is not reassigned: 4 of the day's 7 visits go to T-1053 (Ridgeway, adjacent, 3 free slots) as a partial temporary assignment and T-1056 keeps the rest.",
      zones: ["HV-10"], techs: ["T-1055", "T-1053"], week: 1,
      overrides: [{ tech: "T-1053", zone: "HV-10", dates: ["2026-10-06"], kind: "temp", partial: true }],
      effects: { jobs: { "T-1053": 2 }, waits: { "HV-10": -0.2 } },
      effect: "4 of the day's 7 visits kept on the day · HV-10 wait −0.2 d" },
    { id: "coverage", rule: "Zone-level demand · coverage", kind: "improves", title: "Millbrook's uncovered postcode HV2 7 covered, Fri 9 Oct",
      what: "Three booked visits that had no technician get one from the adjacent zone.",
      why: "T-1044 is on leave on Fri 9 Oct and HV-02 Millbrook has no second technician, so postcode HV2 7's three booked visits had no cover in the current plan. T-1042 (Northgate, adjacent, 2 free slots) takes them; his own zone keeps its Friday coverage.",
      zones: ["HV-02"], techs: ["T-1044", "T-1042"], week: 1,
      overrides: [{ tech: "T-1042", zone: "HV-02", dates: ["2026-10-09"], kind: "temp", partial: true }],
      effects: { jobs: { "T-1042": 1 }, waits: { "HV-02": -0.8 } },
      effect: "HV-02 wait 8.1 → 6.9 d · 3 booked visits no longer slip a week" },
    { id: "capacity", rule: "Daily capacity · 7 visits", kind: "improves", title: "T-1048's 8-visit day brought back to 7, Tue 13 Oct",
      what: "Two movable visits move to the neighbouring technician who has room that day.",
      why: "T-1048 had 8 visits booked in HV-05 Westhaven on Tue 13 Oct against the capacity of 7 per day. Two movable visits move to T-1050 (Kingsbridge, adjacent, 2 free slots); the six with parts allocated stay with T-1048.",
      zones: ["HV-05"], techs: ["T-1048", "T-1050"], week: 2,
      overrides: [{ tech: "T-1050", zone: "HV-05", dates: ["2026-10-13"], kind: "temp", partial: true }],
      effects: { jobs: { "T-1048": -2, "T-1050": 2 }, waits: { "HV-05": -0.1 } },
      effect: "T-1048 at 114% → 100% of capacity that day · 2 visits to T-1050" },
    { id: "marsh-move", rule: "Workload balance · cross-zone allocation", kind: "worsens", title: "Marsh End's technician moved to Southbank on Wednesdays",
      what: "T-1054 leaves his default zone every Wednesday to absorb Southbank's overload; Marsh End's Wednesday visits slip to Thursday and Friday.",
      why: "HV-10 Southbank runs at 96% of capacity on Wednesdays while HV-09 Marsh End has slack, so T-1054 leaves his default zone every Wednesday to work Southbank. Marsh End's Wednesday visits are rescheduled to Thursday and Friday — its average wait rises from 5.1 to 6.4 days.",
      zones: ["HV-09", "HV-10"], techs: ["T-1054", "T-1056"], week: 1,
      overrides: [{ tech: "T-1054", zone: "HV-10", dates: WED, kind: "moved" }],
      effects: { jobs: { "T-1054": 4, "T-1056": 2 }, waits: { "HV-09": 1.3, "HV-10": -0.9 } },
      effect: "HV-10 wait 7.6 → 6.2 d, but HV-09 wait 5.1 → 6.4 d" },
    { id: "specialist", rule: "Special skills · specialist-only zone", kind: "improves", title: "A second Specialist assists in Ferry Point, 20–21 Oct",
      what: "Demand on two days exceeds the resident Specialist's capacity; only another Specialist may help.",
      why: "HV-12 Ferry Point requires the Specialist skill. Booked demand on 20–21 Oct exceeds T-1041's capacity, so T-1049 (Specialist, Kingsbridge) assists for two days. Standard technicians are not eligible for this zone, and a specialist may travel further than the neighbouring-zone rule allows.",
      zones: ["HV-12"], techs: ["T-1041", "T-1049"], week: 3,
      overrides: [{ tech: "T-1049", zone: "HV-12", dates: ["2026-10-20", "2026-10-21"], kind: "temp", partial: true }],
      effects: { jobs: { "T-1049": 3 }, waits: { "HV-12": -1.0 } },
      effect: "HV-12 wait 8.4 → 7.1 d · 6 specialist visits placed on the days they were booked" },
    { id: "pinned", rule: "Non-movable appointments", kind: "neutral", title: "Old Harbour's three confirmed appointments kept, Thu 8 Oct",
      what: "Appointments with parts allocated keep their technician and date; the movable visits are reshuffled around them.",
      why: "Three appointments in HV-11 Old Harbour on Thu 8 Oct are non-movable (parts allocated, customer confirmed). They stay with T-1057 on that date; only the movable visits around them were reshuffled.",
      zones: ["HV-11"], techs: ["T-1057"], week: 1,
      overrides: [{ tech: "T-1057", zone: "HV-11", dates: ["2026-10-08"], kind: "pinned" }],
      effects: {}, effect: "Kept with T-1057 on the date · no effect on the KPIs" },
    { id: "backfill", rule: "Zone-level demand · historical backfill", kind: "neutral", flagged: true, title: "Stonebridge allocated on last year's demand for three dates",
      what: "Three sparse dates keep a technician on the zone because last year's demand for the same dates says visits will come.",
      why: "HV-07 Stonebridge has only 69 visits booked for four weeks. For 19, 22 and 27 Oct the booked demand is below last year's for the same dates, so the zone is allocated on last year's demand (9 visits) to keep it covered. Only booked visits are shown; nothing is invented on the visit list.",
      zones: ["HV-07"], techs: ["T-1051"], week: 3,
      overrides: [{ tech: "T-1051", zone: "HV-07", dates: ["2026-10-19", "2026-10-22", "2026-10-27"], kind: "backfill" }],
      effects: { waits: { "HV-07": -0.1 } }, effect: "19, 22 and 27 Oct stay covered · a dispatcher confirms or rejects" },
    { id: "spare", rule: "Zone-level demand", kind: "neutral", title: "T-1058's Friday 16 Oct visits fit into Thursday",
      what: "A day with no visits left — spare capacity the dispatcher can use.",
      why: "T-1058's Friday 16 Oct visits fit into Thursday, leaving the day with no visits — spare capacity the dispatcher can use.",
      zones: ["HV-11"], techs: ["T-1058"], week: 2,
      overrides: [{ tech: "T-1058", zone: "HV-11", dates: ["2026-10-16"], kind: "off" }],
      effects: {}, effect: "One day of spare capacity in Old Harbour" },
    { id: "marsh-keep", rule: "Dispatcher feedback · re-optimization", kind: "improves", title: "Southbank's Wednesday overflow to T-1053 instead of moving T-1054",
      what: "The re-run keeps Marsh End's technician at home and sends Southbank's Wednesday overflow to a neighbour with spare capacity.",
      why: "Feedback on plan v1: keep HV-09 Marsh End covered on Wednesdays. T-1054 now stays in his default zone; Southbank's Wednesday overflow (3–4 visits) goes to T-1053 (Ridgeway, adjacent, spare capacity) instead. Marsh End's average wait returns to 5.0 days; fleet productivity gives up 0.02 jobs per day.",
      zones: ["HV-10", "HV-09"], techs: ["T-1053", "T-1054"], week: 1,
      overrides: [{ tech: "T-1053", zone: "HV-10", dates: WED, kind: "temp", partial: true }],
      effects: { jobs: { "T-1053": 1 }, waits: { "HV-09": -0.1, "HV-10": -0.7 } },
      effect: "HV-10 wait 7.1 → 6.4 d · Marsh End keeps its Wednesday coverage",
      alts: [
        { name: "Chosen — T-1053 covers the overflow", effect: "wait 5.0 d in Marsh End · fleet 4.75 jobs/day · 2 assignments changed", chosen: true },
        { name: "T-1056 takes 8 visits on Wednesdays", effect: "breaks the 7-per-day capacity rule — not allowed" },
        { name: "Leave Southbank at 96% on Wednesdays", effect: "wait in HV-10 +0.4 d · 0 assignments changed" }
      ] }
  ];
  changes.forEach(function (c) { c.overrides.forEach(function (o) { o.change = c.id; o.rule = c.rule; o.why = c.why; if (c.alts) o.alts = c.alts; }); });
  var plans = {
    v1: ["packing", "vacation", "sick", "coverage", "capacity", "marsh-move", "specialist", "pinned", "backfill", "spare"],
    v2: ["packing", "vacation", "sick", "coverage", "capacity", "specialist", "pinned", "backfill", "spare", "marsh-keep"]
  };
  /* Problems a plan carries, as a function of which changes are applied. */
  function flagsFor(applied) {
    var on = function (id) { return applied.indexOf(id) >= 0; }, out = [];
    if (!on("vacation")) out.push({ kind: "absence", zone: "HV-04", date: "2026-10-12", title: "No cover during an absence", text: "T-1047 is on vacation 12–16 Oct and nobody is allocated to Eastfield." });
    if (!on("coverage")) out.push({ kind: "uncovered", zone: "HV-02", date: "2026-10-09", title: "Uncovered postcode", text: "HV2 7 has three booked visits and no technician on Fri 9 Oct (T-1044 on leave)." });
    if (!on("capacity")) out.push({ kind: "over-capacity", tech: "T-1048", zone: "HV-05", date: "2026-10-13", title: "Over capacity", text: "8 visits on Tue 13 Oct against a capacity of 7 per day." });
    if (on("marsh-move")) out.push({ kind: "wait-worse", zone: "HV-09", title: "Wait time up", text: "Average wait rises from 5.1 to 6.4 days: T-1054 is moved to Southbank on Wednesdays.", decision: true });
    if (!on("marsh-move") && !on("marsh-keep")) out.push({ kind: "overload", zone: "HV-10", title: "Wednesday overload", text: "Southbank runs at 96% of capacity on Wednesdays; visits slip to Thursday." });
    if (on("backfill")) out.push({ kind: "backfill", zone: "HV-07", title: "Allocated on historical demand", text: "19, 22 and 27 Oct are allocated on last year's demand for the same dates — confirm or reject.", decision: true });
    return out;
  }

  /* ------------------------------------------------------ run + settings */
  var region = { id: "harborview", name: "Harborview Metro", others: ["Northern Lakes", "Coastal South"] };
  var pickerFiles = [
    { name: "Harborview_2026-10-05_4w.xlsx", kind: "XLSX · 7 sheets · 1,640 visits", size: "1.4 MB", main: true },
    { name: "Harborview_2026-09-07_4w.xlsx", kind: "XLSX · 7 sheets · 1,588 visits", size: "1.3 MB" },
    { name: "NorthernLakes_2026-10-05_2w.xlsx", kind: "XLSX · 7 sheets · 910 visits", size: "0.8 MB" },
    { name: "Harborview_technicians.xlsx", kind: "XLSX · 2 sheets", size: "0.1 MB" }
  ];
  var inputSheets = ["Visits", "TechLocation", "Skills", "SpecialSkills", "Calendars", "WZ_Zip", "WZ_Assignments"];
  var stages = [
    { name: "Validate the input file", done: "7 sheets · 18 technicians · 12 zones · 1,640 visits · 1 warning", ms: 900, warn: true },
    { name: "Build the travel matrix", done: "18 homes × 12 zones · neighbouring-zone graph", ms: 800 },
    { name: "Load rules and objectives", done: "5 hard rules · 4 soft rules · capacity 7 visits/day", ms: 700 },
    { name: "Solve the allocation on the GPU solver", done: "19 working days · 342 technician-days · 1,640 visits placed", ms: 1700, tick: true },
    { name: "Post-process and compute KPIs", done: "productivity · capacity · wait time, before and after", ms: 800 }
  ];
  var reoptStages = [
    { name: "Apply the dispatcher's fixes and notes", done: "1 manual fix · 1 note → 1 constraint added (keep HV-09 covered on Wednesdays)", ms: 700 },
    { name: "Re-solve with minimal disruption", done: "2 assignments changed · 10 zones unchanged", ms: 1300, tick: true },
    { name: "Recompute KPIs", done: "productivity · capacity · wait time", ms: 600 }
  ];
  var uploadWarning = { title: "Upload warning", text: "2 technicians in Calendars have no home location in TechLocation (T-1052, T-1056). Their default zone's centre is used as the start location." };
  var settings = {
    mode: "Roster — a stable technician-to-zone pattern for the whole period",
    horizon: "Up to 4 weeks per run",
    capacity: "7 visits per technician per working day (1 h per visit)",
    minimalDisruption: true,
    objectives: [
      { name: "Productivity", desc: "Jobs per technician per working day", weight: 40 },
      { name: "Waiting time", desc: "Booking to appointment, calendar days", weight: 35 },
      { name: "Workload balance", desc: "Even load across technicians and days", weight: 25 }
    ],
    rules: [
      { name: "Availability and absences", type: "Hard", desc: "No assignments on absent or non-working days; absences over 2 days reassign the zone, shorter ones split the day's visits." },
      { name: "Daily capacity", type: "Hard", desc: "Assigned work never exceeds 7 visits per technician per day." },
      { name: "Skill match", type: "Hard", desc: "A visit's required skill must be on the technician's skill list." },
      { name: "Specialist-only zones", type: "Hard", desc: "Zones that require special skills accept specialists only." },
      { name: "Non-movable appointments", type: "Hard", desc: "Confirmed appointments with parts allocated keep their technician and date." },
      { name: "Home proximity", type: "Soft", desc: "Zones are assigned close to the technician's home; distant zones are penalised (specialists excepted)." },
      { name: "Neighbouring zones", type: "Soft", desc: "Several zones on one day should share a border." },
      { name: "Zone-level demand", type: "Soft", desc: "Coverage follows booked visits, then the demand forecast where one is supplied; sparse dates are backfilled from last year's demand for the same period." },
      { name: "Cross-zone allocation", type: "Soft", desc: "Selected technicians may work a neighbouring zone when it balances the load." }
    ],
    regions: [
      { name: "Harborview Metro", state: "Active · this rule set", zones: 12, techs: 18 },
      { name: "Northern Lakes", state: "Own rule set · 2-week horizon", zones: 9, techs: 11 },
      { name: "Coastal South", state: "Own rule set · crews enabled", zones: 15, techs: 24 }
    ],
    connectors: [
      { name: "Field-service system", state: "Connected", dir: "In: staff, availability, bookings · Out: allocations · Back: actual durations" },
      { name: "Booking system", state: "Connected", dir: "In: appointments and SLA type" },
      { name: "Inventory (parts)", state: "Configured", dir: "In: parts availability → non-movable flag" },
      { name: "HR / workforce management", state: "Configured", dir: "In: absences and calendars" },
      { name: "Demand forecast", state: "Configured", dir: "In: expected visits per zone and day" },
      { name: "BI export", state: "Configured", dir: "Out: KPIs per plan version" }
    ]
  };
  var sources = [
    { name: "Manual upload", state: "XLSX", ok: false },
    { name: "Field-service system", state: "connected", ok: true },
    { name: "Booking · Inventory · HR/WFM · Forecast · BI", state: "configured", ok: true }
  ];
  var exportColumns = ["Resource ID", "Item ID", "Work Zone Label", "Start Date", "End Date", "Ratio", "Recurrence Type", "Recur Every", "Assignment Type", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Decision", "Comment"];
  var priorHistory = [
    { time: "Sep 28", text: "Execution data received for the September plan", sub: "96% of planned visits completed · actual durations fed back to the next run", kind: "" },
    { time: "Sep 4", text: "September plan exported and sent to the field-service system", sub: "12 zones accepted · 0 rejected · Sam Okafor", kind: "ok" },
    { time: "Sep 4", text: "Plan optimized: Harborview Metro, 7 Sep – 2 Oct", sub: "12 zones · 18 technicians · 1,588 visits · 1 flag", kind: "" }
  ];
  var user = { name: "Sam Okafor", role: "Dispatcher · Harborview", initials: "SO" };
  var jobTypes = ["Repair", "Installation", "Maintenance", "Safety inspection"];
  var slaTypes = ["Standard", "Priority 48 h", "Standard", "Standard", "Priority 48 h"];
  var suggestedComment = "Keep Marsh End covered on Wednesdays — the Wednesday visits are the coastal run and cannot slip to Thursday.";

  return { days: days, weeks: weeks, period: period, holidays: holidays, map: map, zones: zones, zone: zone, techs: techs, tech: tech, changes: changes, plans: plans, flagsFor: flagsFor, region: region, pickerFiles: pickerFiles, inputSheets: inputSheets, stages: stages, reoptStages: reoptStages, uploadWarning: uploadWarning, settings: settings, sources: sources, exportColumns: exportColumns, priorHistory: priorHistory, user: user, jobTypes: jobTypes, slaTypes: slaTypes, suggestedComment: suggestedComment, capacityPerDay: 7 };
})();
