/* Service Worker — offline shell caching */
const CACHE_NAME = 'todo-shell-v1';
const CACHE_PREFIX = 'todo-shell-';

// Absolute pathnames served by this app shell
const SHELL_PATHNAMES = [
  '/index.html',
  '/manifest.json',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache =>
      cache.addAll(SHELL_PATHNAMES.map(p => '.' + p))
    )
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(k => k.startsWith(CACHE_PREFIX) && k !== CACHE_NAME)
          .map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const pathname = new URL(event.request.url).pathname;
  // Treat requests for the app root the same as index.html
  const normalised = (pathname.endsWith('/') ? pathname + 'index.html' : pathname);
  const isShell = SHELL_PATHNAMES.some(p => normalised.endsWith(p));

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (response.ok && response.type === 'basic' && isShell) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() =>
        caches.match('./index.html').then(fallback =>
          fallback ||
          new Response('Offline shell unavailable', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: { 'Content-Type': 'text/plain; charset=utf-8' },
          })
        )
      );
    })
  );
});
