/**
 * ESO Logs API Status Monitor
 * Checks API status periodically and displays indicator in the header
 */

(function() {
    'use strict';

    // Configuration
    const CHECK_INTERVAL = 5 * 60 * 1000; // 5 minutes
    const ENDPOINTS = {
        oauth: 'https://www.esologs.com/oauth/token',
        graphql: 'https://www.esologs.com/api/v2/client'
    };

    // Status states
    const STATUS = {
        CHECKING: { icon: '🔄', text: 'Checking...', class: 'checking' },
        ONLINE: { icon: '✅', text: 'API Online', class: 'online' },
        PARTIAL: { icon: '⚠️', text: 'Partial Outage', class: 'partial' },
        OFFLINE: { icon: '❌', text: 'API Offline', class: 'offline' },
        ERROR: { icon: '❓', text: 'Status Unknown', class: 'error' }
    };

    let statusElement = null;
    let lastCheck = null;
    let checkTimeout = null;

    /**
     * Create the status indicator element
     */
    function createStatusIndicator() {
        // Create container
        const container = document.createElement('div');
        container.id = 'api-status-indicator';
        container.className = 'api-status';
        container.innerHTML = `
            <span class="api-status-icon"></span>
            <span class="api-status-text">Initializing...</span>
            <span class="api-status-details" style="display: none;"></span>
        `;

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            #api-status-indicator {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: var(--md-code-bg-color);
                border: 1px solid var(--md-default-fg-color--lightest);
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 0.875rem;
                display: flex;
                align-items: center;
                gap: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                z-index: 999;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }

            #api-status-indicator:hover {
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }

            #api-status-indicator:hover .api-status-details {
                display: inline !important;
                margin-left: 8px;
                opacity: 0.8;
                font-size: 0.75rem;
            }

            .api-status-icon {
                font-size: 1rem;
            }

            .api-status.online {
                border-color: #4caf50;
                background: rgba(76, 175, 80, 0.1);
            }

            .api-status.partial {
                border-color: #ff9800;
                background: rgba(255, 152, 0, 0.1);
            }

            .api-status.offline {
                border-color: #f44336;
                background: rgba(244, 67, 54, 0.1);
            }

            .api-status.checking {
                opacity: 0.7;
            }

            /* Mobile adjustments */
            @media (max-width: 768px) {
                #api-status-indicator {
                    bottom: 10px;
                    right: 10px;
                    font-size: 0.75rem;
                }
            }

            /* Dark theme adjustments */
            [data-md-color-scheme="slate"] #api-status-indicator {
                background: var(--md-code-bg-color);
                color: var(--md-default-fg-color);
            }
        `;
        document.head.appendChild(style);

        return container;
    }

    /**
     * Update the status indicator
     */
    function updateStatus(status, details = '') {
        if (!statusElement) return;

        const iconEl = statusElement.querySelector('.api-status-icon');
        const textEl = statusElement.querySelector('.api-status-text');
        const detailsEl = statusElement.querySelector('.api-status-details');

        iconEl.textContent = status.icon;
        textEl.textContent = status.text;
        detailsEl.textContent = details;

        statusElement.className = `api-status ${status.class}`;

        // Store last check time
        lastCheck = new Date();
    }

    /**
     * Check API endpoint status
     */
    async function checkEndpoint(url, method = 'GET') {
        try {
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 5000); // 5s timeout

            const options = {
                method: method,
                mode: 'no-cors', // Important for cross-origin requests
                signal: controller.signal
            };

            const response = await fetch(url, options);
            clearTimeout(timeout);

            // With no-cors, we can't read the response, but if fetch succeeds, endpoint is up
            return true;
        } catch (error) {
            if (error.name === 'AbortError') {
                console.log(`Timeout checking ${url}`);
            }
            return false;
        }
    }

    /**
     * Check all endpoints and determine overall status
     */
    async function checkAPIStatus() {
        updateStatus(STATUS.CHECKING);

        try {
            // Since we can't actually check the endpoints due to CORS in the browser,
            // we'll use a different approach - check if we can load a small image from the site
            const testUrl = 'https://www.esologs.com/favicon.ico';
            const img = new Image();

            const imageLoaded = await new Promise((resolve) => {
                img.onload = () => resolve(true);
                img.onerror = () => resolve(false);
                setTimeout(() => resolve(false), 5000); // 5s timeout
                img.src = testUrl + '?t=' + Date.now(); // Prevent caching
            });

            if (imageLoaded) {
                updateStatus(STATUS.ONLINE, 'Last checked: ' + new Date().toLocaleTimeString());
            } else {
                updateStatus(STATUS.OFFLINE, 'Cannot reach ESO Logs');
            }

        } catch (error) {
            console.error('Error checking API status:', error);
            updateStatus(STATUS.ERROR, 'Check failed');
        }

        // Schedule next check
        scheduleNextCheck();
    }

    /**
     * Schedule the next status check
     */
    function scheduleNextCheck() {
        if (checkTimeout) {
            clearTimeout(checkTimeout);
        }
        checkTimeout = setTimeout(checkAPIStatus, CHECK_INTERVAL);
    }

    /**
     * Initialize the status monitor
     */
    function init() {
        // Only run on main documentation pages, not in search results
        if (window.location.pathname.includes('/search/')) {
            return;
        }

        // Create and add status indicator
        statusElement = createStatusIndicator();
        document.body.appendChild(statusElement);

        // Add click handler to manually refresh
        statusElement.addEventListener('click', () => {
            checkAPIStatus();
        });

        // Initial check
        checkAPIStatus();

        // Also check when page becomes visible again
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden && lastCheck) {
                const timeSinceLastCheck = Date.now() - lastCheck.getTime();
                if (timeSinceLastCheck > CHECK_INTERVAL) {
                    checkAPIStatus();
                }
            }
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
