// German Vocabulary in Context — C1 · Service Worker
// The page is fetched from the network first (so updates arrive), everything
// else from cache. Offline keeps working fully once cached.

const CACHE = 'gvic-c1-v1';
const PAGE = './German-C1-Vocabulary.html';

const ASSETS = [
  './', PAGE, './manifest.json',
  './icon-192.png', './icon-512.png', './icon-maskable-512.png'
];

const NETWORK_TIMEOUT = 3000;

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

function fetchWithTimeout(request) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('timeout')), NETWORK_TIMEOUT);
    fetch(request).then(
      resp => { clearTimeout(timer); resolve(resp); },
      err  => { clearTimeout(timer); reject(err); }
    );
  });
}

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  const isPage =
    e.request.mode === 'navigate' ||
    url.pathname.endsWith('/') ||
    url.pathname.endsWith('German-C1-Vocabulary.html');

  if (isPage) {
    e.respondWith(
      fetchWithTimeout(e.request)
        .then(resp => {
          if (resp && resp.ok) {
            const copy = resp.clone();
            caches.open(CACHE).then(c => c.put(PAGE, copy));
          }
          return resp;
        })
        .catch(() => caches.match(PAGE))
    );
    return;
  }

  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request)
        .then(resp => {
          if (resp && resp.ok) {
            const copy = resp.clone();
            caches.open(CACHE).then(c => c.put(e.request, copy));
          }
          return resp;
        })
        .catch(() => caches.match(PAGE));
    })
  );
});
