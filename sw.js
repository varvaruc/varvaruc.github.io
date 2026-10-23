/* Service worker for the Flappy PWA.
 * Only the app shell is precached; everything else stays network-only.
 */

const VERSION = 'v1';
const CACHE = 'flappy-' + VERSION;
const SHELL = [
  '/',
  '/index.html',
  '/manifest.webmanifest',
  '/icons/favicon.svg',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/maskable-512.png',
  '/icons/apple-touch-icon.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(CACHE);
      await Promise.all(
        SHELL.map((url) =>
          fetch(url, { cache: 'reload' })
            .then((res) => (res.ok ? cache.put(url, res) : null))
            .catch(() => null)
        )
      );
      await self.skipWaiting();
    })()
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)));
      await self.clients.claim();
    })()
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // Navigations: network first, cached shell when offline.
  if (req.mode === 'navigate') {
    event.respondWith(
      (async () => {
        try {
          const fresh = await fetch(req);
          if (fresh.ok && fresh.type === 'basic') {
            const cache = await caches.open(CACHE);
            cache.put('/', fresh.clone());
          }
          return fresh;
        } catch (err) {
          const hit = await caches.match('/');
          return hit || Response.error();
        }
      })()
    );
    return;
  }

  // Static assets: cache first, network fallback (no offline caching of the rest).
  event.respondWith(
    (async () => {
      const hit = await caches.match(req);
      if (hit) return hit;
      return fetch(req);
    })()
  );
});
