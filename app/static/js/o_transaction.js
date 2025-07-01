document.addEventListener('DOMContentLoaded', function() {
    // Debugging start
    console.log('[Debug] Modal initialization started');

    // 1. Verify Bootstrap
    if (typeof bootstrap === 'undefined' || typeof bootstrap.Modal === 'undefined') {
        console.error('Bootstrap Modal not loaded!');
        return;
    }

    // 2. Get modal element
    const modalEl = document.getElementById('receiptModal');
    if (!modalEl) {
        console.error('Modal #receiptModal not found.');
        return;
    }

    // 3. Add critical CSS rules to ensure visibility
    const ensureModalVisibility = () => {
        const style = document.createElement('style');
        style.id = 'modal-fix-styles';
        style.textContent = `
            #receiptModal.show {
                opacity: 1 !important;
                pointer-events: all !important;
                transform: none !important;
            }
            #receiptModal.modal.fade.show {
                display: block !important;
            }
        `;
        document.head.appendChild(style);
    };
    ensureModalVisibility();

    // 4. Initialize modal
    let modalInstance;
    try {
        modalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        console.log('[Debug] Modal instance created');
    } catch (e) {
        console.error('Modal init failed:', e);
        return;
    }

    // 5. Enhanced click handler
    document.addEventListener('click', function(e) {
        const trigger = e.target.closest('[data-bs-toggle="modal"][data-bs-target="#receiptModal"]');
        if (!trigger) return;

        e.preventDefault();
        console.log('[Debug] Modal trigger clicked');

        // Force visibility before showing
        modalEl.style.display = 'block';
        modalEl.classList.add('show');
        document.body.classList.add('modal-open');

        // Create backdrop manually if needed
        if (!document.querySelector('.modal-backdrop')) {
            const backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop fade show';
            document.body.appendChild(backdrop);
        }

        // Official show call
        try {
            modalInstance.show();
            console.log('[Debug] Official show() called');
        } catch (error) {
            console.error('Modal show failed:', error);
        }

        // Debug visibility
        setTimeout(() => {
            console.log('[Debug] Computed styles:', {
                display: window.getComputedStyle(modalEl).display,
                opacity: window.getComputedStyle(modalEl).opacity,
                visibility: window.getComputedStyle(modalEl).visibility
            });
        }, 100);
    });

    console.log('[Debug] Modal system ready');
});

// Cleanup for SPA navigation
window.addEventListener('unload', function() {
    const style = document.getElementById('modal-fix-styles');
    if (style) style.remove();
});