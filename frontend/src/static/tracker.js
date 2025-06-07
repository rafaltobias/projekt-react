/**
 * Visit Tracker - Automatic website visitor tracking script
 * With Tag Manager integration for custom events and actions
 * Includes consent management for data sharing
 */
(function() {
  // Configuration
  const API_ENDPOINT = 'http://localhost:5000/api/track';
  const TAGS_ENDPOINT = 'http://localhost:5000/api/tags';
  const SESSION_STORAGE_KEY = 'visitor_tracker_session_id';
  const CONSENT_KEY = 'data_sharing_consent';

  // Consent check function
  function hasConsent() {
    const consent = localStorage.getItem(CONSENT_KEY);
    return consent === 'granted';
  }

  // Check if tracking is allowed
  function isTrackingAllowed() {
    return hasConsent();
  }
  
  // Utility functions
  function generateSessionId() {
    // Generate a random session ID
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0;
      return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
  }
  
  function getSessionId() {
    // Get or create a session ID
    let sessionId = sessionStorage.getItem(SESSION_STORAGE_KEY);
    if (!sessionId) {
      sessionId = generateSessionId();
      sessionStorage.setItem(SESSION_STORAGE_KEY, sessionId);
    }
    return sessionId;
  }
  
  // Browser detection
  function detectBrowser() {
    const userAgent = navigator.userAgent;
    let browser = "Unknown";
    
    if (userAgent.indexOf("Firefox") > -1) {
      browser = "Firefox";
    } else if (userAgent.indexOf("SamsungBrowser") > -1) {
      browser = "Samsung Browser";
    } else if (userAgent.indexOf("Opera") > -1 || userAgent.indexOf("OPR") > -1) {
      browser = "Opera";
    } else if (userAgent.indexOf("Edge") > -1 || userAgent.indexOf("Edg") > -1) {
      browser = "Edge";
    } else if (userAgent.indexOf("Chrome") > -1) {
      browser = "Chrome";
    } else if (userAgent.indexOf("Safari") > -1) {
      browser = "Safari";
    } else if (userAgent.indexOf("MSIE") > -1 || userAgent.indexOf("Trident") > -1) {
      browser = "Internet Explorer";
    }
    
    return browser;
  }
  
  // OS detection
  function detectOS() {
    const userAgent = navigator.userAgent;
    let os = "Unknown";
    
    if (userAgent.indexOf("Windows NT 10.0") > -1) os = "Windows 10";
    else if (userAgent.indexOf("Windows NT 6.3") > -1) os = "Windows 8.1";
    else if (userAgent.indexOf("Windows NT 6.2") > -1) os = "Windows 8";
    else if (userAgent.indexOf("Windows NT 6.1") > -1) os = "Windows 7";
    else if (userAgent.indexOf("Windows NT") > -1) os = "Windows";
    else if (/iPhone|iPad|iPod/.test(userAgent)) os = "iOS";
    else if (userAgent.indexOf("Android") > -1) os = "Android";
    else if (userAgent.indexOf("Mac") > -1) os = "macOS";
    else if (userAgent.indexOf("Linux") > -1) os = "Linux";
    
    return os;
  }
  
  // Device detection
  function detectDevice() {
    if (/Mobi|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
      if (/iPad|Tablet|Android(?!.*Mobile)/i.test(navigator.userAgent)) {
        return 'Tablet';
      } else {
        return 'Mobile';
      }
    } else {
      return 'Desktop';
    }
  }
    // Visit tracker
  function trackVisit(isEntryPage = false) {
    // Check if tracking is allowed
    if (!isTrackingAllowed()) {
      console.debug('Tracking skipped - no consent granted');
      return;
    }

    try {
      const sessionId = getSessionId();
      const browser = detectBrowser();
      const os = detectOS();
      const device = detectDevice();
      
      // Collect data
      const visitData = {
        page_url: window.location.href,
        referrer: document.referrer,
        browser: browser,
        os: os,
        device: device,
        session_id: sessionId,
        is_entry_page: isEntryPage,
        is_exit_page: false
      };
      
      // Send data to backend
      fetch(API_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(visitData)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.debug('Visit tracking successful', data);
      })
      .catch(error => {
        console.error('Error sending tracking data:', error);
      });
    } catch (error) {
      console.error('Error in tracking visit:', error);
    }
  }
    // Track exit page
  function trackExitPage() {
    // Check if tracking is allowed
    if (!isTrackingAllowed()) {
      console.debug('Exit page tracking skipped - no consent granted');
      return;
    }

    try {
      const sessionId = sessionStorage.getItem(SESSION_STORAGE_KEY);
      if (sessionId) {
        // Collect data
        const visitData = {
          page_url: window.location.href,
          session_id: sessionId,
          is_entry_page: false,
          is_exit_page: true
        };
        
        // Use the sendBeacon API which continues to work even when the page is unloading
        if (navigator.sendBeacon) {
          const headers = new Headers();
          headers.append('Content-Type', 'application/json');
          const blob = new Blob([JSON.stringify(visitData)], { type: 'application/json' });
          navigator.sendBeacon(API_ENDPOINT, blob);
        } else {
          // Fallback for browsers that don't support sendBeacon
          fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(visitData),
            keepalive: true
          }).catch(() => {});
        }
      }
    } catch (error) {
      console.error('Error in tracking exit page:', error);
    }
  }

  // Check if this is an entry page (first page of the session)
  const isNewSession = !sessionStorage.getItem(SESSION_STORAGE_KEY);
  
  // Track the current visit
  trackVisit(isNewSession);
  
  // Set up event listeners
  window.addEventListener('beforeunload', trackExitPage);
  window.addEventListener('pagehide', trackExitPage);
    // Track page visibility changes (when user switches tabs or minimizes browser)
  document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden') {
      // Check if tracking is allowed
      if (!isTrackingAllowed()) {
        console.debug('Visibility tracking skipped - no consent granted');
        return;
      }

      const visitData = {
        page_url: window.location.href,
        session_id: getSessionId(),
        is_entry_page: false,
        is_exit_page: true
      };
      
      // Use sendBeacon for more reliable delivery when page is unloading
      if (navigator.sendBeacon) {
        const blob = new Blob([JSON.stringify(visitData)], { type: 'application/json' });
        navigator.sendBeacon(API_ENDPOINT, blob);
      }
    }
  });
    // Expose the tracker API
  window.VisitTracker = {
    trackEvent: function(eventName, eventData) {
      // Check if tracking is allowed
      if (!isTrackingAllowed()) {
        console.debug('Event tracking skipped - no consent granted');
        return;
      }

      try {
        const sessionId = getSessionId();
        const visitData = {
          page_url: window.location.href,
          session_id: sessionId,
          is_entry_page: false,
          is_exit_page: false,
          event_name: eventName,
          event_data: eventData
        };
        
        fetch(API_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(visitData)
        })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          console.debug('Event tracking successful', data);
        })
        .catch(error => {
          console.error('Error sending event data:', error);
        });
      } catch (error) {
        console.error('Error in tracking event:', error);
      }
    },
    
    getSessionId: function() {
      return getSessionId();
    },
      getBrowserInfo: function() {
      return {
        browser: detectBrowser(),
        os: detectOS(),
        device: detectDevice(),
        userAgent: navigator.userAgent
      };
    }
  };
  
  // Tag Manager Functionality
  const TagManager = {
    tags: [],
    initialized: false,
    
    // Initialize the tag manager
    init: async function() {
      if (this.initialized) return;
      
      try {
        await this.loadTags();
        this.setupEventListeners();
        this.initialized = true;
        console.log('Tag Manager initialized successfully');
      } catch (error) {
        console.error('Failed to initialize Tag Manager:', error);
      }
    },
    
    // Load tags from API
    loadTags: async function() {
      try {
        const response = await fetch(TAGS_ENDPOINT);
        const data = await response.json();
        this.tags = data || [];
        console.log(`Loaded ${this.tags.length} tags`);
      } catch (error) {
        console.error('Failed to load tags:', error);
        this.tags = [];
      }
    },
    
    // Set up tag event listeners
    setupEventListeners: function() {
      this.executeTags('page_view');
      this.executeTags('all_pages');
      
      // Set up click listeners
      this.tags.forEach(tag => {
        let trigger = tag.trigger;
        
        try {
          // Try to parse JSON if it's a string
          if (typeof trigger === 'string' && trigger.startsWith('{')) {
            trigger = JSON.parse(trigger);
          }
        } catch (e) {
          console.error('Error parsing trigger:', e);
        }
        
        // Handle click triggers
        if ((typeof trigger === 'object' && trigger.type === 'click' && trigger.target) || 
            trigger === 'click') {
          
          const selector = typeof trigger === 'object' ? trigger.target : '';
          if (!selector) return;
          
          setTimeout(() => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(el => {
              // Prevent adding duplicate listeners
              if (!el.dataset.tagClickListener) {
                el.addEventListener('click', (event) => {
                  event.stopPropagation();
                  this.executeTag(tag);
                });
                el.dataset.tagClickListener = "1";
              }
            });
          }, 500); // Small delay to ensure DOM is ready
        }
      });
    },
    
    // Execute all tags with a specific trigger
    executeTags: function(triggerType) {
      this.tags.forEach(tag => {
        let trigger = tag.trigger;
        
        try {
          // Try to parse JSON if it's a string
          if (typeof trigger === 'string' && trigger.startsWith('{')) {
            trigger = JSON.parse(trigger);
          }
        } catch (e) {
          // Silently handle parse error
        }
        
        if ((typeof trigger === 'object' && trigger.type === triggerType) || 
            trigger === triggerType) {
          this.executeTag(tag);
        }
      });
    },
    
    // Execute a single tag's action
    executeTag: function(tag) {
      let config = {};
      
      try {
        // Try to parse config if it's a string
        if (typeof tag.config === 'string') {
          config = JSON.parse(tag.config);
        } else if (typeof tag.config === 'object') {
          config = tag.config;
        }
      } catch (e) {
        console.error('Error parsing tag config:', e);
        return;
      }
      
      // Skip if no action defined
      if (!config.action) return;
      
      // Execute the appropriate action
      switch (config.action) {
        case 'alert':
          alert(config.value || 'Alert!');
          break;
        
        case 'log':
          console.log('[Tag Manager]', config.value || 'Log event');
          break;
        
        case 'redirect':
          if (config.value) {
            window.location.href = config.value;
          }
          break;
        
        default:
          // No matching action type
          break;
      }
    }
  };
  
  // Initialize the Tag Manager
  TagManager.init();
  
  // Expose Tag Manager
  window.VisitTracker.TagManager = TagManager;
})();
