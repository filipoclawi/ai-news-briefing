(() => {
  const filters = [...document.querySelectorAll('.filter')];
  const stories = [...document.querySelectorAll('.story[data-category]')];
  const resultCount = document.querySelector('#result-count');
  const progress = document.querySelector('.progress');

  function applyFilter(category) {
    let shown = 0;
    stories.forEach(story => {
      const match = category === 'all' || story.dataset.category === category;
      story.hidden = !match;
      if (match) shown += 1;
    });
    filters.forEach(button => {
      const active = button.dataset.filter === category;
      button.classList.toggle('active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    if (resultCount) {
      const german = document.documentElement.lang === 'de';
      const noun = german ? (shown === 1 ? 'Meldung' : 'Meldungen') : (shown === 1 ? 'story' : 'stories');
      resultCount.textContent = `${shown} ${noun}`;
    }
  }

  filters.forEach(button => button.addEventListener('click', () => applyFilter(button.dataset.filter)));
  window.addEventListener('scroll', () => {
    const height = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = `${height > 0 ? (scrollY / height) * 100 : 0}%`;
  }, { passive: true });
  applyFilter('all');
  document.documentElement.dataset.ready = 'true';
})();
