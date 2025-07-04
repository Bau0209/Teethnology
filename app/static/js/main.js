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

    // Get services string from the hidden input (expects a JSON array or comma-separated string)
    const servicesString = document.getElementById('preselected-services')?.value || "[]";

    // Parse string (supports both JSON array or comma-separated fallback)
    let selectedServices;
    try {
        selectedServices = JSON.parse(servicesString);
    } catch (err) {
        selectedServices = servicesString.split(',').map(s => s.trim());
    }

    // Fetch real service data from the backend
    fetch('/api/services')
        .then(response => response.json())
        .then(servicesData => {
            selectedServices.forEach(serviceName => {
                const matched = servicesData.find(s => s.name === serviceName);
                if (matched) {
                    addServiceCard(matched);
                } else {
                    console.warn(`⚠️ Service not found: ${serviceName}`);
                }
            });
        })
        .catch(error => {
            console.error('❌ Failed to load service data:', error);
        });

    // Dynamically add service card
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