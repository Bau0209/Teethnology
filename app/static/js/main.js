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
document.addEventListener('DOMContentLoaded', function () {
    console.log("main.js loaded ✅");

    const selectedServicesContainer = document.getElementById('selected-services-cards');

    // Service data (matches your existing service cards)
    const servicesData = {
        'Preventive Dentistry': {
            bgImage: '../../static/images/Dental Examination(BG).png',
            icon: '../../static/images/Dental Examination.png',
            description: 'Nullam sagittis hendrerit elit vitae faucibus. In augue urna, consequat quis accumsan non, vestibulum id dui.'
        },
        'Intervention Dentistry': {
            bgImage: '../../static/images/Root canal treatment(BG).png',
            icon: '../../static/images/Root canal treatment.png',
            description: 'Nullam sagittis hendrerit elit vitae faucibus. In augue urna, consequat quis accumsan non, vestibulum id dui.'
        },
        'Coroneric Dentistry': {
            bgImage: '../../static/images/dentures(bg).jpg',
            icon: '../../static/images/Dentures.png',
            description: 'Nullam sagittis hendrerit elit vitae faucibus. In augue urna, consequat quis accumsan non, vestibulum id dui.'
        },
        'Pediatric Dentistry': {
            bgImage: '../../static/images/Dental Examination(BG).png', // Default image if specific one doesn't exist
            icon: '../../static/images/Dental Examination.png',
            description: 'Child-focused dental care for healthy smiles.'
        },
        'Orthodontics': {
            bgImage: '../../static/images/Dental Examination(BG).png',
            icon: '../../static/images/Dental Examination.png',
            description: 'Orthodontic dental care for smile alignment.'
        },
        'Periodontics': {
            bgImage: '../../static/images/Root canal treatment(BG).png',
            icon: '../../static/images/Root canal treatment.png',
            description: 'Gum and periodontal treatment.'
        },
        'Oral and Nutritional': {
            bgImage: '../../static/images/dentures(bg).jpg',
            icon: '../../static/images/Dentures.png',
            description: 'Diet-based oral care guidance.'
        },
        'Sedation Dentistry': {
            bgImage: '../../static/images/Dental Examination(BG).png', // Default image if specific one doesn't exist
            icon: '../../static/images/Dental Examination.png',
            description: 'Comfort-focused sedation procedures.'
        },
        'Others': {
            bgImage: '../../static/images/Dental Examination(BG).png',
            icon: '../../static/images/Dental Examination.png',
            description: 'Miscellaneous dental services.'
        },

    };

    // Get services string from the hidden input and split
    const servicesString = document.getElementById('preselected-services')?.value || "";
    const selectedServices = servicesString.split(',').map(s => s.trim());

    selectedServices.forEach(serviceName => {
        addServiceCard(serviceName);
    });

    function addServiceCard(serviceName) {
        if (!servicesData[serviceName] || document.querySelector(`.selected-service-card[data-service="${serviceName}"]`)) {
            console.log(`Skipping: ${serviceName}`);
            return;
        }

        const service = servicesData[serviceName];
        const card = document.createElement('div');
        card.className = 'selected-service-card';
        card.dataset.service = serviceName;

        card.innerHTML = `
            <div class="service-card">
                <img src="${service.bgImage}" alt="${serviceName}" class="service-img">
                <div class="service-icon">
                    <img src="${service.icon}" alt="${serviceName} Icon">
                </div>
                <h3>${serviceName}</h3>
                <p>${service.description}</p>
            </div>
        `;

        selectedServicesContainer.appendChild(card);
        console.log(`✅ Rendered: ${serviceName}`);
    }
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
});
