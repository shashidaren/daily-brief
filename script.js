/*
 * Daily Brief – JavaScript
 *
 * This script enhances navigation by highlighting the current section link as
 * the user scrolls through the page.  It uses the Intersection Observer
 * API to detect when a section enters the viewport.
 */

document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('nav .nav-list li a');
  const sections = document.querySelectorAll('.news-section');

  // Map section IDs to corresponding nav links for quick lookup
  const sectionMap = {};
  navLinks.forEach(link => {
    const targetId = link.getAttribute('href').replace('#', '');
    sectionMap[targetId] = link;
  });

  // Remove 'active' class from all links
  const clearActive = () => {
    navLinks.forEach(link => link.classList.remove('active'));
  };

  // Observer callback to set the active nav link when a section is intersecting
  const observerCallback = entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        clearActive();
        const link = sectionMap[id];
        if (link) {
          link.classList.add('active');
        }
      }
    });
  };

  // Configure Intersection Observer
  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -60% 0px',
    threshold: 0.2,
  };

  const observer = new IntersectionObserver(observerCallback, observerOptions);
  sections.forEach(section => observer.observe(section));
});