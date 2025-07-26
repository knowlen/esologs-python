/**
 * ESO Logs API Status Checker - Lightweight Dynamic Version
 * Uses indirect methods to check API status without CORS issues
 */

(function() {
    'use strict';

    // Configuration
    const CHECK_INTERVAL = 10 * 60 * 1000; // 10 minutes
    const STORAGE_KEY = 'esologs_api_status_cache';
    const DISMISSED_KEY = 'esologs_api_status_dismissed';
    const CACHE_DURATION = 10 * 60 * 1000; // 10 minutes

    let bannerElement = null;
    let checkTimer = null;

    /**
     * Create status banner HTML
     */
    function createBanner() {
        const banner = document.createElement('div');
        banner.id = 'esologs-api-status';
        banner.innerHTML = `
            <style>
                #esologs-api-status {
                    position: fixed;
                    top: -100px;
                    left: 0;
                    right: 0;
                    background: #ff6b35;
                    color: white;
                    padding: 10px;
                    text-align: center;
                    font-size: 14px;
                    z-index: 9999;
                    transition: top 0.3s ease;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                }

                #esologs-api-status.visible {
                    top: 0;
                }

                #esologs-api-status a {
                    color: white;
                    text-decoration: underline;
                    margin-left: 10px;
                }

                #esologs-api-status .close {
                    float: right;
                    cursor: pointer;
                    margin-left: 20px;
                    font-weight: bold;
                }

                @media (max-width: 768px) {
                    #esologs-api-status {
                        font-size: 12px;
                        padding: 8px;
                    }
                }
            </style>
            <span class="close" onclick="this.parentElement.classList.remove('visible'); localStorage.setItem('${DISMISSED_KEY}', Date.now())">×</span>
            <span>⚠️ ESO Logs API may be experiencing issues. Some examples might not work.</span>
            <a href="https://github.com/knowlen/esologs-python/issues" target="_blank">Report Issue</a>
        `;
        return banner;
    }

    /**
     * Check if banner was recently dismissed
     */
    function wasDismissed() {
        try {
            const dismissed = localStorage.getItem(DISMISSED_KEY);
            if (dismissed) {
                // Don't show again for 24 hours after dismissal
                return (Date.now() - parseInt(dismissed)) < 24 * 60 * 60 * 1000;
            }
        } catch (e) {}
        return false;
    }

    /**
     * Get cached status
     */
    function getCachedStatus() {
        try {
            const cached = localStorage.getItem(STORAGE_KEY);
            if (cached) {
                const data = JSON.parse(cached);
                if (Date.now() - data.time < CACHE_DURATION) {
                    return data.online;
                }
            }
        } catch (e) {}
        return null;
    }

    /**
     * Save status to cache
     */
    function setCachedStatus(online) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
                online: online,
                time: Date.now()
            }));
        } catch (e) {}
    }

    /**
     * Check API status using image loading as a proxy
     */
    async function checkStatus() {
        // Check cache first
        const cached = getCachedStatus();
        if (cached !== null) {
            return cached;
        }

        // Try to load a small asset from ESO Logs
        return new Promise((resolve) => {
            const img = new Image();
            const timeout = setTimeout(() => {
                img.src = '';
                resolve(false); // Timeout = assume offline
            }, 5000);

            img.onload = () => {
                clearTimeout(timeout);
                setCachedStatus(true);
                resolve(true);
            };

            img.onerror = () => {
                clearTimeout(timeout);
                setCachedStatus(false);
                resolve(false);
            };

            // Add timestamp to prevent caching
            img.src = `https://assets.rpglogs.com/img/eso/favicon.png?t=${Date.now()}`;
        });
    }

    /**
     * Update banner visibility
     */
    async function updateBanner() {
        if (wasDismissed()) return;

        const isOnline = await checkStatus();

        if (!isOnline && bannerElement) {
            // Show banner after a short delay
            setTimeout(() => {
                bannerElement.classList.add('visible');
            }, 1000);
        } else if (isOnline && bannerElement) {
            bannerElement.classList.remove('visible');
        }

        // Schedule next check
        if (checkTimer) clearTimeout(checkTimer);
        checkTimer = setTimeout(updateBanner, CHECK_INTERVAL);
    }

    /**
     * Initialize on page load
     */
    function init() {
        // Don't run on localhost or in iframes
        if (window.location.hostname === 'localhost' ||
            window.location.hostname === '127.0.0.1' ||
            window.self !== window.top) {
            return;
        }

        // Create banner
        bannerElement = createBanner();
        document.body.appendChild(bannerElement);

        // Start checking
        updateBanner();

        // Re-check when tab becomes active
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                updateBanner();
            }
        });
    }

    // Start when ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
