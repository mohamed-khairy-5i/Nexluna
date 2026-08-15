/* Nexluna — shared UI behaviour (nav, theme, reveal, footer year, PWA). */
(function () {
  'use strict';
  var LOCALE = window.NexlunaLocale || {};
  var MUI = LOCALE.ui || {};
  function mtx(key, fallback) { return MUI[key] || fallback; }

  /* Week 8 client error boundary: fail visibly, locally, and without leaking details. */
  (function () {
    var reported = false;
    function showFallback() {
      if (reported || !document.body) return;
      reported = true;
      var node = document.createElement('div');
      node.className = 'client-error-banner';
      node.setAttribute('role', 'status');
      node.setAttribute('data-error-boundary', 'true');
      node.textContent = mtx('client_error', 'تعذّر إكمال جزء من الواجهة. أعد تحميل الصفحة؛ الحسابات الأساسية تعمل محليًا.');
      document.body.appendChild(node);
    }
    window.addEventListener('error', function () { showFallback(); });
    window.addEventListener('unhandledrejection', function () { showFallback(); });
    window.NexlunaErrorBoundary = { show: showFallback };
  })();

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
      themeBtn.setAttribute('aria-label', t === 'dark' ? mtx('light_mode', 'تفعيل الوضع الفاتح') : mtx('dark_mode', 'تفعيل الوضع الداكن'));
    }
  }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () { applyTheme(currentTheme() === 'dark' ? 'light' : 'dark'); });
    // render initial icon after icons script loads
    setTimeout(function () { applyTheme(currentTheme()); }, 0);
  }

  /* PWA install prompt — progressive enhancement, never blocks the app. */
  (function () {
    var installBtn = document.querySelector('[data-pwa-install]');
    var installHint = document.querySelector('[data-install-hint]');
    var deferred = null;
    var standalone = window.matchMedia && window.matchMedia('(display-mode: standalone)').matches;
    if (!installBtn || standalone) return;
    window.addEventListener('beforeinstallprompt', function (event) {
      event.preventDefault();
      deferred = event;
      installBtn.hidden = false;
      if (installHint) installHint.hidden = true;
    });
    installBtn.addEventListener('click', function () {
      if (!deferred) return;
      deferred.prompt();
      deferred.userChoice.then(function () { deferred = null; installBtn.hidden = true; }).catch(function () {});
    });
    window.addEventListener('appinstalled', function () {
      deferred = null;
      installBtn.hidden = true;
      if (installHint) installHint.hidden = true;
    });
  })();

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
