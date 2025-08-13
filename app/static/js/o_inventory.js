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

 // Simple increment/decrement for quantity input
  document.addEventListener('DOMContentLoaded', function() {
    const qtyInput = document.getElementById('restockQuantity');
    document.getElementById('decrementQty').onclick = function() {
      if (qtyInput.value > 1) qtyInput.value--;
    };
    document.getElementById('incrementQty').onclick = function() {
      qtyInput.value++;
    };
  });

  // Function to handle the restock modal
function handleRestock(event, itemId) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    fetch(`/dashboard/restock/${itemId}`, {  // Note the /dashboard/ prefix
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Close modal
            const modalEl = document.getElementById(`restockModal-${itemId}`);
            const modal = bootstrap.Modal.getInstance(modalEl);
            modal.hide();
            
            // Update table row
            updateTableRow(itemId, data);
            
            // Show success message
            showToast('Item restocked successfully!');
            
            // Redirect back to the original tab
            if (data.current_tab) {
                const tabLink = document.querySelector(`.nav-tabs .nav-link[href="#${data.current_tab}"]`);
                if (tabLink) {
                    new bootstrap.Tab(tabLink).show();
                }
            }
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while restocking the item');
    });
}

function updateTableRow(itemId, data) {
    const row = document.querySelector(`tr[data-item-id="${itemId}"]`);
    if (!row) return;
    
    // Update quantity
    const quantityCell = row.querySelector('.quantity-cell');
    if (quantityCell) {
        quantityCell.textContent = `${data.new_quantity} ${data.quantity_unit || ''}`;
    }
    
    // Update status
    const statusCell = row.querySelector('.status-cell');
    if (statusCell) {
        const badge = statusCell.querySelector('.badge');
        if (badge) {
            badge.className = `badge bg-${data.is_low_stock ? 'danger' : 'success'}`;
            badge.textContent = data.is_low_stock ? 'Low Stock' : 'In Stock';
        }
    }
    
    // Update dates
    const restockDateCell = row.querySelector('.restock-date-cell');
    if (restockDateCell && data.last_restock_date) {
        restockDateCell.textContent = formatDate(data.last_restock_date);
    }
    
    const expDateCell = row.querySelector('.expiration-date-cell');
    if (expDateCell && data.expiration_date) {
        expDateCell.textContent = formatDate(data.expiration_date);
    }
}
