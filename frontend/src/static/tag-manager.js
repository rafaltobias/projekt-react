/**
 * Tag Manager - Handles tag execution for website tracking and custom actions
 * Similar to the functionality in tags.js from the previous project
 */

class TagManager {
    constructor() {
        this.tags = [];
        this.initialized = false;
    }

    /**
     * Initialize the tag manager and load all tags
     */
    async init() {
        if (this.initialized) return;
        
        try {
            await this.loadTags();
            this.setupEventListeners();
            this.initialized = true;
            console.log('Tag Manager initialized successfully');
        } catch (error) {
            console.error('Failed to initialize Tag Manager:', error);
        }
    }    /**
     * Load all tags from the API
     */
    async loadTags() {
        try {
            // Use the API URL constant rather than a relative URL
            const API_URL = 'http://localhost:5000';
            const response = await fetch(`${API_URL}/api/tags`);
            
            // Check if the response is successful before parsing
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            // Check content type to make sure it's JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error(`Expected JSON but got ${contentType}`);
            }
            
            const data = await response.json();
            
            // Handle both direct array responses and { rows: [...] } format
            if (Array.isArray(data)) {
                this.tags = data;
            } else if (data && data.rows && Array.isArray(data.rows)) {
                this.tags = data.rows;
            } else {
                this.tags = [];
            }
            
            console.log(`Loaded ${this.tags.length} tags`);
        } catch (error) {
            console.error('Failed to load tags:', error);
            this.tags = [];
        }
    }

    /**
     * Set up event listeners for all tags with click triggers
     */
    setupEventListeners() {
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
    }

    /**
     * Execute all tags with a specific trigger
     * 
     * @param {string} triggerType - The trigger type to match
     */
    executeTags(triggerType) {
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
    }

    /**
     * Execute a single tag's action
     * 
     * @param {Object} tag - The tag to execute
     */
    executeTag(tag) {
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
}

// Create and initialize the tag manager
const tagManager = new TagManager();
document.addEventListener('DOMContentLoaded', () => {
    tagManager.init();
});

// Export for usage in other files
export default tagManager;
