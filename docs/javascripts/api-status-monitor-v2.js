/**
 * ESO Logs API Status Monitor v2
 * Uses a proxy endpoint or displays manual status based on known issues
 */

(function() {
    'use strict';

    // Configuration
    const CHECK_INTERVAL = 5 * 60 * 1000; // 5 minutes
    const STATUS_ENDPOINT = 'https://api.github.com/repos/knowlen/esologs-python/issues?labels=api-status&state=open';

    // Status states
    const STATUS = {
        CHECKING: { icon: '🔄', text: 'Checking...', class: 'checking' },
        ONLINE: { icon: '✅', text: 'API Online', class: 'online' },
        ISSUES: { icon: '⚠️', text: 'Known Issues', class: 'partial' },
        OFFLINE: { icon: '❌', text: 'API Offline', class: 'offline' },
        UNKNOWN: { icon: '❓', text: 'Status Unknown', class: 'unknown' }
    };

    let statusElement = null;
    let lastCheck = null;
    let checkTimeout = null;
    let currentStatus = STATUS.UNKNOWN;

    /**
     * Create the status indicator element
     */
    function createStatusIndicator() {
        const container = document.createElement('div');
        container.id = 'api-status-indicator';
        container.className = 'api-status';
        container.innerHTML = `
            <span class="api-status-icon"></span>
            <span class="api-status-text">Initializing...</span>
            <span class="api-status-details" style="display: none;"></span>
        `;

        // Add CSS
        if (!document.getElementById('api-status-styles')) {
            const style = document.createElement('style');
            style.id = 'api-status-styles';
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
                    z-index: 50;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }

                #api-status-indicator:hover {
                    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                }

                #api-status-indicator:hover .api-status-details {
                    display: inline !important;
                    margin-left: 8px;
                    opacity: 0.8;
                    font-size: 0.75rem;
                }

                .api-status-icon {
                    font-size: 1rem;
                    line-height: 1;
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
                        padding: 6px 10px;
                    }
                }

                /* Print styles */
                @media print {
                    #api-status-indicator {
                        display: none !important;
                    }
                }
            `;
            document.head.appendChild(style);
        }

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
        currentStatus = status;

        lastCheck = new Date();
    }

    /**
     * Check API status via GitHub issues
     */
    async function checkAPIStatus() {
        updateStatus(STATUS.CHECKING);

        try {
            // Check for open issues with 'api-status' label
            const response = await fetch(STATUS_ENDPOINT);

            if (response.ok) {
                const issues = await response.json();

                if (issues.length > 0) {
                    // There are open API status issues
                    const latestIssue = issues[0];
                    const title = latestIssue.title.toLowerCase();

                    if (title.includes('offline') || title.includes('down')) {
                        updateStatus(STATUS.OFFLINE, 'See GitHub for updates');
                    } else {
                        updateStatus(STATUS.ISSUES, latestIssue.title);
                    }
                } else {
                    // No open issues, assume API is online
                    updateStatus(STATUS.ONLINE, 'No known issues');
                }
            } else {
                // Couldn't check status
                updateStatus(STATUS.UNKNOWN, 'Unable to check');
            }
        } catch (error) {
            console.error('Error checking API status:', error);
            updateStatus(STATUS.UNKNOWN, 'Check failed');
        }

        scheduleNextCheck();
    }

    /**
     * Manual status display (fallback)
     */
    function displayManualStatus() {
        // Check if URL contains status parameter
        const urlParams = new URLSearchParams(window.location.search);
        const apiStatus = urlParams.get('api-status');

        if (apiStatus === 'offline') {
            updateStatus(STATUS.OFFLINE, 'Manually set');
        } else if (apiStatus === 'issues') {
            updateStatus(STATUS.ISSUES, 'Manually set');
        } else {
            // Default to checking
            checkAPIStatus();
        }
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
        // Don't run on search or 404 pages
        if (window.location.pathname.includes('/search/') ||
            window.location.pathname.includes('/404')) {
            return;
        }

        // Create and add status indicator
        statusElement = createStatusIndicator();
        document.body.appendChild(statusElement);

        // Click handler
        statusElement.addEventListener('click', () => {
            if (currentStatus === STATUS.OFFLINE || currentStatus === STATUS.ISSUES) {
                // Open GitHub issues
                window.open('https://github.com/knowlen/esologs-python/issues?q=is%3Aissue+label%3Aapi-status', '_blank');
            } else {
                // Manual refresh
                checkAPIStatus();
            }
        });

        // Add tooltip
        statusElement.title = 'Click to refresh status or view issues';

        // Initial status display
        displayManualStatus();

        // Visibility change handler
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
