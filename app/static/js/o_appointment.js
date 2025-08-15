// Confirmation function for reject
window.confirmReject = function (appointmentId) {
  if (confirm("Are you sure you want to reject this appointment?")) {
    handleCancel(appointmentId);
  }
};

// Simple confirmation for cancel
window.confirmCancel = function (appointmentId) {
  if (confirm("Are you sure you want to cancel this appointment?")) {
    handleCancel(appointmentId);
  }
};

// Confirmation function for accept
window.confirmAccept = function (appointmentId) {
  if (confirm("Are you sure you want to accept this appointment?")) {
    handleAccept(appointmentId);
  }
};

function handleAccept(id) {
  fetch(`/dashboard/appointments/${id}/status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status: 'approved' }),
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert('Appointment approved!');
      location.reload();
    } else {
      alert(data.message);
    }
  })
  .catch(err => {
    alert('An error occurred. Please try again.');
    console.error(err);
  });
}

function handleComplete(appointmentId, branchId) {
  // Store appointment ID
  document.getElementById('complete-appointment-id').value = appointmentId;

  // Reset form
  document.getElementById('completeProcedureForm').reset();

  // Fetch filtered inventory for this branch
  fetch(`/dashboard/appointment/inventory/${branchId}`)
    .then(res => res.json())
    .then(data => {
      const tbody = document.querySelector('#completeProcedureModal tbody');
      tbody.innerHTML = '';
      data.forEach(item => {
        tbody.innerHTML += `
          <tr>
            <td>${item.item_name}</td>
            <td>
              <input type="number" 
                     name="quantity_used[${item.id}]" 
                     class="form-control" 
                     min="0" step="0.01" value="0">
            </td>
            <td>${item.quantity_unit}</td>
          </tr>
        `;
      });

      // Show modal after loading inventory
      const modal = new bootstrap.Modal(document.getElementById('completeProcedureModal'));
      modal.show();
    });
}

function handleCancel(id) {
  fetch(`/dashboard/cancel_appointment/${id}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert('Appointment cancelled and archived!');
      location.reload();
    } else {
      alert(data.message || 'Failed to cancel appointment');
    }
  })
  .catch(err => {
    alert('An error occurred. Please try again.');
    console.error(err);
  });
}

document.addEventListener('DOMContentLoaded', function () {
  // =====================
  // FullCalendar Setup
  // =====================
  const calendarEl = document.getElementById('calendar');
  const appointmentsModalEl = document.getElementById('appointmentsModal');
  const appointmentDateSpan = document.getElementById('appointment-date');

  document.querySelectorAll('.custom-calendar-title').forEach(title => title.remove());

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    selectable: true,
    events: dynamicEvents.filter(event => event.extendedProps?.status !== 'cancelled'),
    eventDidMount: function(info) {
        const { patient, type } = info.event.extendedProps;
        info.el.querySelector('.fc-event-title').innerHTML = `${patient}<br>${type}`;
    },
  dateClick: function (info) {
    const clickedDate = info.dateStr;

    // Set modal date
    appointmentDateSpan.textContent = new Date(clickedDate).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });

    const modalBody = appointmentsModalEl.querySelector('.modal-body');
    modalBody.innerHTML = ''; // Clear existing content

    const matches = appointmentData.filter(a => a.date === clickedDate && a.status !== 'cancelled');

    if (matches.length === 0) {
      modalBody.innerHTML = '<p class="text-muted">No appointments on this date.</p>';
    } else {
      matches.forEach(a => {
        const item = document.createElement('div');
        item.classList.add('appointment-item');
        item.style.cursor = 'pointer';

        let buttonsHTML = '';

        if (a.status === 'pending') {
          buttonsHTML = `
            <div class="d-flex gap-2 mt-3">
              <button class="btn btn-success btn-sm" onclick="confirmAccept(${a.appointment_id})">Accept</button>
              <button class="btn btn-danger btn-sm reject-btn" onclick="confirmReject(${a.appointment_id})">Reject</button>
            </div>
          `;
        } else {
          if (a.procedure_status === 'completed') {
            buttonsHTML = `
              <div class="mt-3">
                <span class="badge bg-success text-white px-3 py-2 fs-6">✔ Procedure Completed</span>
              </div>
            `;

          } else {
            buttonsHTML = `
              <div class="d-flex gap-2 mt-3">
                <button class="btn btn-primary btn-sm" onclick="handleComplete(${a.appointment_id}, ${a.branch_id})">Mark as Completed</button>
                <button class="btn btn-warning btn-sm" onclick="handleReschedule(${a.appointment_id})">Reschedule</button>
                <button class="btn btn-danger btn-sm" onclick="confirmCancel(${a.appointment_id})">Cancel</button>
              </div>
            `;
          }
        }


        item.innerHTML = `
          <div class="request-section-title" style="margin-bottom: 0;">
            ${a.branch_name} - ${a.time} - ${a.reason}
          </div>
          <div class="appointment-status-label" style="font-size: 0.9rem; font-weight: 500; color: #6c757d;">
            ${a.status || 'No Status'}
          </div>
          <br>
          <div><b>Date:</b> ${a.date}</div>
          <div><b>Time:</b> ${a.time}</div>
          <div><b>Patient Name:</b> ${a.patient_name}</div>
          <div><b>Patient Type:</b> ${a.patient_type}</div>
          <div><b>Contact:</b> ${a.contact}</div>
          <div><b>Email:</b> ${a.email}</div>
          ${buttonsHTML}
          <hr>
        `;

        modalBody.appendChild(item);
      });
    }
  // Automatically set the preferred date in the Add Appointment Modal
  const preferredInput = document.getElementById('preferred');
  if (preferredInput) {
    const date = new Date(info.date);
    date.setHours(9, 0, 0, 0);  // Set default time to 09:00
    preferredInput.value = date.toISOString().slice(0, 16); // Format: yyyy-MM-ddTHH:mm
  }

  // SHOW THE MODAL
  const modal = new bootstrap.Modal(appointmentsModalEl);
  modal.show();
},
    headerToolbar: {
      left: 'prev',
      center: 'title',
      right: 'next'
    },
    titleFormat: { month: 'long' },
    height: 'auto',
    datesSet: function (dateInfo) {
      const titleEl = document.querySelector('.fc-toolbar-title');
      if (titleEl) {
        titleEl.innerHTML = '';

        const monthSpan = document.createElement('span');
        monthSpan.className = 'fc-month-display';
        monthSpan.textContent = dateInfo.view.currentStart
          .toLocaleString('default', { month: 'long' })
          .toUpperCase();

        const yearSelect = document.createElement('select');
        yearSelect.className = 'fc-year-select';

        const currentYear = new Date().getFullYear();
        const viewedYear = dateInfo.view.currentStart.getFullYear();

        for (let year = currentYear - 10; year <= currentYear + 10; year++) {
          const option = document.createElement('option');
          option.value = year;
          option.textContent = year;
          option.selected = year === viewedYear;
          yearSelect.appendChild(option);
        }

        yearSelect.addEventListener('change', function () {
          const newDate = new Date(parseInt(this.value), calendar.getDate().getMonth(), 1);
          calendar.gotoDate(newDate);
        });

        titleEl.appendChild(monthSpan);
        titleEl.appendChild(yearSelect);
      }
    }
  });

  calendar.render();

  // =====================
  // Modal "Add" Button Handler Setup
  // =====================
  const addAppointmentModalEl = document.getElementById('addAppointmentModal');
  if (!addAppointmentModalEl) return;

  const addAppointmentModal = new bootstrap.Modal(addAppointmentModalEl);

  function bindAddButtonHandler() {
    const addButtonLink = document.querySelector('.request-add-btn a');
    if (addButtonLink && !addButtonLink.dataset.bound) {
      addButtonLink.dataset.bound = 'true';
      addButtonLink.addEventListener('click', function (e) {
        e.preventDefault();
        addAppointmentModal.show();
      });
    }
  }

  bindAddButtonHandler(); // Try immediately

  const observer = new MutationObserver(() => {
    bindAddButtonHandler(); // Re-bind if dynamically added
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.querySelector('.input-group input');
  const searchBtn = document.querySelector('.input-group button');

  function filterAppointments() {
    const query = searchInput.value.toLowerCase().trim();
    const requests = document.querySelectorAll('.request-table');

    requests.forEach(request => {
      const nameDiv = request.querySelector('.request-patient b')?.nextSibling;
      const patientName = nameDiv?.textContent?.toLowerCase().trim() || '';

      if (patientName.includes(query)) {
        request.style.display = '';
      } else {
        request.style.display = 'none';
      }
    });
  }

  // On Enter key press in search input
  searchInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      filterAppointments();
    }
  });

  // On click of search button
  searchBtn.addEventListener('click', function () {
    filterAppointments();
  });
});

// Handles reschedule appointment confirmation
function handleReschedule(appointmentId) {
  // Hide the current appointment details modal
  const appointmentModalEl = document.getElementById('appointmentsModal');
  const appointmentModal = bootstrap.Modal.getInstance(appointmentModalEl);
  if (appointmentModal) {
    appointmentModal.hide();

    // After modal is hidden, open the Book Appointment modal
    appointmentModalEl.addEventListener('hidden.bs.modal', function onHidden() {
      appointmentModalEl.removeEventListener('hidden.bs.modal', onHidden);

      const bookModalEl = document.getElementById('addAppointmentModal');
      const bookModal = new bootstrap.Modal(bookModalEl);
      bookModal.show();

      // Optional: Pre-fill appointment ID if needed
      const hiddenIdField = document.getElementById('reschedule-appointment-id');
      if (hiddenIdField) {
        hiddenIdField.value = appointmentId;
      }
    });
  } else {
    // Fallback: Just open the form directly
    const bookModalEl = document.getElementById('addAppointmentModal');
    const bookModal = new bootstrap.Modal(bookModalEl);
    bookModal.show();
  }
}
