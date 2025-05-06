// Service Worker for Eduwize PWA
const CACHE_NAME = 'eduwize-cache-v1';
const OFFLINE_URL = '/offline/';
const OFFLINE_IMG = '/static/eduwize_app/images/offline.svg';

// Assets to cache immediately when the service worker is installed
const PRECACHE_ASSETS = [
  '/',
  '/offline/',
  OFFLINE_IMG,
  '/static/manifest.json',
  '/static/eduwize_app/css/styles.css',
  '/static/eduwize_app/js/main.js',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&display=swap'
];

// Install event - precache key resources
self.addEventListener('install', event => {
  console.log('[Service Worker] Installing Service Worker...');
  
  // Skip waiting to ensure the new service worker activates immediately
  self.skipWaiting();
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[Service Worker] Precaching App Shell');
        return cache.addAll(PRECACHE_ASSETS);
      })
      .catch(error => {
        console.error('[Service Worker] Precaching failed:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('[Service Worker] Activating Service Worker...');
  
  // Claim clients to ensure the service worker takes control immediately
  event.waitUntil(self.clients.claim());
  
  // Remove old caches
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Removing old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Helper function to determine if a request is an API call
const isApiRequest = request => {
  const url = new URL(request.url);
  return url.pathname.startsWith('/api/');
};

// Helper function to determine if a request is for an image
const isImageRequest = request => {
  return request.destination === 'image';
};

// Helper function to determine if a request is for a static asset
const isStaticAsset = request => {
  const url = new URL(request.url);
  return url.pathname.startsWith('/static/') || 
         url.pathname.startsWith('/media/');
};

// Helper function to determine if a request is for an HTML page
const isHtmlPageRequest = request => {
  return request.mode === 'navigate' || 
         (request.method === 'GET' && 
          request.headers.get('accept').includes('text/html'));
};

// Fetch event - handle network requests
self.addEventListener('fetch', event => {
  const request = event.request;
  
  // Skip cross-origin requests
  if (!request.url.startsWith(self.location.origin) && 
      !request.url.startsWith('https://cdn.jsdelivr.net') && 
      !request.url.startsWith('https://cdnjs.cloudflare.com') && 
      !request.url.startsWith('https://fonts.googleapis.com')) {
    return;
  }
  
  // Different strategies based on request type
  if (isApiRequest(request)) {
    // Network-first strategy for API requests
    event.respondWith(networkFirstStrategy(request));
  } else if (isImageRequest(request)) {
    // Cache-first strategy for images with offline fallback
    event.respondWith(cacheFirstWithOfflineFallback(request));
  } else if (isStaticAsset(request)) {
    // Cache-first strategy for static assets
    event.respondWith(cacheFirst(request));
  } else if (isHtmlPageRequest(request)) {
    // Network-first strategy for HTML pages with offline fallback
    event.respondWith(networkFirstWithOfflineFallback(request));
  } else {
    // Stale-while-revalidate for everything else
    event.respondWith(staleWhileRevalidate(request));
  }
});

// Network-first strategy
async function networkFirstStrategy(request) {
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    // Clone the response before caching it
    const responseToCache = networkResponse.clone();
    
    // Cache the response for future use
    caches.open(CACHE_NAME).then(cache => {
      cache.put(request, responseToCache);
    });
    
    return networkResponse;
  } catch (error) {
    // If network fails, try cache
    console.log('[Service Worker] Network request failed, getting from cache:', request.url);
    const cachedResponse = await caches.match(request);
    return cachedResponse || new Response('Network error happened', {
      status: 408,
      headers: { 'Content-Type': 'text/plain' }
    });
  }
}

// Cache-first strategy
async function cacheFirst(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const networkResponse = await fetch(request);
    
    // Cache the response for future use
    const responseToCache = networkResponse.clone();
    caches.open(CACHE_NAME).then(cache => {
      cache.put(request, responseToCache);
    });
    
    return networkResponse;
  } catch (error) {
    console.error('[Service Worker] Fetch failed:', error);
    return new Response('Network error happened', {
      status: 408,
      headers: { 'Content-Type': 'text/plain' }
    });
  }
}

// Cache-first with offline fallback for images
async function cacheFirstWithOfflineFallback(request) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const networkResponse = await fetch(request);
    
    // Cache the response for future use
    const responseToCache = networkResponse.clone();
    caches.open(CACHE_NAME).then(cache => {
      cache.put(request, responseToCache);
    });
    
    return networkResponse;
  } catch (error) {
    console.log('[Service Worker] Image fetch failed, using offline image');
    return caches.match(OFFLINE_IMG);
  }
}

// Network-first with offline fallback for HTML pages
async function networkFirstWithOfflineFallback(request) {
  try {
    const networkResponse = await fetch(request);
    
    // Cache the response for future use
    const responseToCache = networkResponse.clone();
    caches.open(CACHE_NAME).then(cache => {
      cache.put(request, responseToCache);
    });
    
    return networkResponse;
  } catch (error) {
    console.log('[Service Worker] HTML fetch failed, using offline page');
    const cachedResponse = await caches.match(request);
    return cachedResponse || caches.match(OFFLINE_URL);
  }
}

// Stale-while-revalidate strategy
async function staleWhileRevalidate(request) {
  const cachedResponse = await caches.match(request);
  
  const fetchPromise = fetch(request)
    .then(networkResponse => {
      caches.open(CACHE_NAME).then(cache => {
        cache.put(request, networkResponse.clone());
      });
      return networkResponse;
    })
    .catch(error => {
      console.error('[Service Worker] Fetch failed:', error);
    });
  
  return cachedResponse || fetchPromise;
}

// Push event - handle push notifications
self.addEventListener('push', event => {
  console.log('[Service Worker] Push Received');
  
  let data = { title: 'Eduwize Update', body: 'Something new happened!' };
  
  if (event.data) {
    data = JSON.parse(event.data.text());
  }
  
  const options = {
    body: data.body,
    icon: '/static/eduwize_app/images/icons/icon-192x192.png',
    badge: '/static/eduwize_app/images/icons/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/'
    }
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Notification click event - handle notification clicks
self.addEventListener('notificationclick', event => {
  console.log('[Service Worker] Notification click received');
  
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow(event.notification.data.url)
  );
});
