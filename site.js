/* Highlight the research section currently in view. The page works without JS. */
(() => {
  const links = [...document.querySelectorAll('.section-nav a[href^="#"]')];
  const sections = links.map(link => document.querySelector(link.getAttribute('href')));
  let queued = false;
  const update = () => {
    queued = false;
    let active = sections[0];
    for (const section of sections) {
      if (section.getBoundingClientRect().top <= 120) active = section;
    }
    for (const link of links) {
      if (link.getAttribute('href') === '#' + active.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    }
  };
  window.addEventListener('scroll', () => {
    if (!queued) { queued = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  window.addEventListener('resize', update, { passive: true });
  update();
})();
