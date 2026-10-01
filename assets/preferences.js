/* Apply saved display preferences before the stylesheet loads. */
(() => {
  try {
    const theme = localStorage.getItem('retention-theme');
    if (['light', 'dark'].includes(theme)) document.documentElement.dataset.theme = theme;
    const size = Number(localStorage.getItem('retention-size'));
    if (size >= 17 && size <= 28) document.documentElement.style.setProperty('--reading-size', `${size}px`);
  } catch { /* Reading still works when browser storage is disabled. */ }
})();
