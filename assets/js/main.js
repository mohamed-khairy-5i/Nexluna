/* Nexluna — shared UI behaviour (nav, theme, reveal, footer year, PWA). */
(function () {
  'use strict';

  /* Mobile nav */
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    links.addEventListener('click', function (e) { if (e.target.closest('a')) { links.classList.remove('open'); toggle.setAttribute('aria-expanded', 'false'); } });
  }

  /* Theme toggle */
  var themeBtn = document.querySelector('[data-theme-toggle]');
  function currentTheme() { return document.documentElement.getAttribute('data-theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'); }
  function icon(name) { return window.NexIcons ? window.NexIcons.get(name) : ''; }
  function applyTheme(t) {
    document.documentElement.setAttribute('data-theme', t);
    try { localStorage.setItem('nx-theme', t); } catch (e) {}
    if (themeBtn) {
      themeBtn.innerHTML = icon(t === 'dark' ? 'sun' : 'moon');
      themeBtn.setAttribute('aria-label', t === 'dark' ? 'تفعيل الوضع الفاتح' : 'تفعيل الوضع الداكن');
    }
  }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () { applyTheme(currentTheme() === 'dark' ? 'light' : 'dark'); });
    // render initial icon after icons script loads
    setTimeout(function () { applyTheme(currentTheme()); }, 0);
  }

  /* Scroll reveal — reveal-in-viewport items immediately, observe the rest */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.08, rootMargin: '0px 0px -6% 0px' });
    reveals.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.95) { el.classList.add('in'); } // already visible on load
      else { io.observe(el); }
    });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  /* Footer year */
  var y = document.querySelector('[data-year]');
  if (y) y.textContent = new Date().getFullYear();

  /* Service worker */
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () { navigator.serviceWorker.register('/sw.js').catch(function () {}); });
  }
})();
