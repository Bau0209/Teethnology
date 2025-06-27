document.addEventListener('DOMContentLoaded', function() {
  
  /**
   * Makes API calls and handles responses
   * @param {string} url - API endpoint
   * @param {string} method - HTTP method (GET, POST, etc.)
   * @param {object} data - Request payload
   */
  function makeApiCall(url, method = 'GET', data = null) {
    const options = {
      method,
      headers: { 'Content-Type': 'application/json' }
    };
    
    if (data) {
      options.body = JSON.stringify(data);
    }
    
    return fetch(url, options)
      .then(handleResponse)
      .catch(handleError);
  }

  /**
   * Shows a Bootstrap toast notification
   * @param {string} message - Notification text
   * @param {string} type - success/error/warning/info
   */
  function showToast(message, type = 'success') {
    const toastEl = document.getElementById('toastNotification');
    const toast = new bootstrap.Toast(toastEl);
    
    // Set toast content and classes
    toastEl.querySelector('.toast-body').textContent = message;
    toastEl.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-info');
    toastEl.classList.add(`bg-${type}`);
    
    toast.show();
  }

  /**
   * Toggles loading state for buttons
   * @param {HTMLElement} button - Button element
   * @param {boolean} isLoading - Loading state
   */
  function toggleLoading(button, isLoading) {
    if (isLoading) {
      button.setAttribute('data-original-text', button.textContent);
      button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
      button.disabled = true;
    } else {
      button.textContent = button.getAttribute('data-original-text');
      button.disabled = false;
    }
  }

  /**
   * Initializes all modal triggers
   */
  function initModals() {
    // Equipment Details Modal
    document.querySelectorAll('[data-bs-toggle="modal"]').forEach(link => {
      link.addEventListener('click', handleModalTrigger);
    });

    // Chevron-right button for showing both modals
    document.querySelectorAll('.bi-chevron-right').forEach(button => {
      button.addEventListener('click', showBothModals);
    });

    // Restock modals
    document.querySelectorAll('.btn-sm.btn-primary').forEach(button => {
      if (button.textContent.trim() === 'Request Now') {
        button.addEventListener('click', initEquipmentRestockModal);
      } else if (button.textContent.trim() === 'Restock') {
        button.addEventListener('click', initGeneralRestockModal);
      }
    });
  }

  /**
   * Shows both equipment and inventory modals
   */
  function showBothModals() {
    const equipmentModal = new bootstrap.Modal(document.getElementById('o_in_eq_full_details'));
    const inventoryModal = new bootstrap.Modal(document.getElementById('o_in_full_details_modal'));
    
    equipmentModal.show();
    inventoryModal.show();
    
    // Optional: Load data for both modals
    loadEquipmentDetails();
    loadInventoryDetails();
  }

  /**
   * Handles modal trigger click events
   */
  function handleModalTrigger(event) {
    const target = this.getAttribute('data-bs-target');
    if (!target) return;
    
    const itemId = target.split('-').pop();
    const isEquipment = target.includes('equipmentDetailsModal');
    
    if (isEquipment) {
      loadEquipmentDetails(itemId);
    } else {
      loadItemDetails(itemId);
    }
  }

  /**
   * Loads equipment details via API
   */
  function loadEquipmentDetails(itemId) {
    // makeApiCall(`/api/equipment/${itemId}`)
    //   .then(data => populateEquipmentModal(data));
    console.log(`Loading equipment details for ID: ${itemId}`);
  }

  /**
   * Loads inventory details via API
   */
  function loadInventoryDetails(itemId) {
    // makeApiCall(`/api/inventory/${itemId}`)
    //   .then(data => populateInventoryModal(data));
    console.log(`Loading inventory details for ID: ${itemId}`);
  }

  /**
   * Handles API response
   */
  function handleResponse(response) {
    if (!response.ok) {
      return response.json().then(err => Promise.reject(err));
    }
    return response.json();
  }
  
  /**
   * Handles errors from API calls
   */
  function handleError(error) {
    console.error('API Error:', error);
    showToast(error.message || 'An error occurred', 'error');
    throw error;
  }

  /**
   * Formats date to local string
   */
  function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString();
  }

  /**
   * Debounce function for search inputs
   */
  function debounce(func, wait) {
    let timeout;
    return function(...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }

  // Initialize all modal functionality
  initModals();
});