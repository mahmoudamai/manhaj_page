/* =====================================================================
   MANHAJ — CORE JS  (one script for the whole page; blocks carry no JS)
   Everything is driven by data-attributes, so any block can be moved,
   duplicated or removed in GHL without breaking anything.
   ===================================================================== */
(function () {
  "use strict";
  if (window.__MH_CORE__) return;
  window.__MH_CORE__ = true;

  var doc = document;
  var root = doc.documentElement;
  var cfg = window.MH_CONFIG || {};
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var OPTIONS = {
    theme: ["petrol", "clay", "sage", "night", "sand"],
    accent: ["", "gold", "coral", "apricot", "terracotta", "mint", "rose"],
    type: ["editorial", "classic", "modern"]
  };
  var FONTS = {
    classic: "https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;800&display=swap",
    modern: "https://fonts.googleapis.com/css2?family=Readex+Pro:wght@300;400;500;600;700&display=swap"
  };

  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      if (val === null) localStorage.removeItem(key);
      else localStorage.setItem(key, val);
    } catch (e) { return null; }
  }
  function param(name) {
    try { return new URLSearchParams(location.search).get(name); } catch (e) { return null; }
  }

  /* ---------- 1. THEME: config  <  saved lab choice  <  URL ---------- */
  var labOn = param("mh-lab") === "1" || cfg.lab === true || store("mh-lab") === "1";
  if (param("mh-lab") === "0") { labOn = false; store("mh-lab", null); }

  function pick(key) {
    var v = param("mh-" + key);
    if (v === null && labOn) v = store("mh-" + key);
    if (v === null || v === undefined) v = cfg[key] || "";
    return OPTIONS[key].indexOf(v) > -1 ? v : "";
  }

  function applyTheme(t) {
    ["theme", "accent", "type"].forEach(function (k) {
      if (t[k]) root.setAttribute("data-mh-" + k, t[k]);
      else root.removeAttribute("data-mh-" + k);
    });
    if (FONTS[t.type] && !doc.getElementById("mh-font-" + t.type)) {
      var l = doc.createElement("link");
      l.id = "mh-font-" + t.type;
      l.rel = "stylesheet";
      l.href = FONTS[t.type];
      doc.head.appendChild(l);
    }
  }

  var theme = { theme: pick("theme"), accent: pick("accent"), type: pick("type") };
  applyTheme(theme);
  root.classList.add("mh-js");

  /* ---------- helpers ---------- */
  function onReady(fn) {
    if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", fn, { once: true });
    else fn();
  }
  function each(sel, fn, scope) {
    Array.prototype.forEach.call((scope || doc).querySelectorAll(sel), fn);
  }
  function once(el, flag) {
    if (el["__mh_" + flag]) return false;
    el["__mh_" + flag] = true;
    return true;
  }

  /* ---------- 2. REVEAL ---------- */
  var io = ("IntersectionObserver" in window) && !reduce
    ? new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          e.target.classList.add("is-in");
          io.unobserve(e.target);
        });
      }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" })
    : null;

  function initReveal(scope) {
    each("[data-reveal-group]", function (g) {
      Array.prototype.forEach.call(g.children, function (c, i) {
        if (!c.hasAttribute("data-reveal")) c.setAttribute("data-reveal", "");
        c.style.setProperty("--i", Math.min(i, 6));
      });
    }, scope);
    each("[data-reveal]", function (el) {
      if (!once(el, "rev")) return;
      if (io) io.observe(el);
      else el.classList.add("is-in");
    }, scope);
  }

  /* ---------- 3. PAIN PICKER ---------- */
  function initPick(scope) {
    each("[data-mh-pickset]", function (set) {
      if (!once(set, "pick")) return;
      var answer = set.querySelector("[data-mh-pick-answer]");
      var count = set.querySelector("[data-mh-pick-count]");
      set.addEventListener("click", function (ev) {
        var b = ev.target.closest("[data-mh-pick]");
        if (!b) return;
        b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true");
        var n = set.querySelectorAll('[data-mh-pick][aria-pressed="true"]').length;
        if (count) count.textContent = n.toLocaleString("ar-EG");
        if (answer) answer.classList.toggle("is-on", n > 0);
      });
    }, scope);
  }

  /* ---------- 4. TRY-IT EXERCISE ---------- */
  function initTry(scope) {
    each("[data-mh-try]", function (box) {
      if (!once(box, "try")) return;
      var qs = [];
      each("[data-mh-q]", function (q) { qs.push({ q: q.textContent.trim(), src: q.getAttribute("data-mh-q") }); }, box);
      var qEl = box.querySelector("[data-mh-try-q]");
      var srcEl = box.querySelector("[data-mh-try-src]");
      var ta = box.querySelector("textarea");
      var done = box.querySelector("[data-mh-try-done]");
      var next = box.querySelector("[data-mh-try-next]");
      var i = 0;
      if (next && qs.length) {
        next.addEventListener("click", function () {
          i = (i + 1) % qs.length;
          qEl.textContent = qs[i].q;
          if (srcEl) srcEl.textContent = qs[i].src;
          if (ta) { ta.value = ""; ta.focus(); }
          if (done) done.classList.remove("is-on");
        });
      }
      if (ta && done) {
        ta.addEventListener("input", function () {
          if (ta.value.trim().length >= 25) done.classList.add("is-on");
        });
      }
    }, scope);
  }

  /* ---------- 5. VIDEO (lazy embed + top-left PiP) ---------- */
  function embedUrl(src) {
    var m = src.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([\w-]{11})/);
    if (m) return { kind: "iframe", url: "https://www.youtube-nocookie.com/embed/" + m[1] + "?autoplay=1&rel=0&modestbranding=1&playsinline=1" };
    m = src.match(/vimeo\.com\/(?:video\/)?(\d+)/);
    if (m) return { kind: "iframe", url: "https://player.vimeo.com/video/" + m[1] + "?autoplay=1&title=0&byline=0&portrait=0" };
    return { kind: "video", url: src };
  }

  function initVideo(scope) {
    each("[data-mh-video]", function (box) {
      if (!once(box, "vid")) return;
      var frame = box.querySelector(".mh-video__frame");
      var poster = box.querySelector(".mh-video__poster");
      var close = box.querySelector(".mh-video__close");
      var src = box.getAttribute("data-mh-video");
      var closed = false;
      if (!frame || !poster || !src) return;

      function play() {
        var e = embedUrl(src), el;
        if (e.kind === "iframe") {
          el = doc.createElement("iframe");
          el.src = e.url;
          el.allow = "autoplay; fullscreen; picture-in-picture; encrypted-media";
          el.allowFullscreen = true;
          el.title = poster.getAttribute("aria-label") || "video";
        } else {
          el = doc.createElement("video");
          el.src = e.url;
          el.controls = true;
          el.autoplay = true;
          el.playsInline = true;
          el.addEventListener("ended", function () { box.classList.remove("is-floating"); closed = true; });
        }
        frame.appendChild(el);
        box.classList.add("is-playing");
        if (el.play) { var p = el.play(); if (p && p.catch) p.catch(function () {}); }
      }
      poster.addEventListener("click", play);
      poster.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); play(); }
      });
      if (close) close.addEventListener("click", function () {
        closed = true;
        box.classList.remove("is-floating");
        var v = frame.querySelector("video");
        if (v) v.pause();
        var f = frame.querySelector("iframe");
        if (f) {
          f.remove();
          box.classList.remove("is-playing");
        }
      });

      if ("IntersectionObserver" in window && box.hasAttribute("data-mh-pip")) {
        new IntersectionObserver(function (entries) {
          var e = entries[0];
          var passed = !e.isIntersecting && e.boundingClientRect.top < 0;
          box.classList.toggle("is-floating", passed && box.classList.contains("is-playing") && !closed);
        }, { threshold: 0.25 }).observe(box);
      }
    }, scope);
  }

  /* ---------- 6. STICKY BAR: visible after hero, hidden near offer ---------- */
  function initSticky() {
    var bar = doc.querySelector("[data-mh-sticky]");
    if (!bar || !once(bar, "sticky")) return;
    var ticking = false;
    function update() {
      ticking = false;
      var hero = doc.querySelector("[data-mh-hero]");
      var hides = doc.querySelectorAll("[data-mh-hide-sticky]");
      var vh = window.innerHeight;
      var passed = hero ? hero.getBoundingClientRect().bottom < 0 : window.scrollY > 700;
      var blocked = false;
      Array.prototype.forEach.call(hides, function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < vh * 0.85 && r.bottom > vh * 0.15) blocked = true;
      });
      bar.classList.toggle("is-on", passed && !blocked);
    }
    function req() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
    window.addEventListener("scroll", req, { passive: true });
    window.addEventListener("resize", req);
    update();
    setTimeout(update, 600);
  }

  /* ---------- 7. READING PROGRESS ---------- */
  function initProgress() {
    if (cfg.progress === false || doc.querySelector(".mh-progress")) return;
    var bar = doc.createElement("div");
    bar.className = "mh-progress";
    bar.setAttribute("aria-hidden", "true");
    doc.body.appendChild(bar);
    var ticking = false;
    function update() {
      ticking = false;
      var h = doc.documentElement.scrollHeight - window.innerHeight;
      bar.style.setProperty("--p", h > 0 ? Math.min(1, window.scrollY / h).toFixed(4) : 0);
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------- 8. SMOOTH ANCHORS (#mh-…) ---------- */
  function initAnchors() {
    doc.addEventListener("click", function (ev) {
      var a = ev.target.closest('a[href^="#mh-"]');
      if (!a) return;
      var t = doc.getElementById(a.getAttribute("href").slice(1));
      if (!t) return;
      ev.preventDefault();
      t.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    });
  }

  /* ---------- 9. LIGHTBOX (screenshots) ---------- */
  function initLightbox() {
    var dlg;
    doc.addEventListener("click", function (ev) {
      var a = ev.target.closest("[data-mh-zoom]");
      if (!a) return;
      var img = a.querySelector("img");
      if (!img || typeof HTMLDialogElement !== "function") return;
      ev.preventDefault();
      if (!dlg) {
        dlg = doc.createElement("dialog");
        dlg.className = "mh-lightbox";
        dlg.innerHTML = '<button type="button" aria-label="إغلاق">×</button><img alt="">';
        doc.body.appendChild(dlg);
        dlg.addEventListener("click", function (e) {
          if (e.target === dlg || e.target.tagName === "BUTTON") dlg.close();
        });
      }
      var big = dlg.querySelector("img");
      big.src = a.getAttribute("href") || img.src;
      big.alt = img.alt;
      dlg.showModal();
    });
  }

  /* ---------- 10. PALETTE LAB  (?mh-lab=1) ---------- */
  function initLab() {
    if (!labOn || doc.querySelector(".mh-lab")) return;
    store("mh-lab", "1");
    var box = doc.createElement("div");
    box.className = "mh-lab";
    function sel(key) {
      return '<label>' + key + '<select data-k="' + key + '">' +
        OPTIONS[key].map(function (o) {
          return '<option value="' + o + '"' + (theme[key] === o ? " selected" : "") + ">" + (o || "(palette default)") + "</option>";
        }).join("") + "</select></label>";
    }
    box.innerHTML =
      '<b>Palette Lab <span><button type="button" data-min title="minimize">–</button>' +
      '<button type="button" data-off title="close lab">×</button></span></b>' +
      sel("theme") + sel("accent") + sel("type") +
      '<div class="mh-lab__sw">' +
      ["--mh-deep", "--mh-brand", "--mh-support", "--mh-accent", "--mh-paper-2", "--mh-paper"].map(function (v) {
        return '<i style="background:var(' + v + ')" title="' + v + '"></i>';
      }).join("") + "</div>" +
      '<button type="button" class="mh-lab__copy">Copy config for GHL</button>';
    doc.body.appendChild(box);

    box.addEventListener("change", function (ev) {
      var k = ev.target.getAttribute("data-k");
      if (!k) return;
      theme[k] = ev.target.value;
      store("mh-" + k, theme[k] || null);
      applyTheme(theme);
    });
    box.querySelector("[data-min]").addEventListener("click", function () { box.classList.toggle("is-min"); });
    box.querySelector("[data-off]").addEventListener("click", function () {
      ["lab", "theme", "accent", "type"].forEach(function (k) { store("mh-" + k, null); });
      box.remove();
    });
    box.querySelector(".mh-lab__copy").addEventListener("click", function () {
      var out = {};
      ["theme", "accent", "type"].forEach(function (k) { if (theme[k]) out[k] = theme[k]; });
      var snippet = "window.MH_CONFIG = " + JSON.stringify(out) + ";";
      var btn = this;
      function ok() { btn.textContent = "Copied ✓"; setTimeout(function () { btn.textContent = "Copy config for GHL"; }, 1600); }
      if (navigator.clipboard) navigator.clipboard.writeText(snippet).then(ok, function () { prompt("Copy:", snippet); });
      else prompt("Copy:", snippet);
    });
  }

  /* ---------- BOOT (+ re-scan when GHL injects blocks late) ---------- */
  function scan(scope) {
    initReveal(scope);
    initPick(scope);
    initTry(scope);
    initVideo(scope);
  }

  onReady(function () {
    scan(doc);
    initSticky();
    initProgress();
    initAnchors();
    initLightbox();
    initLab();

    if ("MutationObserver" in window) {
      var pending = false;
      new MutationObserver(function () {
        if (pending) return;
        pending = true;
        setTimeout(function () { pending = false; scan(doc); initSticky(); }, 120);
      }).observe(doc.body, { childList: true, subtree: true });
    }
  });
})();
