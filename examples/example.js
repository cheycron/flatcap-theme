(() => {
  const root = document.documentElement;
  const controls = ['theme', 'contrast', 'density'];
  const condensed = document.getElementById('condensed');
  const persist = () => {
    const state = Object.fromEntries(controls.map(key => [key, root.getAttribute(`data-fc-${key}`)]));
    state.condensed = condensed.checked;
    try { localStorage.setItem('flatcap-example', JSON.stringify(state)); } catch { /* Optional storage. */ }
  };
  controls.forEach(key => {
    const input = document.getElementById(key);
    input.value = root.getAttribute(`data-fc-${key}`);
    input.addEventListener('change', () => {
      root.setAttribute(`data-fc-${key}`, input.value);
      persist();
    });
  });
  condensed.checked = root.dataset.exampleCondensed === 'true';
  condensed.addEventListener('change', () => {
    root.dataset.exampleCondensed = String(condensed.checked);
    persist();
  });
  document.getElementById('preferences').disabled = false;
  document.getElementById('settings-fields').disabled = false;

  const name = document.getElementById('service-name');
  const error = document.getElementById('name-error');
  const status = document.getElementById('form-status');
  document.getElementById('settings-form').addEventListener('submit', event => {
    event.preventDefault();
    const valid = name.value.trim().length > 0;
    error.hidden = valid;
    name.setAttribute('aria-invalid', String(!valid));
    status.textContent = valid ? `Example saved: ${name.value.trim()}. No data was sent.` : '';
    if (!valid) name.focus();
  });
})();
