document.addEventListener('DOMContentLoaded', function () {
    // --- Modal Initialization ---
    const modalEl = document.getElementById('receiptModal');
    if (!modalEl) return;

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

    let modalInstance;
    try {
        modalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
    } catch (e) {
        console.error('Modal init failed:', e);
        return;
    }

    document.addEventListener('click', function (e) {
        const trigger = e.target.closest('[data-bs-toggle="modal"][data-bs-target="#receiptModal"]');
        if (!trigger) return;

        e.preventDefault();
        modalEl.style.display = 'block';
        modalEl.classList.add('show');
        document.body.classList.add('modal-open');

        if (!document.querySelector('.modal-backdrop')) {
            const backdrop = document.createElement('div');
            backdrop.className = 'modal-backdrop fade show';
            document.body.appendChild(backdrop);
        }

        modalInstance.show();
    });

    // --- Filter Dropdown Setup ---
    const filterBtn = document.querySelector('.input-group button[data-bs-target="#filterModal"]');
    const tableBody = document.querySelector('.table tbody');

    if (filterBtn && tableBody) {
        const filterDropdown = document.createElement('div');
        filterDropdown.id = 'customFilterDropdown';
        filterDropdown.className = 'custom-filter-dropdown';
        filterDropdown.style.display = 'none';

        filterDropdown.innerHTML = `
            <button class="btn btn-sm d-block w-100 mb-1" data-sort="az">Sort by Name (A-Z)</button>
            <button class="btn btn-sm d-block w-100" data-sort="date">Sort by Date</button>
        `;

        // Place the dropdown right after the filter button
        filterBtn.parentNode.insertBefore(filterDropdown, filterBtn.nextSibling);

        filterBtn.addEventListener('click', function (e) {
            e.preventDefault();
            filterDropdown.style.display = filterDropdown.style.display === 'none' ? 'block' : 'none';
        });

        document.addEventListener('click', function (e) {
            if (!filterDropdown.contains(e.target) && !filterBtn.contains(e.target)) {
                filterDropdown.style.display = 'none';
            }
        });

        filterDropdown.addEventListener('click', function (e) {
            const button = e.target.closest('button[data-sort]');
            if (!button) return;

            const sortType = button.getAttribute('data-sort');
            const rows = Array.from(tableBody.querySelectorAll('tr'));

            if (sortType === 'az') {
                rows.sort((a, b) => {
                    const nameA = a.querySelector('.patient-info h6')?.textContent.trim().toLowerCase() || '';
                    const nameB = b.querySelector('.patient-info h6')?.textContent.trim().toLowerCase() || '';
                    return nameA.localeCompare(nameB);
                });
            } else if (sortType === 'date') {
                rows.sort((a, b) => {
                    const dateA = new Date(a.children[3].textContent.trim());
                    const dateB = new Date(b.children[3].textContent.trim());
                    return dateA - dateB;
                });
            }

            rows.forEach(row => tableBody.appendChild(row));
            filterDropdown.style.display = 'none';
        });
    }

    // --- Search Bar Logic ---
    const searchInput = document.querySelector('.input-group input[type="text"]');
    const searchBtn = document.querySelector('.input-group button[type="button"]');
    const rows = document.querySelectorAll('.table tbody tr');

    function filterTransactions() {
        const query = searchInput.value.trim().toLowerCase();
        rows.forEach(row => {
            const rowText = row.textContent.toLowerCase();
            row.style.display = rowText.includes(query) ? '' : 'none';
        });
    }

    if (searchInput) {
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') filterTransactions();
        });
    }

    if (searchBtn) {
        searchBtn.addEventListener('click', filterTransactions);
    }
});

// --- SPA Cleanup ---
window.addEventListener('unload', function () {
    const style = document.getElementById('modal-fix-styles');
    if (style) style.remove();
});
