document.addEventListener('DOMContentLoaded', function() {
    // Initialize the main add item modal
    const initAddItemModal = () => {
        const addModalEl = document.getElementById('addItemModal');
        if (!addModalEl) return;
        
        const addModal = new bootstrap.Modal(addModalEl, {
            focus: true,
            keyboard: true
        });

        // Handle add button clicks
        document.addEventListener('click', function(e) {
            if (e.target.closest('.add-btn')) {
                e.preventDefault();
                addModal.show();
            }
        });

        // Fix for aria-hidden warning
        addModalEl.addEventListener('shown.bs.modal', function() {
            const closeBtn = addModalEl.querySelector('.btn-close');
            if (closeBtn) closeBtn.focus();
        });
    };

    // Handle detail modals with proper error handling
    const initDetailModals = () => {
        document.addEventListener('click', function(e) {
            const viewTrigger = e.target.closest('a[data-bs-target^="#fullDetailsModal"]');
            if (!viewTrigger) return;
            
            e.preventDefault();
            const modalId = viewTrigger.getAttribute('data-bs-target');
            const modalEl = document.querySelector(modalId);
            
            if (!modalEl) {
                console.error(`Modal ${modalId} not found in DOM`);
                return;
            }

            // Initialize modal if not already initialized
            let modal = bootstrap.Modal.getInstance(modalEl);
            if (!modal) {
                modal = new bootstrap.Modal(modalEl, {
                    focus: true,
                    keyboard: true
                });
            }

            modal.show();
        });
    };

    // Initialize both modal systems
    initAddItemModal();
    initDetailModals();

    // Performance optimization to prevent forced reflows
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            // Any layout-sensitive operations
        }, 250);
    });
});

//function for filter
document.addEventListener('DOMContentLoaded', function () {
    const filterBtn = document.querySelector('.filter-btn');

    if (filterBtn) {
        // Create dropdown element (unchanged)
        const dropdown = document.createElement('div');
        dropdown.classList.add('dropdown-menu');
        dropdown.style.position = 'absolute';
        dropdown.style.display = 'none';
        dropdown.style.zIndex = '9999';
        dropdown.innerHTML = `
            <a class="dropdown-item" href="#" id="sortAZ">Sort by A-Z</a>
            <a class="dropdown-item" href="#" id="lowStock">Low Stock</a>
            <a class="dropdown-item" href="#" id="outOfStock">Out of Stock</a>
            <a class="dropdown-item" href="#" id="expired">Expired</a>
        `;
        document.body.appendChild(dropdown);

        // Toggle dropdown position on click (FIXED: Added e.preventDefault())
        filterBtn.addEventListener('click', function (e) {
            e.preventDefault(); // Prevent default form submission
            const rect = filterBtn.getBoundingClientRect();
            dropdown.style.left = `${rect.left + window.scrollX}px`;
            dropdown.style.top = `${rect.bottom + window.scrollY}px`;
            dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
        });

        // Hide dropdown on outside click (unchanged)
        document.addEventListener('click', function (e) {
            if (!filterBtn.contains(e.target) && !dropdown.contains(e.target)) {
                dropdown.style.display = 'none';
            }
        });

        // Sort by A-Z (unchanged)
        dropdown.querySelector('#sortAZ').addEventListener('click', function (e) {
            e.preventDefault();
            const tbody = document.querySelector('.patients-table tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            rows.sort((a, b) => {
                const nameA = a.children[2].textContent.trim().toLowerCase();
                const nameB = b.children[2].textContent.trim().toLowerCase();
                return nameA.localeCompare(nameB);
            });
            rows.forEach(row => tbody.appendChild(row));
            dropdown.style.display = 'none';
        });

        // Low Stock filter (unchanged)
        dropdown.querySelector('#lowStock').addEventListener('click', function (e) {
            e.preventDefault();
            const rows = document.querySelectorAll('.patients-table tbody tr');
            rows.forEach(row => {
                const stockCell = row.dataset.stock || row.textContent.toLowerCase();
                row.style.display = stockCell.includes('low') ? '' : 'none';
            });
            dropdown.style.display = 'none';
        });

        // Out of Stock filter (unchanged)
        dropdown.querySelector('#outOfStock').addEventListener('click', function (e) {
            e.preventDefault();
            const rows = document.querySelectorAll('.patients-table tbody tr');
            rows.forEach(row => {
                const stockCell = row.dataset.stock || row.textContent.toLowerCase();
                row.style.display = stockCell.includes('out of stock') ? '' : 'none';
            });
            dropdown.style.display = 'none';
        });

        // Expired filter (unchanged)
        dropdown.querySelector('#expired').addEventListener('click', function (e) {
            e.preventDefault();
            const rows = document.querySelectorAll('.patients-table tbody tr');
            rows.forEach(row => {
                const expCell = row.dataset.expired || row.textContent.toLowerCase();
                row.style.display = expCell.includes('expired') ? '' : 'none';
            });
            dropdown.style.display = 'none';
        });
    } else {
        console.warn("No element with class '.filter-btn' found.");
    }
});