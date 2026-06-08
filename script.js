/* ClinOmicsAI — site interactions */
(function(){
  "use strict";

  // ── Mobile nav toggle
  var nav = document.getElementById("nav");
  var toggle = document.getElementById("navToggle");
  if (toggle) {
    toggle.addEventListener("click", function(){
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
    document.querySelectorAll(".nav__links a, .nav__cta").forEach(function(a){
      a.addEventListener("click", function(){
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded","false");
      });
    });
  }

  // ── Sticky-nav style switch on scroll
  var onScroll = function(){
    if (!nav) return;
    nav.classList.toggle("is-stuck", window.scrollY > 12);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // ── Scroll-reveal (one-shot)
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en, i){
        if (en.isIntersecting) {
          setTimeout(function(){ en.target.classList.add("is-in"); }, Math.min(i*60, 240));
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach(function(el){ io.observe(el); });
  } else {
    revealEls.forEach(function(el){ el.classList.add("is-in"); });
  }

  // ── Smooth-scroll offset for sticky nav
  document.querySelectorAll('a[href^="#"]').forEach(function(a){
    a.addEventListener("click", function(e){
      var hash = a.getAttribute("href");
      if (hash === "#" || hash.length < 2) return;
      var target = document.querySelector(hash);
      if (!target) return;
      e.preventDefault();
      var navH = nav ? nav.offsetHeight : 0;
      var y = target.getBoundingClientRect().top + window.scrollY - navH + 1;
      window.scrollTo({ top: y, behavior: "smooth" });
    });
  });

  // ── Partner form — basic client-side validation + friendly fallback
  var form = document.getElementById("partnerForm");
  var statusEl = document.getElementById("formStatus");
  if (!form) return;

  var RE_EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var fieldOf = function(input){ return input.closest(".field"); };
  var setErr = function(input, msg){
    var f = fieldOf(input);
    if (!f) return;
    f.classList.add("is-invalid");
    var slot = f.querySelector("[data-error]");
    if (slot) slot.textContent = msg;
  };
  var clearErr = function(input){
    var f = fieldOf(input);
    if (!f) return;
    f.classList.remove("is-invalid");
    var slot = f.querySelector("[data-error]");
    if (slot) slot.textContent = "";
  };

  var validate = function(){
    var ok = true;
    var n = form.elements.name;
    var e = form.elements.email;
    if (n && !n.value.trim()) { setErr(n, "Please share your name."); ok = false; }
    if (e) {
      if (!e.value.trim()) { setErr(e, "Email is required so we can reply."); ok = false; }
      else if (!RE_EMAIL.test(e.value.trim())) { setErr(e, "That email doesn't look right."); ok = false; }
    }
    return ok;
  };

  ["name","email","message"].forEach(function(k){
    var el = form.elements[k];
    if (el) el.addEventListener("input", function(){ clearErr(el); });
  });

  var show = function(text, kind){
    if (!statusEl) return;
    statusEl.textContent = text;
    statusEl.className = "pform__status is-visible " + (kind === "ok" ? "is-ok" : "is-error");
  };

  form.addEventListener("submit", function(ev){
    ev.preventDefault();
    if (!validate()) { show("Please fix the highlighted fields and try again.", "error"); return; }
    // No backend wired in this template — show a confirmation message and reset the form.
    // (When a backend is connected, send the form data here instead.)
    show("Thanks — your message has been received. We'll reply within 1–2 business days.", "ok");
    form.reset();
  });
})();
