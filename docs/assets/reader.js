(() => {
  const root = document.documentElement;
  const theme = document.querySelector('#theme');
  const size = document.querySelector('#size');
  const output = document.querySelector('#size-label');
  const settings = document.querySelector('.settings');
  const save = (key, value) => { try { localStorage.setItem(key, value); } catch {} };
  theme.value = root.dataset.theme || 'system';
  size.value = parseInt(getComputedStyle(root).getPropertyValue('--reading-size'), 10) || 21;
  output.value = `${size.value} px`;
  theme.addEventListener('change', () => {
    if (theme.value === 'system') delete root.dataset.theme;
    else root.dataset.theme = theme.value;
    save('retention-theme', theme.value);
  });
  size.addEventListener('input', () => {
    root.style.setProperty('--reading-size', `${size.value}px`);
    output.value = `${size.value} px`;
    save('retention-size', size.value);
  });
  document.addEventListener('click', event => {
    if (!settings.contains(event.target)) settings.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && settings.open) {
      settings.open = false;
      settings.querySelector('summary').focus();
    }
  });
})();
