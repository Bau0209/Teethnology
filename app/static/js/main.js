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

//service list function
// service list function
document.addEventListener('DOMContentLoaded', function () {
    console.log("main.js loaded ✅");

    const selectedServicesContainer = document.getElementById('selected-services-cards');

    // Hardcoded services list (since you're not using an API)
    const servicesData = [
        {
            "name": "Preventive Dentistry",
            "description": "Focuses on regular cleanings, exams, and education to prevent dental issues.",
            "icon_class": "fas fa-shield-alt",
            "bg_image": "/static/images/contact.jpg"
        },
        {
            "name": "Intervention Dentistry",
            "description": "Treats developing problems with fillings, sealants, and restorations.",
            "icon_class": "fas fa-tools",
            "bg_image": "/static/images/dentures(bg).jpg"
        },
        {
            "name": "Coroneric Dentistry",
            "description": "Specializes in restoring severely damaged or decayed teeth.",
            "icon_class": "fas fa-tooth",
            "bg_image": "/static/images/Root canal treatment(BG).png"
        },
        {
            "name": "Pediatric Dentistry",
            "description": "Provides dental care tailored for children.",
            "icon_class": "fas fa-child",
            "bg_image": "/static/images/Dental Examination(BG).png"
        },
        {
            "name": "Orthodontics",
            "description": "Aligns teeth and jaws using braces or aligners.",
            "icon_class": "fas fa-teeth",
            "bg_image": "/static/images/contact.jpg"
        },
        {
            "name": "Periodontics",
            "description": "Focuses on gum health and treatment of gum diseases.",
            "icon_class": "fas fa-syringe",
            "bg_image": "/static/images/dentures(bg).jpg"
        },
        {
            "name": "Oral and Nutritional",
            "description": "Promotes overall oral health through proper nutrition.",
            "icon_class": "fas fa-apple-alt",
            "bg_image": "/static/images/Root canal treatment(BG).png"
        },
        {
            "name": "Sedation Dentistry",
            "description": "Helps patients relax during procedures using sedation.",
            "icon_class": "fas fa-bed",
            "bg_image": "/static/images/Dental Examination(BG).png"
        },
        {
            "name": "Others",
            "description": "Miscellaneous or custom dental services.",
            "icon_class": "fas fa-ellipsis-h",
            "bg_image": "/static/images/contact.jpg"
        }
    ];

    const servicesString = document.getElementById('preselected-services')?.value || "[]";
    let selectedServices;
    try {
        selectedServices = JSON.parse(servicesString);
    } catch (err) {
        selectedServices = servicesString.split(',').map(s => s.trim());
    }

    selectedServices.forEach(serviceName => {
        const matched = servicesData.find(s => s.name === serviceName);
        if (matched) {
            addServiceCard(matched);
        } else {
            console.warn(`⚠️ Service not found: ${serviceName}`);
        }
    });

    function addServiceCard(service) {
        const serviceName = service.name;
        if (document.querySelector(`.selected-service-card[data-service="${serviceName}"]`)) {
            console.log(`⏭️ Skipping duplicate: ${serviceName}`);
            return;
        }

        const card = document.createElement('div');
        card.className = 'selected-service-card';
        card.dataset.service = serviceName;

        card.innerHTML = `
            <div class="service-card">
                <img src="${service.bg_image}" alt="${serviceName}" class="service-img">
                <div class="service-icon">
                    <i class="${service.icon_class}" style="color: #00898e; font-size: 40px;"></i>
                </div>
                <h3>${serviceName}</h3>
                <p>${service.description}</p>
            </div>
        `;

        selectedServicesContainer.appendChild(card);
        console.log(`✅ Rendered: ${serviceName}`);
    }
});

// Mobile Navigation Menu
document.addEventListener('DOMContentLoaded', function() {
    // Create and setup mobile navigation
    function setupMobileNavigation() {
        const header = document.querySelector('header');
        const existingNav = document.querySelector('header nav');
        const headerButtons = document.querySelector('header .button');
        
        // Create hamburger menu button
        const hamburgerMenu = document.createElement('div');
        hamburgerMenu.className = 'hamburger-menu';
        hamburgerMenu.innerHTML = '<span></span><span></span><span></span>';
        header.appendChild(hamburgerMenu);

        // Create mobile navigation menu
        const mobileNav = document.createElement('div');
        mobileNav.className = 'nav-menu';
        
        // Clone the existing navigation
        if (existingNav) {
            const navClone = existingNav.cloneNode(true);
            mobileNav.appendChild(navClone);
        }
        
        // Clone the buttons from header and reorder them
        if (headerButtons) {
            const buttonsClone = headerButtons.cloneNode(true);
            buttonsClone.classList.add('mobile-nav-buttons');
            
            // Get the buttons and reorder them
            const loginBtn = buttonsClone.querySelector('.login');
            const bookBtn = buttonsClone.querySelector('.book');
            
            // Clear existing buttons
            buttonsClone.innerHTML = '';
            
            // Add buttons in new order: Login first, then Book
            if (loginBtn) {
                loginBtn.style.display = 'block';
                loginBtn.style.width = '50% !important';
                loginBtn.style.margin = '10px 20px';
                loginBtn.style.textAlign = 'center';
                loginBtn.style.padding = '12px 10px';
                buttonsClone.appendChild(loginBtn);
            }
            
            if (bookBtn) {
                bookBtn.style.display = 'block';
                bookBtn.style.width = '50% !important';
                bookBtn.style.margin = '10px 20px';
                bookBtn.style.textAlign = 'center';
                bookBtn.style.padding = '12px 10px';
                buttonsClone.appendChild(bookBtn);
            }
            
            mobileNav.appendChild(buttonsClone);
        }
        
        // Add the mobile nav to the body
        document.body.appendChild(mobileNav);
        
        // Apply styles for right-side positioning
        mobileNav.style.width = '50%';
        mobileNav.style.right = '0';
        mobileNav.style.left = 'auto';
        mobileNav.style.transform = 'translateX(100%)';
        mobileNav.style.transition = 'transform 0.3s ease-in-out';
        mobileNav.style.flexDirection = 'column';
        mobileNav.style.justifyContent = 'flex-start';
        mobileNav.style.paddingTop = '60px';
        mobileNav.style.alignItems = 'flex-start'; 
        
        // Update active state styling for right position
        const style = document.createElement('style');
        style.textContent = `
            .nav-menu.active {
                transform: translateX(0) !important;
            }
            
            .nav-menu a {
                display: block;
                width: 80% !important;
                text-align: left; /* Changed from center to left */
                margin: 8px 0;
                padding: 12px 20px; /* Added left padding for better alignment */
            }
            
            .mobile-nav-buttons {
                display: flex;
                flex-direction: column;
                width: 100%;
                margin-top: 20px;
            }
            
            /* Prevent horizontal scrolling globally */
            html, body {
                overflow-x: hidden;
                max-width: 100%;
            }
            
        
            
            @media (max-width: 670px) {
                .hamburger-menu {
                    display: flex !important;
                    right: 20px;
                    left: auto;
                }
                
                header nav,
                header .button {
                    display: none !important;
                }
                
                .nav-menu.active {
                    transform: translateX(0) !important;
                }
                
                /* Fix for mobile nav menu width */
                .nav-menu {
                    width: 80% !important;
                    max-width: 300px;
                }
            }
            
            @media (max-width: 400px) {
                .hamburger-menu {
                    display: flex !important;
                    right: 10px !important;
                    left: auto !important;
                }
                
                header nav,
                header .button {
                    display: none !important;
                }
                
                .nav-menu.active {
                    transform: translateX(0) !important;
                }
                
                /* Further adjustments for very small screens */
                .nav-menu {
                    width: 85% !important;
                    max-width: 280px;
                }
                
                /* Left alignment for mobile nav links */
                .nav-menu a {
                    text-align: left;
                    align-items: flex-start;
                    padding-left: 30px; /* Added more left padding for small screens */
                }
            }

            @media (min-width: 671px) {
                .hamburger-menu {
                    display: none !important;
                }
                
                .nav-menu {
                    display: none !important;
                }
                
                header nav,
                header .button {
                    display: flex !important;
                }
            }
        `;
        document.head.appendChild(style);
        
        // Toggle mobile navigation
        hamburgerMenu.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileNav.classList.toggle('active');
            hamburgerMenu.classList.toggle('active');
            
            // Prevent body from scrolling when menu is open
            if (mobileNav.classList.contains('active')) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        });
        
        // Close menu when clicking on a link
        const navLinks = mobileNav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileNav.classList.remove('active');
                hamburgerMenu.classList.remove('active');
                document.body.style.overflow = ''; // Restore scrolling
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInsideNav = mobileNav.contains(event.target);
            const isClickOnHamburger = hamburgerMenu.contains(event.target);
            
            if (!isClickInsideNav && !isClickOnHamburger && mobileNav.classList.contains('active')) {
                mobileNav.classList.remove('active');
                hamburgerMenu.classList.remove('active');
                document.body.style.overflow = ''; // Restore scrolling
            }
        });
        
        // Check if we're in mobile view and hide header elements
        function checkViewport() {
            const isMobileView = window.matchMedia('(max-width: 670px)').matches;
            
            if (isMobileView) {
                // Hide navigation and buttons in header
                if (existingNav) existingNav.style.display = 'none';
                if (headerButtons) headerButtons.style.display = 'none';
                hamburgerMenu.style.display = 'flex';
                // Update status indicator
                if (document.getElementById('menu-status')) {
                    document.getElementById('menu-status').textContent = 'visible';
                }
            } else {
                // Show navigation and buttons in header
                if (existingNav) existingNav.style.display = '';
                if (headerButtons) headerButtons.style.display = '';
                hamburgerMenu.style.display = 'none';
                mobileNav.classList.remove('active');
                hamburgerMenu.classList.remove('active');
                document.body.style.overflow = ''; // Ensure scrolling is restored
                // Update status indicator
                if (document.getElementById('menu-status')) {
                    document.getElementById('menu-status').textContent = 'hidden';
                }
            }
            
            // Update viewport width display
            if (document.getElementById('viewport-width')) {
                document.getElementById('viewport-width').textContent = window.innerWidth;
            }
        }
        
        // Initial check
        checkViewport();
        
        // Listen for resize events
        window.addEventListener('resize', checkViewport);
    }
    
    // Initialize the mobile navigation
    setupMobileNavigation();
});
/*
 // Removes a service card
    function removeServiceCard(serviceName) {
        const card = document.querySelector(`.selected-service-card[data-service="${serviceName}"]`);
        if (card) {
            card.remove();
        }
    }

    // Global function for the remove button's onclick event
    window.removeService = function(serviceName) {
        removeServiceCard(serviceName);
        // Uncheck the corresponding checkbox
        const checkboxes = document.querySelectorAll('.services-checklist input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            if (checkbox.nextElementSibling.textContent === serviceName) {
                checkbox.checked = false;
            }
        });
    };*/

    