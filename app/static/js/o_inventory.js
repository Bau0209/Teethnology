//for equipment restock modal
document.addEventListener('DOMContentLoaded', function() {
  // Connect Request Now buttons to the modal
  document.querySelectorAll('.btn-primary').forEach(btn => {
    if (btn.textContent.trim() === 'Request Now') {
      btn.addEventListener('click', function() {
        const row = this.closest('tr');
        const modal = new bootstrap.Modal(document.getElementById('equipmentRestockModal'));
        
        // Populate modal with equipment data
        document.getElementById('equipmentName').value = row.cells[1].textContent;
        document.getElementById('equipmentCode').value = row.cells[0].textContent;
        document.getElementById('equipmentCondition').value = row.cells[6].textContent.trim();
        
        modal.show();
      });
    }
  });
});

//for cosumable, sterilization, lab material and medication restock modal
// Initialize restock modals for all inventory types
document.addEventListener('DOMContentLoaded', function() {
  // Connect Restock buttons to the modal
  document.querySelectorAll('.btn-sm.btn-primary').forEach(btn => {
    if (btn.textContent.trim() === 'Restock') {
      btn.addEventListener('click', function() {
        const row = this.closest('tr');
        const modal = new bootstrap.Modal(document.getElementById('restockModal'));
        
        // Populate modal with item data
        document.getElementById('restockItemName').value = row.cells[1].textContent;
        document.getElementById('restockItemCode').value = row.cells[0].textContent;
        document.getElementById('restockCurrentStock').value = row.cells[2].textContent;
        
        // Determine category based on which page we're on
        const activeTab = document.querySelector('.nav-tabs .nav-link.active').textContent.trim();
        document.getElementById('restockCategory').value = activeTab;
        
        modal.show();
      });
    }
  });
});