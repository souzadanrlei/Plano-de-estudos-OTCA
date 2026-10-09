const outdatedWeekPath = /\/(semana-(?:1-fundamentos|2-api-sdk|3-collector|4-pipelines-revisao)\/)README\.md$/;

if (outdatedWeekPath.test(window.location.pathname)) {
  window.location.replace(
    window.location.pathname.replace(/README\.md$/, '') +
      window.location.search +
      window.location.hash
  );
} else {
  document.addEventListener('DOMContentLoaded', function () {
    const items = document.querySelectorAll('[data-animate="fade-up"]');

    if (!items.length) {
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    items.forEach((item) => observer.observe(item));
  });
}
