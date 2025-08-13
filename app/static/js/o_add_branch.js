// Handle image upload and preview
    document.getElementById('imageUpload').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('imagePreview');
                preview.src = e.target.result;
                preview.style.display = 'block';
                
                // Hide the upload button text
                document.querySelector('.btn-upload').style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    });
    
    // You can add form submission logic here
    document.querySelector('.btn-add').addEventListener('click', function() {
        // Add your form submission logic here
        alert('Branch added!');
        // Then close the modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addBranchModal'));
        modal.hide();
    });

// Open the archive modal
let archiveBranchId = null;

// Call this when archive button is clicked
function openArchiveModal(branchId) {
  archiveBranchId = branchId;

  const modal = new bootstrap.Modal(document.getElementById('archiveBranchModal'));
  modal.show();
}

