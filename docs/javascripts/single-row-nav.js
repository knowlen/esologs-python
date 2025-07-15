/**
 * Single Row Navigation for ESO Logs Python Documentation
 * Moves navigation tabs into the header for a cleaner single-row layout
 */

document.addEventListener('DOMContentLoaded', function() {
    // Wait for MkDocs to initialize
    setTimeout(function() {
        setupSingleRowNav();
    }, 100);
    
    function setupSingleRowNav() {
        // Only run on desktop viewports
        if (window.innerWidth < 1220) return;
        
        const header = document.querySelector('.md-header__inner');
        const tabs = document.querySelector('.md-tabs__list');
        const tabsContainer = document.querySelector('.md-tabs');
        
        if (!header || !tabs) return;
        
        // Prevent duplicate moves
        if (header.querySelector('.md-header__nav')) return;
        
        // Create a nav wrapper
        const navWrapper = document.createElement('div');
        navWrapper.className = 'md-header__nav';
        
        // Move the tabs list into the nav wrapper
        navWrapper.appendChild(tabs.cloneNode(true));
        
        // Find insertion point - after title/before search
        const search = header.querySelector('.md-search');
        if (search) {
            header.insertBefore(navWrapper, search);
        } else {
            header.appendChild(navWrapper);
        }
        
        // Hide the original tabs container
        if (tabsContainer) {
            tabsContainer.style.display = 'none';
        }
        
        // Sync active states and handle navigation
        const clonedLinks = navWrapper.querySelectorAll('.md-tabs__link');
        const originalLinks = tabs.querySelectorAll('.md-tabs__link');
        
        clonedLinks.forEach((link, index) => {
            // Copy active state
            if (originalLinks[index] && originalLinks[index].classList.contains('md-tabs__link--active')) {
                link.classList.add('md-tabs__link--active');
            }
            
            // Handle clicks
            link.addEventListener('click', function(e) {
                e.preventDefault();
                if (originalLinks[index]) {
                    originalLinks[index].click();
                }
            });
        });
    }
    
    // Re-run on page changes (MkDocs instant loading)
    document.addEventListener('DOMContentSwitch', function() {
        setTimeout(setupSingleRowNav, 100);
    });
    
    // Also listen for location changes
    let lastLocation = location.href;
    new MutationObserver(function() {
        if (location.href !== lastLocation) {
            lastLocation = location.href;
            setTimeout(setupSingleRowNav, 100);
        }
    }).observe(document, { subtree: true, childList: true });
});