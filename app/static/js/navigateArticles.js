const articles = document.querySelectorAll('[data-link]');

for (const article of articles) {
  article.addEventListener('click', ({ currentTarget }) => {
    window.location.href = currentTarget.getAttribute('data-link');
  });
}
