/* Restore validated preferences before consumer styles paint. No network requests. */
(() => {
  const choices = { theme: ['slate', 'daylight', 'system'], contrast: ['standard', 'more', 'system'], density: ['comfortable', 'compact'] };
  try {
    const stored = JSON.parse(localStorage.getItem('flatcap-example') || '{}');
    for (const [key, values] of Object.entries(choices)) {
      if (values.includes(stored[key])) document.documentElement.setAttribute(`data-fc-${key}`, stored[key]);
    }
    if (stored.condensed === true) document.documentElement.dataset.exampleCondensed = 'true';
  } catch { /* Restricted storage must not prevent a readable initial page. */ }
})();
