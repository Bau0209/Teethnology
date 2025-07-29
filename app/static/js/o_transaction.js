document.addEventListener('DOMContentLoaded', function () {
    // ===== Payment History Modal Functionality =====
    document.addEventListener('click', function(e) {
        const viewPaymentBtn = e.target.closest('.view-payment-btn');
        if (!viewPaymentBtn) return;
        
        e.preventDefault();
        const patientId = viewPaymentBtn.closest('tr').getAttribute('data-patient-id');
        
        // Update modal title
        const modalTitle = document.getElementById('paymentHistoryModalLabel');
        if (modalTitle) {
            modalTitle.textContent = `Payment History for Patient ID: ${patientId}`;
        }
        
        // Filter table rows to show only this patient's records
        const tableRows = document.querySelectorAll('#paymentHistoryModal tbody tr');
        tableRows.forEach(row => {
            const rowPatientId = row.querySelector('td:first-child').textContent;
            row.style.display = (rowPatientId === patientId) ? '' : 'none';
        });
        
        // Show the modal using Bootstrap's proper method
        try {
            const paymentModal = bootstrap.Modal.getOrCreateInstance(document.getElementById('paymentHistoryModal'));
            paymentModal.show();
        } catch (error) {
            console.error('Failed to show payment modal:', error);
        }
    });

    // --- Modal Initialization ---
    const modalEl = document.getElementById('receiptModal');
    let modalInstance;

    if (modalEl) {
        try {
            // Initialize modal properly
            modalInstance = bootstrap.Modal.getOrCreateInstance(modalEl);
        } catch (e) {
            console.error('Modal init failed:', e);
            return;
        }

        document.addEventListener('click', function (e) {
            const trigger = e.target.closest('[data-bs-toggle="modal"][data-bs-target="#receiptModal"]');
            if (!trigger) return;

            e.preventDefault();
            modalInstance.show(); // Let Bootstrap handle the modal display
        });
    }

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

    // --- Export and Print in Payment History Modal ---
    document.querySelectorAll('[id^="paymentHistoryModal"]').forEach(modal => {
        const exportPdfBtn = modal.querySelector('#exportBtn');
        const printBtn = modal.querySelector('#printBtn');

        if (exportPdfBtn) {
            exportPdfBtn.addEventListener('click', function () {
                try {
                    if (typeof jsPDF === 'undefined') {
                        throw new Error('jsPDF library not loaded');
                    }
                    const doc = new jsPDF('l', 'pt', 'a4');
                    const table = modal.querySelector('table');
                    if (table) {
                        doc.autoTable({ html: table });
                        doc.save('payment-history.pdf');
                    }
                } catch (error) {
                    console.error('PDF export failed:', error);
                    alert('Could not generate PDF. Please make sure jsPDF is loaded and try again.');
                }
            });
        }

        if (printBtn) {
            printBtn.addEventListener('click', function () {
                try {
                    const printContent = modal.querySelector('.modal-body').innerHTML;
                    const win = window.open('', '', 'width=1024,height=768');
                    win.document.write(`
                        <html>
                            <head>
                                <title>Print - Payment History</title>
                                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
                                <style>
                                    body { padding: 20px; font-size: 12px; }
                                    table { width: 100%; border-collapse: collapse; }
                                </style>
                            </head>
                            <body>
                                <h4>Payment History / Transaction Log</h4>
                                ${printContent}
                            </body>
                        </html>
                    `);
                    win.document.close();
                    win.focus();
                    setTimeout(() => {
                        win.print();
                        win.close();
                    }, 200);
                } catch (error) {
                    console.error('Print failed:', error);
                    alert('Printing failed. Please try again.');
                }
            });
        }
    });
});

// Cleanup on page navigation
window.addEventListener('pagehide', function () {
    const style = document.getElementById('modal-fix-styles');
    if (style) style.remove();
});