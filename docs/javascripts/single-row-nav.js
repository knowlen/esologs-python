/**
 * Single Row Navigation for ESO Logs Python Documentation
 * Moves navigation tabs into the header for a cleaner single-row layout
 */

(function() {
    'use strict';

    // Global flag to track if we've set up the navigation
    let navSetup = false;

    function hideOriginalTabs() {
        // Hide ALL instances of the tabs container
        const allTabs = document.querySelectorAll('.md-tabs');
        allTabs.forEach(tab => {
            tab.style.display = 'none';
            tab.style.visibility = 'hidden';
            tab.style.height = '0';
            tab.style.overflow = 'hidden';
        });
    }

    function setupSingleRowNav() {
        // Only run on desktop viewports
        if (window.innerWidth < 1220) {
            navSetup = false;
            return;
        }

        // Always hide original tabs first
        hideOriginalTabs();

        const header = document.querySelector('.md-header__inner');
        const tabs = document.querySelector('.md-tabs__list');

        if (!header || !tabs) return;

        // Check if we already have navigation in header
        const existingNav = header.querySelector('.md-header__nav');
        if (existingNav) {
            // Update active states instead of recreating
            const headerLinks = existingNav.querySelectorAll('.md-tabs__link');
            const originalLinks = tabs.querySelectorAll('.md-tabs__link');

            headerLinks.forEach((link, index) => {
                link.classList.remove('md-tabs__link--active');
                if (originalLinks[index] && originalLinks[index].classList.contains('md-tabs__link--active')) {
                    link.classList.add('md-tabs__link--active');
                }
            });
            return;
        }

        // Create nav wrapper only if it doesn't exist
        const navWrapper = document.createElement('div');
        navWrapper.className = 'md-header__nav';

        // Clone the tabs
        const tabsClone = tabs.cloneNode(true);
        navWrapper.appendChild(tabsClone);

        // Find insertion point
        const search = header.querySelector('.md-search');
        if (search) {
            header.insertBefore(navWrapper, search);
        } else {
            header.appendChild(navWrapper);
        }

        // Handle navigation clicks
        const clonedLinks = navWrapper.querySelectorAll('.md-tabs__link');
        const originalLinks = tabs.querySelectorAll('.md-tabs__link');

        clonedLinks.forEach((link, index) => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                if (originalLinks[index]) {
                    // Use the href instead of click to avoid event issues
                    window.location.href = originalLinks[index].href;
                }
            });
        });

        navSetup = true;
    }

    // Initial setup
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(function() {
            setupSingleRowNav();

            // Set up a more aggressive observer for the tabs
            const observer = new MutationObserver(function(mutations) {
                hideOriginalTabs();
            });

            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true,
                attributeFilter: ['class', 'style']
            });
        }, 100);
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        setupSingleRowNav();
    });

    // Override any attempt to show the tabs
    const style = document.createElement('style');
    style.textContent = `
        @media screen and (min-width: 76.25em) {
            .md-tabs {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                overflow: hidden !important;
            }
        }
    `;
    document.head.appendChild(style);
})();
