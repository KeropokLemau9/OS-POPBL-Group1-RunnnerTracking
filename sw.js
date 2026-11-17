// RunTogether Service Worker v1.0
const CACHE_NAME = 'runtogether-cache-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg'
];

// Install: Simpan aset penting ke cache
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[Service Worker] Memasang aset offline...');
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// Activate: Bersihkan cache lama
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Cuba rangkaian dahulu, jika offline gunakan cache
self.addEventListener('fetch', event => {
  // Hanya proses permohonan HTTP/HTTPS GET
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Jika respons sah, simpan salinan dalam cache
        if (response && response.status === 200 && response.type === 'basic') {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return response;
      })
      .catch(() => {
        // Jika tiada internet, guna aset cache
        return caches.match(event.request).then(cachedResponse => {
          if (cachedResponse) return cachedResponse;
          // Fallback kepada index.html untuk navigasi SPA/PWA
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
        });
      })
  );
});
