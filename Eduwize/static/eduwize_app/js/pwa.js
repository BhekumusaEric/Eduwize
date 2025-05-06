// PWA functionality for Eduwize

// Check if service workers are supported
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    // Register the service worker
    navigator.serviceWorker.register('/static/service-worker.js')
      .then(registration => {
        console.log('Service Worker registered with scope:', registration.scope);
        
        // Check for updates to the service worker
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          console.log('Service Worker update found!');
          
          newWorker.addEventListener('statechange', () => {
            console.log('Service Worker state changed:', newWorker.state);
            
            // When the new service worker is activated, show a refresh notification
            if (newWorker.state === 'activated' && !navigator.serviceWorker.controller) {
              // First-time installation
              console.log('Service Worker installed for the first time');
              showInstallPromotion();
            } else if (newWorker.state === 'activated' && navigator.serviceWorker.controller) {
              // Update to existing service worker
              console.log('Service Worker updated');
              showUpdateNotification();
            }
          });
        });
      })
      .catch(error => {
        console.error('Service Worker registration failed:', error);
      });
      
    // Handle service worker updates
    let refreshing = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (refreshing) return;
      refreshing = true;
      console.log('Controller changed, refreshing page');
      window.location.reload();
    });
  });
}

// Function to show the install promotion
function showInstallPromotion() {
  // Check if the app is already installed
  if (window.matchMedia('(display-mode: standalone)').matches) {
    console.log('App is already installed');
    return;
  }
  
  // Create the install promotion element
  const installPromotion = document.createElement('div');
  installPromotion.className = 'install-promotion';
  installPromotion.innerHTML = `
    <div class="install-promotion-content">
      <div class="install-promotion-icon">
        <i class="fas fa-mobile-alt"></i>
      </div>
      <div class="install-promotion-text">
        <h4>Install Eduwize App</h4>
        <p>Add to your home screen for a better experience</p>
      </div>
      <div class="install-promotion-actions">
        <button id="installButton" class="btn btn-primary">Install</button>
        <button id="dismissInstallButton" class="btn btn-link">Not Now</button>
      </div>
    </div>
  `;
  
  // Add the promotion to the page
  document.body.appendChild(installPromotion);
  
  // Add event listeners
  document.getElementById('dismissInstallButton').addEventListener('click', () => {
    installPromotion.remove();
    // Remember the user's choice for a while
    localStorage.setItem('installPromptDismissed', Date.now());
  });
  
  // Handle the install button
  const installButton = document.getElementById('installButton');
  installButton.addEventListener('click', () => {
    // Show the browser's install prompt
    deferredPrompt.prompt();
    
    // Wait for the user to respond to the prompt
    deferredPrompt.userChoice.then(choiceResult => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the install prompt');
      } else {
        console.log('User dismissed the install prompt');
      }
      
      // Clear the saved prompt
      deferredPrompt = null;
      
      // Remove the promotion
      installPromotion.remove();
    });
  });
}

// Function to show update notification
function showUpdateNotification() {
  // Use the toast notification system
  if (window.showToast) {
    window.showToast('A new version is available. Refresh to update.', 'info');
  } else {
    console.log('New version available, but toast notification function not found');
  }
}

// Store the install prompt event
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent the default browser install prompt
  e.preventDefault();
  
  // Store the event for later use
  deferredPrompt = e;
  
  // Check if we should show the install promotion
  const lastDismissed = localStorage.getItem('installPromptDismissed');
  const oneWeekInMs = 7 * 24 * 60 * 60 * 1000;
  
  if (!lastDismissed || (Date.now() - lastDismissed > oneWeekInMs)) {
    // Show the install promotion after a short delay
    setTimeout(() => {
      showInstallPromotion();
    }, 3000);
  }
});

// Add styles for the install promotion
const style = document.createElement('style');
style.textContent = `
  .install-promotion {
    position: fixed;
    bottom: 20px;
    left: 20px;
    right: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 1050;
    max-width: 500px;
    margin: 0 auto;
    animation: slideUp 0.3s ease-out;
  }
  
  .install-promotion-content {
    display: flex;
    align-items: center;
    padding: 16px;
  }
  
  .install-promotion-icon {
    font-size: 24px;
    color: #4e73df;
    margin-right: 16px;
  }
  
  .install-promotion-text {
    flex: 1;
  }
  
  .install-promotion-text h4 {
    margin: 0 0 4px 0;
    font-size: 16px;
  }
  
  .install-promotion-text p {
    margin: 0;
    font-size: 14px;
    color: #6c757d;
  }
  
  .install-promotion-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  
  @keyframes slideUp {
    from {
      transform: translateY(100%);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
  
  @media (max-width: 576px) {
    .install-promotion {
      bottom: 0;
      left: 0;
      right: 0;
      border-radius: 8px 8px 0 0;
    }
  }
`;

document.head.appendChild(style);

// Register for push notifications
function registerForPushNotifications() {
  if ('Notification' in window && 'PushManager' in window) {
    Notification.requestPermission().then(permission => {
      if (permission === 'granted') {
        console.log('Notification permission granted');
        subscribeToPushNotifications();
      } else {
        console.log('Notification permission denied');
      }
    });
  }
}

// Subscribe to push notifications
function subscribeToPushNotifications() {
  navigator.serviceWorker.ready.then(registration => {
    // Check if we already have a subscription
    registration.pushManager.getSubscription().then(subscription => {
      if (subscription) {
        console.log('User is already subscribed to push notifications');
        return subscription;
      }
      
      // Get the server's public key
      return fetch('/api/push-public-key/')
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to get public key');
          }
          return response.json();
        })
        .then(data => {
          const publicKey = data.publicKey;
          const applicationServerKey = urlBase64ToUint8Array(publicKey);
          
          // Subscribe the user
          return registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: applicationServerKey
          });
        })
        .then(subscription => {
          // Send the subscription to the server
          return fetch('/api/push-subscribe/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              subscription: subscription.toJSON()
            })
          });
        })
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to subscribe');
          }
          console.log('User subscribed to push notifications');
        })
        .catch(error => {
          console.error('Failed to subscribe to push notifications:', error);
        });
    });
  });
}

// Helper function to convert base64 to Uint8Array
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, '+')
    .replace(/_/g, '/');
  
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  
  return outputArray;
}
