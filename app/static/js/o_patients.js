// patient.js
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap modal
    const passwordModal = new bootstrap.Modal(document.getElementById('passwordModal'));
    passwordModal.show();

    // Password validation
    const correctPassword = "admin123"; // Change this to your actual password
    const submitPasswordBtn = document.getElementById('submitPassword');
    const passwordInput = document.getElementById('passwordInput');
    const mainContent = document.getElementById('mainContent');
    const forgotPasswordLink = document.getElementById('forgotPassword');

    submitPasswordBtn.addEventListener('click', function() {
        if (passwordInput.value === correctPassword) {
            passwordModal.hide();
            mainContent.style.display = 'block';
        } else {
            alert('Incorrect password. Please try again.');
            passwordInput.value = '';
        }
    });

    forgotPasswordLink.addEventListener('click', function(e) {
        e.preventDefault();
        alert('Please contact your system administrator to reset your password.');
    });

    // Tab switching functionality
    const branchTabs = document.querySelectorAll('#branchTabs .nav-link');
    branchTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            branchTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            // In a real app, you would load different data based on the selected branch
            console.log('Selected branch:', this.dataset.branch);
        });
    });

    // Filter functionality
    const filterSelect = document.getElementById('filterSelect');
    filterSelect.addEventListener('change', function() {
        console.log('Filter selected:', this.value);
        // In a real app, you would filter records based on this selection
    });

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    searchButton.addEventListener('click', function() {
        console.log('Searching for:', searchInput.value);
        // In a real app, you would search records based on the input
    });

    // Add dropdown functionality
    const addDropdownItems = document.querySelectorAll('[data-action]');
    addDropdownItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.dataset.action;
            if (action === 'scan') {
                alert('Scan functionality would be implemented here');
            } else if (action === 'form') {
                alert('Form would be displayed here');
            }
        });
    });
});