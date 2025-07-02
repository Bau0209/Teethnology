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
});

// js for save type  button
document.getElementById('editBtn').addEventListener('click', function() {
  // Get all input elements in the form
  const inputs = document.querySelectorAll('#patientForm input');
  
  // Make each input editable
  inputs.forEach(input => {
    input.readOnly = false;
  });
  
  // Enable the save button and disable the edit button
  document.getElementById('saveBtn').disabled = false;
  this.disabled = true;
});

// Optional: Handle form submission
javascript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap modal
    const passwordModal = new bootstrap.Modal(document.getElementById('passwordModal'), {
        backdrop: 'static',
        keyboard: false
    });
    
    // Show modal immediately when page loads
    passwordModal.show();

    // Password validation
    const correctPassword = "admin123"; // Change this to your actual password
    const submitPasswordBtn = document.getElementById('submitPassword');
    const passwordInput = document.getElementById('passwordInput');
    const mainContent = document.querySelector('.patients-container');
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

    // Handle Enter key in password field
    passwordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            submitPasswordBtn.click();
        }
    });

    forgotPasswordLink.addEventListener('click', function(e) {
        e.preventDefault();
        alert('Please contact your system administrator to reset your password.');
    });
  // Reset buttons
  document.getElementById('editBtn').disabled = false;
  document.getElementById('saveBtn').disabled = true;
  
  alert('Changes saved!');
});
$('#editBtn').click(function() {
  $('#patientForm input').prop('readonly', false);
  $(this).prop('disabled', true);
  $('#saveBtn').prop('disabled', false);
});

$('#patientForm').submit(function(e) {
  e.preventDefault();
  // Save logic here
  
  $('#patientForm input').prop('readonly', true);
  $('#editBtn').prop('disabled', false);
  $('#saveBtn').prop('disabled', true);
  alert('Changes saved!');
});

