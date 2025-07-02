// Responsive Navigation for header
(function() {
    const nav = document.querySelector('nav ul');
    if (!nav) return;

    // Close nav when a link is clicked (for mobile UX)
    nav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            nav.classList.remove('nav-open');
        });
    });
})();

// Active Nav Link Highlight
(function() {
    const navLinks = document.querySelectorAll('nav ul li a');
    if (!navLinks.length) return;

    // Map section names to their HTML files
    const sectionToPage = {
        '#branch': 'Home.html',
        '#services': 'Home.html',
        '#about-us': 'Home.html',
    };

    // Update nav links to point to their respective pages if needed
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (sectionToPage[href]) {
            link.setAttribute('href', sectionToPage[href]);
        }
    });

    // Get current page (by pathname, ignore case)
    const path = window.location.pathname.split('/').pop().toLowerCase();

    navLinks.forEach(link => {
        // Remove all active classes first
        link.classList.remove('active');
        // If link matches current page, add active
        if (
            link.getAttribute('href').toLowerCase() === path ||
            (path === '' && link.getAttribute('href').toLowerCase().includes('home'))
        ) {
            link.classList.add('active');
        }
        // On click, update active class (SPA-like feel)
        link.addEventListener('click', function() {
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
})();
