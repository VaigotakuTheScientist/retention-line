(() => {
  const root = document.documentElement;
  const theme = document.querySelector('#theme');
  const size = document.querySelector('#size');
  const output = document.querySelector('#size-label');
  const width = document.querySelector('#width');
  const widthOutput = document.querySelector('#width-label');
  const settings = document.querySelector('.settings');
  const save = (key, value) => { try { localStorage.setItem(key, value); } catch {} };
  theme.value = root.dataset.theme || 'system';
  size.value = parseInt(getComputedStyle(root).getPropertyValue('--reading-size'), 10) || 21;
  output.value = `${size.value} px`;
  width.value = root.dataset.readingWidth || 660;
  const updateWidth = () => {
    const value = Number(width.value);
    const label = value === 1500 ? width.dataset.fullLabel : `${value} px`;
    root.style.setProperty('--reading-width', value === 1500 ? 'none' : `${value}px`);
    root.dataset.readingWidth = value;
    widthOutput.value = label;
    width.setAttribute('aria-valuetext', label);
  };
  updateWidth();
  width.addEventListener('input', () => {
    updateWidth();
    save('retention-width', width.value);
  });
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
