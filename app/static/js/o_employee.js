// employee.js
document.addEventListener('DOMContentLoaded', function() {
    // Tab switching functionality - enhanced version
    const branchTabs = document.querySelectorAll('.nav-link');
    
    branchTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all tabs
            branchTabs.forEach(t => t.classList.remove('active'));
            
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Hide all sections
            document.querySelectorAll('.tab-content').forEach(section => {
                section.style.display = 'none';
            });
            
            // Show the selected section
            const sectionId = this.getAttribute('data-branch');
            document.getElementById(sectionId).style.display = 'block';
            
            // Log the selected branch (similar to patient.js functionality)
            console.log('Selected branch:', this.dataset.branch);
        });
    });

    // Additional functionality similar to patient.js
    const filterSelect = document.getElementById('filterSelect');
    if (filterSelect) {
        filterSelect.addEventListener('change', function() {
            console.log('Filter selected:', this.value);
            // Filter implementation would go here
        });
    }

    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    if (searchButton && searchInput) {
        searchButton.addEventListener('click', function() {
            console.log('Searching for:', searchInput.value);
            // Search implementation would go here
        });
    }

    // Add dropdown functionality similar to patient.js
    const addDropdownItems = document.querySelectorAll('[data-action]');
    addDropdownItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const action = this.dataset.action;
            if (action === 'add') {
                alert('Add new employee functionality would be implemented here');
            } else if (action === 'import') {
                alert('Import employees functionality would be implemented here');
            }
        });
    });
});

// Form edit/save functionality similar to patient.js
document.addEventListener('DOMContentLoaded', function() {
    const editBtn = document.getElementById('editBtn');
    const saveBtn = document.getElementById('saveBtn');
    const employeeForm = document.getElementById('employeeForm');

    if (editBtn && saveBtn && employeeForm) {
        editBtn.addEventListener('click', function() {
            const inputs = employeeForm.querySelectorAll('input');
            inputs.forEach(input => {
                input.readOnly = false;
            });
            editBtn.disabled = true;
            saveBtn.disabled = false;
        });

        employeeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            // Save logic would go here
            
            const inputs = employeeForm.querySelectorAll('input');
            inputs.forEach(input => {
                input.readOnly = true;
            });
            editBtn.disabled = false;
            saveBtn.disabled = true;
            alert('Employee changes saved!');
        });
    }
});