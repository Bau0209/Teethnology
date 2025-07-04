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