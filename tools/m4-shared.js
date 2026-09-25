/* =====================================================================
   M4 · BLOCK 00B — SHARED JAVASCRIPT
   One script for the whole page (replaces the 25 per-block scripts).
     1. motion     — soft scroll entrance for .m4-reveal (never hides
                     anything on screen or already passed; off in the GHL
                     editor/preview iframe and with reduced motion)
     2. faq        — accordion for #m4-faq
     3. sticky     — show/hide the fixed bar + back-to-top + FAQ link
     4. masonry    — photo gallery rows in #m4-kareem
   Optional:  window.M4_CONFIG = { motion: false }  (before this script)
              or add ?m4-motion=0 to the URL to switch the entrance off.
   ===================================================================== */
(function () {
  "use strict";
  if (window.__M4_SHARED__) return;
  window.__M4_SHARED__ = true;

  var doc = document;
  var root = doc.documentElement;
  var cfg = window.M4_CONFIG || {};
  root.classList.add("m4-js");

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var inFrame = (function () { try { return window.self !== window.top; } catch (e) { return true; } })();
  var motionOn = cfg.motion !== false &&
    !/[?&]m4-motion=0\b/.test(location.search) &&
    !reduceMotion && !inFrame && "requestAnimationFrame" in window;

  function ready(fn) {
    if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", fn, { once: true });
    else fn();
  }
  function each(list, fn) { Array.prototype.forEach.call(list, fn); }
  function smooth() { return reduceMotion ? "auto" : "smooth"; }


  /* ---------------- 1 · MOTION ----------------
     Elements below the screen are "armed" (transparent). A light, rAF-throttled
     scroll check reveals every armed element that has reached the screen OR
     has already been scrolled past — so a fast scroll, an anchor jump or the
     sticky-bar FAQ link can never leave anything hidden. */
  var armed = [];
  var checking = false;

  function revealDue() {
    checking = false;
    if (!armed.length) return;
    var line = window.innerHeight * 0.94;
    // at the very bottom of the page everything left is due
    if (window.scrollY + window.innerHeight >= doc.documentElement.scrollHeight - 4) line = Infinity;
    var perParent = new Map();
    armed = armed.filter(function (el) {
      if (el.getBoundingClientRect().top >= line) return true;
      var n = perParent.get(el.parentNode) || 0;
      perParent.set(el.parentNode, n + 1);
      el.style.setProperty("--m4-i", Math.min(n, 5));
      el.classList.remove("is-armed");
      el.classList.add("is-revealed");
      return false;
    });
  }
  function requestReveal() {
    if (checking) return;
    checking = true;
    requestAnimationFrame(revealDue);
  }

  function armReveals() {
    if (!motionOn) return;
    root.classList.add("m4-motion");
    var fold = window.innerHeight;
    each(doc.querySelectorAll(".m4-reveal:not([data-m4-seen])"), function (el) {
      el.setAttribute("data-m4-seen", "");
      var r = el.getBoundingClientRect();
      // only animate what the visitor has not seen yet (below the screen)
      if (r.top < fold || r.height === 0) return;
      el.classList.add("is-armed");
      armed.push(el);
    });
  }

  if (motionOn) {
    window.addEventListener("scroll", requestReveal, { passive: true });
    window.addEventListener("resize", requestReveal);
  }
  // printing never leaves anything hidden
  window.addEventListener("beforeprint", function () {
    armed.forEach(function (el) { el.classList.remove("is-armed"); });
    armed = [];
  });


  /* ---------------- 2 · FAQ ---------------- */
  function initFaq() {
    var faq = doc.getElementById("m4-faq");
    if (!faq || faq.__m4) return;
    faq.__m4 = true;
    faq.addEventListener("click", function (ev) {
      var btn = ev.target.closest(".m4-faq__question");
      if (!btn || !faq.contains(btn)) return;
      var item = btn.closest(".m4-faq__item");
      if (!item) return;
      var wasOpen = item.classList.contains("is-open");
      each(faq.querySelectorAll(".m4-faq__item.is-open"), function (other) {
        other.classList.remove("is-open");
        var b = other.querySelector(".m4-faq__question");
        if (b) b.setAttribute("aria-expanded", "false");
      });
      if (!wasOpen) {
        item.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  }


  /* ---------------- 3 · STICKY BAR ---------------- */
  function initSticky() {
    var host = doc.querySelector(".m4-sticky-host, .mhh-sticky-cta");
    var bar = doc.querySelector(".m4-sticky__action-bar");
    if (!host || !bar || host.__m4) return;
    host.__m4 = true;

    var backTop = bar.querySelector(".m4-sticky__back-top");
    var faqLink = bar.querySelector(".m4-sticky__float-faq");
    var ticking = false;
    var goingUp = false;

    function update() {
      ticking = false;
      // the bar appears once the whole hero (text, video, button, trust row) is behind us
      var hero = doc.getElementById("m4-hero-trust") || doc.getElementById("m4-hero");
      var offer = doc.getElementById("m4-offer");
      var passed = hero ? hero.getBoundingClientRect().bottom <= 0 : window.scrollY > 650;
      var offerOnScreen = false;
      if (offer) {
        var r = offer.getBoundingClientRect();
        offerOnScreen = r.top < window.innerHeight * .88 && r.bottom > window.innerHeight * .12;
      }
      var show = passed && !offerOnScreen;
      host.classList.toggle("is-visible", show);
      if (backTop) backTop.classList.toggle("is-visible", show && window.scrollY > 650 && !goingUp);
    }
    function request() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    }

    if (backTop) {
      backTop.addEventListener("click", function (ev) {
        ev.preventDefault();
        goingUp = true;
        backTop.classList.remove("is-visible");
        window.scrollTo({ top: 0, behavior: smooth() });
        setTimeout(function () { goingUp = false; request(); }, 900);
      });
    }
    if (faqLink) {
      faqLink.addEventListener("click", function (ev) {
        var faq = doc.getElementById("m4-faq");
        if (!faq) return;
        ev.preventDefault();
        faq.scrollIntoView({ behavior: smooth(), block: "start" });
      });
    }

    window.addEventListener("scroll", request, { passive: true });
    window.addEventListener("resize", request);
    window.addEventListener("orientationchange", request);
    update();
    setTimeout(update, 250);
    setTimeout(update, 900);
  }


  /* ---------------- 4 · MASONRY (#m4-kareem gallery) ---------------- */
  function initMasonry() {
    var gallery = doc.querySelector("#m4-kareem .m4-kareem__gallery");
    if (!gallery || gallery.__m4) return;
    gallery.__m4 = true;
    var items = gallery.querySelectorAll(".m4-kareem__event");
    var timer;

    function size(item) {
      var img = item.querySelector("img");
      if (!img || !img.complete || !img.naturalWidth) return;
      var cs = getComputedStyle(gallery);
      var row = parseFloat(cs.gridAutoRows) || 6;
      var gap = parseFloat(cs.rowGap) || 10;
      item.style.gridRowEnd = "auto";
      var h = img.getBoundingClientRect().height;
      item.style.gridRowEnd = "span " + Math.ceil((h + gap) / (row + gap));
    }
    function sizeAll() { each(items, size); }

    each(items, function (item) {
      var img = item.querySelector("img");
      if (!img) return;
      if (img.complete) size(item);
      else img.addEventListener("load", function () { size(item); }, { once: true });
    });
    window.addEventListener("resize", function () {
      clearTimeout(timer);
      timer = setTimeout(sizeAll, 100);
    });
    [150, 600, 1200].forEach(function (t) { setTimeout(sizeAll, t); });
  }


  /* ---------------- BOOT ---------------- */
  function boot() {
    armReveals();
    initFaq();
    initSticky();
    initMasonry();
  }

  ready(function () {
    boot();
    // GHL can render blocks late — pick them up once more
    window.addEventListener("load", boot, { once: true });
  });
})();
