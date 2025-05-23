/**
 * Web Analytics Tracking Script
 * This script should be included on websites that want to be tracked
 */

(function() {
    'use strict';
    
    // Configuration
    const config = {
        apiUrl: 'http://localhost:5000/api', // Flask backend URL
        trackPageViews: true,
        trackClicks: true,
        trackErrors: false,
        debug: false
    };
    
    // Utility functions
    function log(message, data = null) {
        if (config.debug) {
            console.log('[Analytics]', message, data);
        }
    }
    
    function generateSessionId() {
        return 'sess_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
    }
    
    function getSessionId() {
        let sessionId = sessionStorage.getItem('analytics_session_id');
        if (!sessionId) {
            sessionId = generateSessionId();
            sessionStorage.setItem('analytics_session_id', sessionId);
        }
        return sessionId;
    }
    
    function detectBrowser() {
        const userAgent = navigator.userAgent;
        if (userAgent.indexOf('Chrome') > -1) return 'Chrome';
        if (userAgent.indexOf('Firefox') > -1) return 'Firefox';
        if (userAgent.indexOf('Safari') > -1 && userAgent.indexOf('Chrome') === -1) return 'Safari';
        if (userAgent.indexOf('Edge') > -1) return 'Edge';
        if (userAgent.indexOf('Opera') > -1) return 'Opera';
        return 'Unknown';
    }
    
    function detectOS() {
        const userAgent = navigator.userAgent;
        if (userAgent.indexOf('Windows') > -1) return 'Windows';
        if (userAgent.indexOf('Mac') > -1) return 'macOS';
        if (userAgent.indexOf('Linux') > -1) return 'Linux';
        if (userAgent.indexOf('Android') > -1) return 'Android';
        if (userAgent.indexOf('iOS') > -1) return 'iOS';
        return 'Unknown';
    }
    
    function detectDevice() {
        const userAgent = navigator.userAgent;
        if (/tablet|ipad|playbook|silk/i.test(userAgent)) return 'Tablet';
        if (/mobile|iphone|ipod|android|blackberry|opera|mini|windows\\sce|palm|smartphone|iemobile/i.test(userAgent)) return 'Mobile';
        return 'Desktop';
    }
    
    // Track visit function
    function trackVisit(data = {}) {
        const visitData = {
            page_url: window.location.href,
            referrer: document.referrer || '',
            user_agent: navigator.userAgent,
            browser: detectBrowser(),
            os: detectOS(),
            device: detectDevice(),
            session_id: getSessionId(),
            timestamp: new Date().toISOString(),
            ...data
        };
        
        log('Tracking visit', visitData);
        
        // Send data to backend
        fetch(`${config.apiUrl}/track`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(visitData)
        })
        .then(response => response.json())
        .then(result => {
            log('Visit tracked successfully', result);
        })
        .catch(error => {
            log('Error tracking visit', error);
        });
    }
    
    // Track custom event
    function trackEvent(eventName, eventData = {}) {
        const data = {
            event_name: eventName,
            event_data: eventData,
            custom_event: true
        };
        trackVisit(data);
    }
    
    // Track page view
    function trackPageView() {
        if (config.trackPageViews) {
            trackVisit({
                is_entry_page: !document.referrer || document.referrer.indexOf(window.location.host) === -1
            });
        }
    }
    
    // Track clicks
    function setupClickTracking() {
        if (config.trackClicks) {
            document.addEventListener('click', function(event) {
                const element = event.target;
                const tagName = element.tagName.toLowerCase();
                
                // Track important clicks
                if (tagName === 'a' || tagName === 'button' || element.onclick) {
                    const clickData = {
                        click_element: tagName,
                        click_text: element.textContent?.trim() || '',
                        click_href: element.href || '',
                        click_id: element.id || '',
                        click_class: element.className || '',
                        custom_event: true,
                        event_name: 'click'
                    };
                    trackEvent('click', clickData);
                }
            });
        }
    }
    
    // Track errors
    function setupErrorTracking() {
        if (config.trackErrors) {
            window.addEventListener('error', function(event) {
                trackEvent('javascript_error', {
                    error_message: event.message,
                    error_filename: event.filename,
                    error_line: event.lineno,
                    error_column: event.colno
                });
            });
        }
    }
    
    // Track page exit
    function setupExitTracking() {
        window.addEventListener('beforeunload', function() {
            // Use navigator.sendBeacon for reliable exit tracking
            const exitData = {
                is_exit_page: true,
                session_id: getSessionId(),
                page_url: window.location.href,
                timestamp: new Date().toISOString()
            };
            
            const blob = new Blob([JSON.stringify(exitData)], { type: 'application/json' });
            navigator.sendBeacon(`${config.apiUrl}/track`, blob);
        });
    }
    
    // Initialize analytics
    function init(customConfig = {}) {
        // Merge custom configuration
        Object.assign(config, customConfig);
        
        log('Initializing analytics', config);
        
        // Set up tracking
        trackPageView();
        setupClickTracking();
        setupErrorTracking();
        setupExitTracking();
        
        // Expose public API
        window.analytics = {
            track: trackVisit,
            trackEvent: trackEvent,
            trackPageView: trackPageView,
            config: config
        };
        
        log('Analytics initialized');
    }
    
    // Auto-initialize if DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
})();
