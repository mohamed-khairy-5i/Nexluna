/* Nexluna service worker — offline-first for visited pages + static assets. */
const CACHE = 'nexluna-v6';
const CORE = [
  '/',
  '/index.html',
  '/offline.html',
  '/assets/css/style.css',
  '/assets/js/icons.js',
  '/assets/js/main.js',
  '/assets/js/smartsearch.js',
  '/assets/js/units.generated.js',
  '/assets/js/locale.en.generated.js',
  '/assets/js/explain.js',
  '/assets/js/webmcp.js',
  '/assets/js/converter.js',
  '/assets/js/embed.js',
  '/embed.html',
  '/assets/img/logo.svg',
  '/assets/img/icon-192.png',
  '/manifest.webmanifest',
  '/en/',
  '/en/index.html',
  '/en/converters/index.html'
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Never cache cross-origin (ads/fonts) — let the network handle them.
  if (url.origin !== self.location.origin) return;

  // HTML: network-first, fall back to cache, then offline page.
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
    e.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then((r) => r || caches.match('/offline.html')))
    );
    return;
  }

  // Static assets: cache-first.
  e.respondWith(
    caches.match(req).then((cached) => cached || fetch(req).then((res) => {
      const copy = res.clone();
      caches.open(CACHE).then((c) => c.put(req, copy));
      return res;
    }).catch(() => cached))
  );
});
