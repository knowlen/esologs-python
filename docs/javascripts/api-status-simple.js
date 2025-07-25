/**
 * ESO Logs API Status Indicator - Simple Version
 * Displays a status indicator with link to check current status
 */

(function() {
    'use strict';

    // Configuration - Set this to true when API is known to be down
    const API_IS_DOWN = true; // TODO: Update this based on monitoring
    const LAST_CHECKED = '2025-07-23'; // TODO: Update when status changes

    function createStatusIndicator() {
        const container = document.createElement('div');
        container.id = 'api-status-banner';

        if (API_IS_DOWN) {
            container.className = 'api-status-banner offline';
            container.innerHTML = `
                <span class="status-icon">⚠️</span>
                <span class="status-text">ESO Logs API is currently experiencing issues</span>
                <a href="https://github.com/knowlen/esologs-python/issues/new?labels=api-status&title=API%20Status%20Report"
                   target="_blank" class="status-link">Report Status</a>
            `;
        } else {
            container.className = 'api-status-banner online';
            container.innerHTML = `
                <span class="status-icon">✅</span>
                <span class="status-text">ESO Logs API is operational</span>
            `;
        }

        // Add CSS
        if (!document.getElementById('api-status-banner-styles')) {
            const style = document.createElement('style');
            style.id = 'api-status-banner-styles';
            style.textContent = `
                #api-status-banner {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    padding: 8px 20px;
                    text-align: center;
                    font-size: 0.875rem;
                    z-index: 100;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                }

                #api-status-banner.offline {
                    background: #ff9800;
                    color: #000;
                }

                #api-status-banner.online {
                    display: none; /* Hide when online */
                }

                .status-icon {
                    font-size: 1rem;
                }

                .status-link {
                    color: inherit;
                    text-decoration: underline;
                    margin-left: 10px;
                }

                .status-link:hover {
                    text-decoration: none;
                }

                /* Adjust page content to account for banner */
                .md-header {
                    top: 32px !important;
                }

                /* Mobile adjustments */
                @media (max-width: 768px) {
                    #api-status-banner {
                        font-size: 0.75rem;
                        padding: 6px 10px;
                        flex-wrap: wrap;
                    }
                }

                /* Print styles */
                @media print {
                    #api-status-banner {
                        display: none !important;
                    }
                    .md-header {
                        top: 0 !important;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        return container;
    }

    function init() {
        // Don't show on 404 pages
        if (window.location.pathname.includes('/404')) {
            return;
        }

        // Add status banner to body
        const banner = createStatusIndicator();
        document.body.insertBefore(banner, document.body.firstChild);

        // If API is down, adjust header position
        if (API_IS_DOWN) {
            const header = document.querySelector('.md-header');
            if (header) {
                header.style.top = '32px';
            }
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
