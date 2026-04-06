// ProTrader Suite — Service Worker v5
// Cache pour fonctionnement hors ligne (PWA Android)

const CACHE = 'protrader-v5';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './android/icon-192.png',
  './android/icon-512.png',
];

// Installation — mise en cache des ressources
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// Activation — nettoyage anciens caches
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch — stratégie Network First (données fraîches prioritaires)
self.addEventListener('fetch', e => {
  // Ignorer les requêtes API externes (Binance, AllSports)
  if (e.request.url.includes('api.') || e.request.url.includes('allsports')) {
    return;
  }
  e.respondWith(
    fetch(e.request)
      .then(resp => {
        const clone = resp.clone();
        caches.open(CACHE).then(cache => cache.put(e.request, clone));
        return resp;
      })
      .catch(() => caches.match(e.request))
  );
});
