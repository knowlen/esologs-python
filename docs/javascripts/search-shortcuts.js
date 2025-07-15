// Vim-style search shortcuts for ESO Logs Python Documentation
document.addEventListener('keydown', function(e) {
  // Forward slash to focus search (like vim)
  if (e.key === '/' && !e.ctrlKey && !e.metaKey && !e.altKey) {
    const searchInput = document.querySelector('.md-search__input');
    if (searchInput && document.activeElement !== searchInput) {
      // Don't trigger if we're in an input or textarea
      const tagName = document.activeElement.tagName.toLowerCase();
      if (tagName !== 'input' && tagName !== 'textarea') {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
      }
    }
  }

  // Escape to close search
  if (e.key === 'Escape') {
    const searchInput = document.querySelector('.md-search__input');
    if (searchInput && document.activeElement === searchInput) {
      searchInput.blur();
      searchInput.value = '';
      // Close search dialog
      const searchReset = document.querySelector('.md-search__form [type="reset"]');
      if (searchReset) {
        searchReset.click();
      }
    }
  }
});

// Add vim-style command hint to search
document.addEventListener('DOMContentLoaded', function() {
  const searchForm = document.querySelector('.md-search__form');
  if (searchForm && !searchForm.dataset.vimHint) {
    const hint = document.createElement('div');
    hint.className = 'search-vim-hint';
    hint.innerHTML = 'Press <kbd>/</kbd> to search';
    hint.style.cssText = `
      position: absolute;
      right: 3rem;
      top: 50%;
      transform: translateY(-50%);
      font-size: 0.7rem;
      color: var(--vim-comment);
      pointer-events: none;
      font-family: var(--md-code-font);
    `;
    searchForm.appendChild(hint);
    searchForm.dataset.vimHint = 'true';

    // Hide hint when search is focused
    const searchInput = searchForm.querySelector('.md-search__input');
    if (searchInput) {
      searchInput.addEventListener('focus', () => hint.style.display = 'none');
      searchInput.addEventListener('blur', () => {
        if (!searchInput.value) hint.style.display = 'block';
      });
    }
  }
});
