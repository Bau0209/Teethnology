// Tab switching functionality
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Remove active class from all tabs
        document.querySelectorAll('.nav-link').forEach(tab => {
            tab.classList.remove('active');
        });
        
        // Add active class to clicked tab
        this.classList.add('active');
        
        // Hide all sections
        document.querySelectorAll('.tab-content').forEach(section => {
            section.style.display = 'none';
        });
        
        // Show the selected section
        const sectionId = this.getAttribute('data-branch');
        document.getElementById(sectionId).style.display = 'block';
    });
});
