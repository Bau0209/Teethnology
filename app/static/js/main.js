// Responsive Navigation for header
(function() {
    const nav = document.querySelector('nav ul');
    if (!nav) return;

    // Create hamburger button if not present
    let hamburger = document.querySelector('.hamburger');
    if (!hamburger) {
        hamburger = document.createElement('button');
        hamburger.className = 'hamburger';
        hamburger.setAttribute('aria-label', 'Toggle navigation');
        hamburger.innerHTML = '<i class="fa fa-bars"></i>';
        nav.parentElement.insertBefore(hamburger, nav);
    }

    // Toggle nav menu on hamburger click
    hamburger.addEventListener('click', function(e) {
        e.stopPropagation();
        nav.classList.toggle('nav-open');
    });

    // Close nav when clicking outside (for mobile)
    document.addEventListener('click', function(e) {
        if (!nav.contains(e.target) && !hamburger.contains(e.target)) {
            nav.classList.remove('nav-open');
        }
    });

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