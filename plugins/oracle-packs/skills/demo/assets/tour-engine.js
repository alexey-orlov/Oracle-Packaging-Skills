/* tour-engine.js — the guided-walkthrough mechanics, extracted once.
 *
 * Three walkthroughs were built before this file existed, and each carried its
 * own copy of the same 150 lines: a STEPS array, a `tour` object, a capturing
 * click guard, a positioner and an end card. The copies drifted — the counter
 * learned to move inside a step in the third one only, the "don't cover what
 * this step is describing" rule existed in one — and the third demo cost four
 * rounds partly for that reason. This is that object, once, with every
 * behaviour the three of them earned.
 *
 * Plain ES5, no dependencies, loaded with a <script> tag before the demo's own
 * script. It owns the callout, the click guard and the end card; it owns
 * nothing about the product being demonstrated.
 *
 *   <script src="tour-engine.js"></script>
 *   <script src="data.js"></script>
 *   <script src="demo.js"></script>
 *
 * See tour-engine.md for the DOM contract, the step shape and the rules the
 * behaviours encode. tour-engine-example.html is a runnable three-step demo.
 */
(function (root) {
  "use strict";

  function $(sel, ctx) { return typeof sel === "string" ? (ctx || document).querySelector(sel) : sel; }
  function noop() {}

  var DEFAULT_IDS = {
    card: "#tour",
    step: "#tour-step",
    title: "#tour-title",
    body: "#tour-body",
    progress: "#tour-progress",
    next: "#tour-next",
    skip: "#tour-skip",
    pill: "#tour-pill",
    toggle: "#tour-toggle",
    gate: "#gate",
    gateTitle: "#gate-title",
    gateBody: "#gate-body",
    gateStart: "#gate-start",
    gateFree: "#gate-free",
    gateTry: "#gate-try",
    gateSteps: "#gate-steps",
    gateNote: ".gate-note"
  };

  /* Everything a person can act on. A step's target must match this, or the
     guard cannot tell a real control from a stray click on the page. */
  var DEFAULT_CLICKABLE =
    "button, a, input, select, textarea, label, tr.clickable, li[data-file], " +
    "[role=menuitem], [role=tab], [data-act]";

  function createTour(config) {
    var cfg = config || {};
    var STEPS = cfg.steps || [];
    if (!STEPS.length) throw new Error("tour-engine: config.steps is required");

    var ids = {};
    for (var k in DEFAULT_IDS) if (DEFAULT_IDS.hasOwnProperty(k)) ids[k] = (cfg.ids && cfg.ids[k]) || DEFAULT_IDS[k];

    var CLICKABLE = cfg.clickableSelector || DEFAULT_CLICKABLE;
    var W = cfg.width || 306;
    var GAP = cfg.gap || 14;
    var LABELS = cfg.labels || {};
    var EXIT_LABEL = LABELS.exit || "Exit guide";
    var RESTART_LABEL = LABELS.restart || "Restart walkthrough";
    var isBusy = cfg.busy || function () { return false; };
    var onStart = cfg.onStart || noop;
    var onExit = cfg.onExit || noop;
    var onStep = cfg.onStep || noop;

    /* MAJORS: the number the viewer counts in. A "major" is one thing the
       viewer would describe out loud ("run it", "see what improved"); several
       clicks may live inside one. The counter shows both, and the progress bar
       fills the current segment fractionally, so EVERY click moves something —
       a counter that stands still through four clicks reads as broken. */
    var MAJORS = cfg.majors || STEPS.reduce(function (m, s) { return Math.max(m, s.major || 1); }, 1);
    var MAJOR_N = {}, MAJOR_I = [];
    STEPS.forEach(function (st) {
      var m = st.major || 1;
      MAJOR_N[m] = (MAJOR_N[m] || 0) + 1;
      MAJOR_I.push(MAJOR_N[m]);
    });

    var tour = {
      active: false,
      i: 0,
      steps: STEPS,
      majors: MAJORS,
      el: $(ids.card),
      target: null,
      tries: 0,

      step: function () { return STEPS[this.i]; },
      stepId: function () { return STEPS[this.i] ? STEPS[this.i].id : ""; },
      counterText: function () {
        var st = STEPS[this.i];
        if (!st) return "";
        var sub = MAJOR_I[this.i], subN = MAJOR_N[st.major || 1];
        var head = "Step " + (st.major || 1) + " of " + MAJORS;
        return subN > 1 ? head + " · " + sub + " of " + subN : head;
      },

      start: function () {
        this.active = true;
        this.i = 0;
        document.body.classList.add("tour-on");
        if ($(ids.pill)) $(ids.pill).hidden = false;
        if ($(ids.toggle)) $(ids.toggle).textContent = EXIT_LABEL;
        onStart(this);
        this.show();
      },

      show: function () {
        var st = STEPS[this.i], self = this;
        if (!st) return;
        /* `before` sets up the screen a step needs (open the panel it points
           into). It runs once, and it runs BEFORE target() is asked for. */
        if (st.before && !st._did) { st._did = 1; st.before(); }
        var t = st.target();
        /* A target can be a frame late when the previous action re-rendered.
           Wait for it rather than failing the step. */
        if (!t) {
          if (this.tries++ < 90) return void requestAnimationFrame(function () { self.show(); });
          return;
        }
        this.tries = 0;
        if (this.target) this.target.classList.remove("tour-target");
        this.target = t;
        t.classList.add("tour-target");

        if ($(ids.step)) $(ids.step).textContent = this.counterText();
        if ($(ids.title)) $(ids.title).textContent = st.title;
        if ($(ids.body)) $(ids.body).textContent = st.body;

        if ($(ids.progress)) {
          var sub = MAJOR_I[this.i], subN = MAJOR_N[st.major || 1], bars = "";
          for (var n = 1; n <= MAJORS; n++) {
            var pct = n < (st.major || 1) ? 100 : n > (st.major || 1) ? 0 : Math.round(sub / subN * 100);
            bars += '<i><b style="width:' + pct + '%"></b></i>';
          }
          $(ids.progress).innerHTML = bars;
        }

        /* A passive step asks for nothing on the page, so Next is its way
           forward and Skip has no meaning there. */
        if ($(ids.next)) $(ids.next).hidden = !st.passive;
        if ($(ids.skip)) $(ids.skip).hidden = !!st.passive;

        this.el.hidden = false;
        this.el.dataset.side = st.side || "bottom";
        document.body.classList.toggle("tour-gutter", !!st.dock);
        try { t.scrollIntoView({ block: st.scroll || "nearest", behavior: "smooth", inline: "nearest" }); } catch (e) {}

        this.reposition();
        setTimeout(function () { self.reposition(); }, 320);
        setTimeout(function () { self.reposition(); }, 720);
        onStep(st, this);
      },

      /* The demo calls after("<id>") from inside the handler of the action the
         step asked for. It advances only when that action is the one the
         current step named, so a viewer clicking ahead cannot skip a step.
         CALL THE STATE-CHANGING ACTION FIRST, then after(): reversing them
         advances the tour while the page is still busy, and the real click is
         then blocked by the guard. */
      after: function (id) {
        if (!this.active || !id) return;
        if (STEPS[this.i] && STEPS[this.i].id === id) this.next();
      },

      next: function () {
        if (!this.active) return;
        /* A step marked `waits` starts an async stage. Hide the callout and
           stop; the demo calls next() again (or after()) when the stage lands. */
        if (STEPS[this.i] && STEPS[this.i].waits && isBusy()) {
          this.el.hidden = true;
          if (this.target) { this.target.classList.remove("tour-target"); this.target = null; }
          return;
        }
        this.i++;
        if (this.i >= STEPS.length) return this.finish();
        var self = this;
        setTimeout(function () { self.show(); }, cfg.stepDelay || 280);
      },

      /* Skip performs the step's own action rather than jumping over it, so the
         page state stays consistent with the narration. */
      skip: function () { var st = STEPS[this.i]; if (st && st.auto) st.auto(); },

      exit: function () {
        this.active = false;
        this.el.hidden = true;
        if (this.target) this.target.classList.remove("tour-target");
        this.target = null;
        document.body.classList.remove("tour-on");
        document.body.classList.remove("tour-gutter");
        if ($(ids.pill)) $(ids.pill).hidden = true;
        if ($(ids.toggle)) $(ids.toggle).textContent = RESTART_LABEL;
        onExit(this);
      },

      /* The end card is FOR THE VIEWER: what they can act on now, in three
         sentences and three doors, with no figures. It is never a recap of
         what the build did — that reads as a justification of the session. */
      finish: function () {
        this.exit();
        var end = cfg.end || {};
        var g = $(ids.gate);
        if ($(ids.step)) $(ids.step).textContent = "Step " + MAJORS + " of " + MAJORS + " · done";
        if (!g) return;
        if ($(ids.gateTitle)) $(ids.gateTitle).textContent = end.title || "What you can act on now";
        if ($(ids.gateBody)) $(ids.gateBody).textContent = end.body || "";
        if ($(ids.gateSteps)) $(ids.gateSteps).hidden = true;

        var tryEl = $(ids.gateTry);
        var doors = end.doors || [];
        if (tryEl) {
          tryEl.innerHTML = doors.map(function (d, n) {
            return '<button type="button" data-door="' + (d.id || n) + '"><b>' +
              d.label + "</b><span>" + (d.hint || "") + "</span></button>";
          }).join("");
          tryEl.hidden = !doors.length;
          tryEl.onclick = function (e) {
            var b = e.target.closest("[data-door]");
            if (!b) return;
            g.hidden = true;
            var door = doors.filter(function (d, n) { return String(d.id || n) === b.dataset.door; })[0];
            if (door && door.go) door.go();
          };
        }
        if ($(ids.gateStart)) {
          $(ids.gateStart).textContent = end.replayLabel || "Replay the walkthrough";
          $(ids.gateStart).onclick = function () { location.href = location.pathname; };
        }
        if ($(ids.gateFree)) {
          $(ids.gateFree).textContent = end.exploreLabel || "Keep exploring";
          $(ids.gateFree).onclick = function () { g.hidden = true; };
        }
        if (end.note && $(ids.gateNote)) $(ids.gateNote).textContent = end.note;
        g.hidden = false;
      },

      reposition: function () {
        if (!this.active || !this.target || this.el.hidden) return;
        var st = STEPS[this.i];
        /* A re-render replaces nodes: re-resolve the target rather than
           following a detached one off-screen. */
        if (!document.body.contains(this.target)) {
          var t = st.target();
          if (t) { this.target.classList.remove("tour-target"); this.target = t; t.classList.add("tour-target"); }
          else return;
        }
        /* `anchor` is what the card is positioned against when it differs from
           the thing being highlighted (highlight a row, sit beside its table). */
        var anchor = (st.anchor && st.anchor()) || this.target;
        var r = anchor.getBoundingClientRect();
        var h = this.el.offsetHeight || 160;
        var side = st.side || "bottom", top, left;

        /* A docked step lives in the gutter the page reserves while the tour
           runs, so the card never lands on the analysis it is describing. */
        if (st.dock === "right" || st.dock === "left") {
          left = st.dock === "right" ? innerWidth - W - 12 : 12;
          top = Math.max(56, Math.min(innerHeight - h - 8, r.top - 8));
          this.el.style.top = top + "px";
          this.el.style.left = left + "px";
          this.el.dataset.side = st.dock === "right" ? "left" : "right";
          return;
        }

        var fits = {
          right: r.right + GAP + W < innerWidth,
          left: r.left - GAP - W > 0,
          bottom: r.bottom + GAP + h < innerHeight,
          top: r.top - GAP - h > 0
        };
        if (!fits[side]) side = ["bottom", "top", "right", "left"].filter(function (s) { return fits[s]; })[0] || "bottom";
        if (side === "right") { left = r.right + GAP; top = r.top - 8; }
        if (side === "left") { left = r.left - GAP - W; top = r.top - 8; }
        if (side === "bottom") { left = r.left; top = r.bottom + GAP; }
        if (side === "top") { left = r.left; top = r.top - GAP - h; }
        top = Math.max(8, Math.min(innerHeight - h - 8, top));
        left = Math.max(8, Math.min(innerWidth - W - 8, left));

        /* Never cover the element this step's copy is talking about. */
        var keep = st.avoid && st.avoid();
        if (keep && document.body.contains(keep)) {
          var kr = keep.getBoundingClientRect();
          var hit = !(left + W <= kr.left || left >= kr.right || top + h <= kr.top || top >= kr.bottom);
          if (hit && kr.width && kr.height) {
            var cand = [
              { t: kr.bottom + GAP, l: left, s: "bottom" },
              { t: kr.top - GAP - h, l: left, s: "top" },
              { t: top, l: kr.right + GAP, s: "right" },
              { t: top, l: kr.left - GAP - W, s: "left" }
            ].filter(function (c) {
              return c.t >= 8 && c.t + h <= innerHeight - 8 && c.l >= 8 && c.l + W <= innerWidth - 8;
            })[0];
            if (cand) { top = cand.t; left = cand.l; side = cand.s; }
            else { top = Math.max(8, Math.min(innerHeight - h - 8, kr.bottom + GAP)); side = "bottom"; }
          }
        }
        this.el.style.top = top + "px";
        this.el.style.left = left + "px";
        this.el.dataset.side = side;
      },

      /* QA hook: is the callout currently covering the element this step names?
         Assert it in the scripted click-through — measure, do not eyeball. */
      avoidHit: function () {
        var st = STEPS[this.i];
        if (!this.active || this.el.hidden || !st || !st.avoid) return false;
        var keep = st.avoid();
        if (!keep || !document.body.contains(keep)) return false;
        var a = this.el.getBoundingClientRect(), b = keep.getBoundingClientRect();
        if (!b.width || !b.height) return false;
        return !(a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom);
      },

      nudge: function () {
        var self = this;
        this.el.classList.remove("is-nudge");
        void this.el.offsetWidth;
        this.el.classList.add("is-nudge");
        setTimeout(function () { self.el.classList.remove("is-nudge"); }, 400);
      }
    };

    if (!tour.el) throw new Error("tour-engine: no callout element at " + ids.card);

    /* ---- the click guard: only the designated control acts while the tour runs.
       Capturing, so it stops the event before the page's own handlers see it. */
    document.addEventListener("click", function (e) {
      if (!tour.active || !tour.target) return;
      if (e.target.closest([ids.card, ids.toggle, ids.gate].join(", "))) return;
      if (cfg.alwaysAllowSelector && e.target.closest(cfg.alwaysAllowSelector)) return;
      var el = e.target.closest(CLICKABLE);
      /* A passive step asks for no click at all: its target is a container, so
         its own children must not act either. Everything is blocked; Next is
         the way on. */
      if (STEPS[tour.i] && STEPS[tour.i].passive) {
        e.preventDefault(); e.stopPropagation();
        if (el) tour.nudge();
        return;
      }
      if (!el) return;
      if (tour.target.contains(el) || el.contains(tour.target)) return;
      e.preventDefault(); e.stopPropagation();
      tour.nudge();
    }, true);

    window.addEventListener("resize", function () { tour.reposition(); });
    document.addEventListener("scroll", function () { tour.reposition(); }, true);
    if ($(ids.skip)) $(ids.skip).addEventListener("click", function () { tour.skip(); });
    if ($(ids.next)) $(ids.next).addEventListener("click", function () { tour.next(); });
    if ($(ids.toggle)) {
      $(ids.toggle).addEventListener("click", function () {
        if (tour.active) tour.exit();
        else location.href = location.pathname;
      });
    }

    return tour;
  }

  /* ---- URL switches -------------------------------------------------------
     ?tour=off   open with no guide, primed to a state (capture, deep links)
     ?ui=clean   hide the demo's own chrome (screenshot mode: product UI only)
     ?state=…    which primed state to open in
     Everything else the demo defines itself; params() hands over the rest. */
  function params() { return new URLSearchParams(location.search); }

  /* boot() wires the gate and the switches so every demo behaves the same way:
       tour=off  → exit the tour, hide the gate, prime the named state
       otherwise → show the gate; Start runs the tour, Explore primes and frees
     `prime(stateName)` and `clean()` are the demo's own. */
  function boot(opts) {
    var p = params();
    var tour = opts.tour;
    var gate = $(opts.gate || DEFAULT_IDS.gate);
    var start = $(opts.gateStart || DEFAULT_IDS.gateStart);
    var free = $(opts.gateFree || DEFAULT_IDS.gateFree);
    var prime = opts.prime || noop;
    var state = p.get("state") || "";

    if (p.get("ui") === "clean" && opts.clean) opts.clean();
    if (p.get("tour") === "off") {
      tour.exit();
      if (gate) gate.hidden = true;
      prime(state || opts.defaultState || "");
      if (opts.afterPrime) opts.afterPrime();
    } else {
      if (state) prime(state);
      if (gate) gate.hidden = false;
      if (start) start.addEventListener("click", function () { gate.hidden = true; tour.start(); });
      if (free) {
        free.addEventListener("click", function () {
          gate.hidden = true;
          tour.exit();
          prime(opts.freeState || opts.defaultState || "");
          if (opts.afterPrime) opts.afterPrime();
        });
      }
    }
    return p;
  }

  var api = { create: createTour, params: params, boot: boot, DEFAULT_IDS: DEFAULT_IDS, DEFAULT_CLICKABLE: DEFAULT_CLICKABLE };
  root.TourEngine = api;
  if (typeof module !== "undefined" && module.exports) module.exports = api;
})(typeof window !== "undefined" ? window : this);
