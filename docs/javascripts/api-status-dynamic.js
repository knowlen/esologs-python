/**
 * ESO Logs API Status Monitor - Dynamic Version
 * Checks API status in real-time without requiring documentation rebuilds
 */

(function() {
    'use strict';

    // Configuration
    const CHECK_INTERVAL = 5 * 60 * 1000; // 5 minutes
    const STORAGE_KEY = 'esologs_api_status';
    const CACHE_DURATION = 5 * 60 * 1000; // Cache for 5 minutes

    // We'll use a CORS proxy or check multiple indicators
    const STATUS_CHECKS = [
        {
            // Option 1: Check via a public CORS proxy (replace with your preferred proxy)
            name: 'cors-proxy',
            check: async () => {
                try {
                    // Using allorigins.win as an example CORS proxy
                    const proxyUrl = `https://api.allorigins.win/raw?url=${encodeURIComponent('https://www.esologs.com/api/v2/client')}`;
                    const response = await fetch(proxyUrl, {
                        method: 'GET',
                        timeout: 5000
                    });
                    // If we get any response, the server is up
                    return response.status !== 502;
                } catch (error) {
                    return null; // Inconclusive
                }
            }
        },
        {
            // Option 2: Check the main website (usually same infrastructure)
            name: 'website-check',
            check: async () => {
                try {
                    // Create an image element to bypass CORS
                    const img = new Image();
                    const promise = new Promise((resolve) => {
                        img.onload = () => resolve(true);
                        img.onerror = () => resolve(false);
                        setTimeout(() => resolve(null), 5000); // 5s timeout
                    });

                    // Try to load favicon with cache buster
                    img.src = `https://www.esologs.com/favicon.ico?_=${Date.now()}`;

                    return await promise;
                } catch (error) {
                    return null;
                }
            }
        },
        {
            // Option 3: Use a third-party status checker API
            name: 'status-api',
            check: async () => {
                try {
                    // You could use services like isitdownrightnow.com API
                    // or create your own status endpoint on a different server
                    const response = await fetch(`https://api.github.com/repos/knowlen/esologs-python/contents/docs/assets/api-status.json?_=${Date.now()}`);
                    if (response.ok) {
                        const data = await response.json();
                        const content = JSON.parse(atob(data.content));
                        return content.online;
                    }
                } catch (error) {
                    return null;
                }
            }
        }
    ];

    let statusElement = null;
    let checkTimeout = null;

    /**
     * Get cached status from localStorage
     */
    function getCachedStatus() {
        try {
            const cached = localStorage.getItem(STORAGE_KEY);
            if (cached) {
                const data = JSON.parse(cached);
                if (Date.now() - data.timestamp < CACHE_DURATION) {
                    return data.status;
                }
            }
        } catch (e) {
            // Ignore localStorage errors
        }
        return null;
    }

    /**
     * Save status to localStorage
     */
    function setCachedStatus(status) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
                status: status,
                timestamp: Date.now()
            }));
        } catch (e) {
            // Ignore localStorage errors
        }
    }

    /**
     * Create the status banner
     */
    function createStatusBanner() {
        const banner = document.createElement('div');
        banner.id = 'api-status-banner';
        banner.className = 'api-status-banner';
        banner.style.display = 'none';
        banner.innerHTML = `
            <div class="status-content">
                <span class="status-icon">⚠️</span>
                <span class="status-text">ESO Logs API may be experiencing issues</span>
                <span class="status-time"></span>
                <a href="#" class="status-dismiss">✕</a>
            </div>
        `;

        // Add CSS
        if (!document.getElementById('api-status-dynamic-styles')) {
            const style = document.createElement('style');
            style.id = 'api-status-dynamic-styles';
            style.textContent = `
                #api-status-banner {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    background: #ff9800;
                    color: #000;
                    padding: 8px 20px;
                    text-align: center;
                    font-size: 0.875rem;
                    z-index: 1000;
                    transform: translateY(-100%);
                    transition: transform 0.3s ease;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
                }

                #api-status-banner.show {
                    transform: translateY(0);
                }

                .status-content {
                    max-width: 1200px;
                    margin: 0 auto;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                    position: relative;
                }

                .status-icon {
                    font-size: 1rem;
                }

                .status-time {
                    font-size: 0.75rem;
                    opacity: 0.8;
                }

                .status-dismiss {
                    position: absolute;
                    right: 0;
                    color: inherit;
                    text-decoration: none;
                    font-size: 1.2rem;
                    line-height: 1;
                    opacity: 0.8;
                    padding: 0 5px;
                }

                .status-dismiss:hover {
                    opacity: 1;
                }

                /* Adjust page content when banner is shown */
                body.api-status-shown .md-header {
                    top: 36px !important;
                }

                /* Mobile adjustments */
                @media (max-width: 768px) {
                    #api-status-banner {
                        font-size: 0.75rem;
                        padding: 6px 10px;
                    }

                    .status-content {
                        flex-wrap: wrap;
                    }

                    body.api-status-shown .md-header {
                        top: 48px !important;
                    }
                }

                /* Print styles */
                @media print {
                    #api-status-banner {
                        display: none !important;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        return banner;
    }

    /**
     * Show or hide the status banner
     */
    function updateBanner(isOnline, lastCheck) {
        if (!statusElement) return;

        if (!isOnline) {
            // Show banner
            statusElement.style.display = 'block';
            setTimeout(() => {
                statusElement.classList.add('show');
                document.body.classList.add('api-status-shown');
            }, 10);

            // Update time
            const timeEl = statusElement.querySelector('.status-time');
            if (timeEl && lastCheck) {
                timeEl.textContent = `(Last checked: ${new Date(lastCheck).toLocaleTimeString()})`;
            }
        } else {
            // Hide banner
            statusElement.classList.remove('show');
            document.body.classList.remove('api-status-shown');
            setTimeout(() => {
                statusElement.style.display = 'none';
            }, 300);
        }
    }

    /**
     * Check API status using multiple methods
     */
    async function checkAPIStatus() {
        // First check cache
        const cached = getCachedStatus();
        if (cached !== null) {
            updateBanner(!cached.online, cached.lastCheck);
            scheduleNextCheck();
            return;
        }

        // Try different check methods
        let isOnline = null;

        for (const checker of STATUS_CHECKS) {
            try {
                const result = await checker.check();
                if (result !== null) {
                    isOnline = result;
                    console.log(`API status via ${checker.name}: ${isOnline ? 'online' : 'offline'}`);
                    break;
                }
            } catch (error) {
                console.error(`Error with ${checker.name}:`, error);
            }
        }

        // Default to online if we can't determine
        if (isOnline === null) {
            isOnline = true;
        }

        // Update cache and UI
        const status = {
            online: isOnline,
            lastCheck: Date.now()
        };
        setCachedStatus(status);
        updateBanner(!isOnline, status.lastCheck);

        scheduleNextCheck();
    }

    /**
     * Schedule the next check
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
        // Don't run on 404 pages
        if (window.location.pathname.includes('/404')) {
            return;
        }

        // Create and add banner
        statusElement = createStatusBanner();
        document.body.appendChild(statusElement);

        // Add dismiss handler
        const dismissBtn = statusElement.querySelector('.status-dismiss');
        if (dismissBtn) {
            dismissBtn.addEventListener('click', (e) => {
                e.preventDefault();
                // Hide for this session
                updateBanner(true);
                // Clear cache so it rechecks later
                try {
                    localStorage.removeItem(STORAGE_KEY);
                } catch (e) {}
            });
        }

        // Start checking
        checkAPIStatus();

        // Re-check when tab becomes visible
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                checkAPIStatus();
            }
        });

        // Also check on page navigation (for single-page apps)
        let lastPath = window.location.pathname;
        setInterval(() => {
            if (window.location.pathname !== lastPath) {
                lastPath = window.location.pathname;
                checkAPIStatus();
            }
        }, 1000);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
