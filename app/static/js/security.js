document.addEventListener('DOMContentLoaded', function() {
    const newPassword = document.getElementById('newPassword');
    const strengthIndicator = document.querySelector('.password-strength');
    
    if (newPassword && strengthIndicator) {
        newPassword.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            updateStrengthIndicator(strength);
        });
    }

    function calculatePasswordStrength(password) {
        let strength = 0;
        
        // Length check
        if (password.length >= 8) strength++;
        if (password.length >= 12) strength++;
        
        // Character variety checks
        if (/[A-Z]/.test(password)) strength++; // Uppercase
        if (/[a-z]/.test(password)) strength++; // Lowercase
        if (/[0-9]/.test(password)) strength++; // Numbers
        if (/[^A-Za-z0-9]/.test(password)) strength++; // Special chars
        
        return Math.min(strength, 4); // Cap at 4 for our strength levels
    }

    function updateStrengthIndicator(strength) {
        // Clear all classes first
        strengthIndicator.className = 'password-strength';
        
        // Add appropriate class based on strength
        if (password.length === 0) {
            strengthIndicator.classList.add('weak');
        } else if (strength <= 2) {
            strengthIndicator.classList.add('weak');
        } else if (strength === 3) {
            strengthIndicator.classList.add('medium');
        } else {
            strengthIndicator.classList.add('strong');
        }
    }
});