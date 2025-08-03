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

function handleReject(id) {
  fetch(`/dashboard/appointments/${id}/status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status: 'cancelled' }),
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert('Appointment rejected!');
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

function handleComplete(appointmentId) {
  // Store appointment ID in a hidden field
  document.getElementById('complete-appointment-id').value = appointmentId;

  // Reset modal form
  document.getElementById('completeProcedureForm').reset();

  // Show modal
  const modal = new bootstrap.Modal(document.getElementById('completeProcedureModal'));
  modal.show();
}


function handleCancel(appointmentId) {
  fetch(`/dashboard/cancel_appointment/${appointmentId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    }
  })
  .then(res => {
    if (!res.ok) {
      throw new Error('Failed to cancel appointment');
    }
    return res.json();
  })
  .then(data => {
    if (data.success) {
      alert('Appointment cancelled and archived!');
      
      // Remove the appointment card from UI without reload
      const appointmentCard = document.querySelector(`[data-appointment-id="${appointmentId}"]`);
      if (appointmentCard) {
        appointmentCard.remove();
      }
      
      // Close any open modals
      const modal = bootstrap.Modal.getInstance(document.getElementById('appointmentsModal'));
      if (modal) modal.hide();
    } else {
      alert(data.message || 'Failed to cancel appointment');
    }
  })
  .catch(err => {
    alert(err.message || 'An error occurred during cancellation');
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
    events: dynamicEvents,
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

    const matches = appointmentData.filter(a => a.date === clickedDate);

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
              <button class="btn btn-success btn-sm" onclick="handleAccept(${a.appointment_id})">Accept</button>
              <button class="btn btn-danger btn-sm" onclick="handleReject(${a.appointment_id})">Reject</button>
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
                <button class="btn btn-primary btn-sm" onclick="handleComplete(${a.appointment_id})">Mark as Completed</button>
                <button class="btn btn-warning btn-sm" onclick="handleReschedule(${a.appointment_id})">Reschedule</button>
                <button class="btn btn-danger btn-sm" onclick="handleCancel(${a.appointment_id})">Cancel</button>
              </div>
            `;
          }
        }


        item.innerHTML = `
          <div class="request-section-title" style="margin-bottom: 0;">
            ${a.time} - ${a.reason}
          </div>
          <div class="appointment-status-label" style="font-size: 0.9rem; font-weight: 500; color: #6c757d;">
            ${a.status || 'No Status'}
          </div>
          <br>
          <div><b>Date:</b> ${a.date}</div>
          <div><b>Time:</b> ${a.time}</div>
          <div><b>Alternative Date / Time:</b> ${a.alternative_sched || 'None'}</div>
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

// Handles reject appointment confirmation
document.addEventListener('DOMContentLoaded', function () {
  // Inject rejection confirmation modal
  const rejectConfirmModalHTML = `
    <div class="modal fade" id="rejectConfirmModal" tabindex="-1" aria-labelledby="rejectConfirmModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="background: #00898E; color: white;">
            <h5 class="modal-title">Confirm Rejection</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to reject this appointment?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-danger" id="btnConfirmReject">Yes</button>
          </div>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', rejectConfirmModalHTML);

  const rejectModal = new bootstrap.Modal(document.getElementById('rejectConfirmModal'));
  let rejectId = null;
  let rejectCard = null;

  document.querySelectorAll('button.btn-danger.btn-sm').forEach(btn => {
    if (btn.textContent.trim() === 'Reject') {
      const originalOnClick = btn.getAttribute('onclick');
      const match = originalOnClick?.match(/\d+/);
      if (!match) return;

      const id = parseInt(match[0]);
      btn.removeAttribute('onclick');

      btn.addEventListener('click', function () {
        rejectId = id;
        rejectCard = btn.closest('.request-table');
        rejectModal.show();
      });
    }
  });

document.getElementById('btnConfirmReject').addEventListener('click', function () {
  if (!rejectId) return;

  fetch(`/dashboard/appointments/${rejectId}/status`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status: 'cancelled', allowWithoutProcedure: true }), //  ensures rejection proceeds
  })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        alert('Appointment rejected!');
        if (rejectCard) rejectCard.remove();

        // Remove the appointment item from the list
        const appointmentItems = document.querySelectorAll('.appointment-item');
        appointmentItems.forEach(item => {
          if (item.innerHTML.includes(`handleReject(${rejectId})`)) {
            item.remove();
          }
        });
      } else {
        alert(data.message);
      }
      rejectModal.hide();
    })
    .catch(err => {
      alert('An error occurred. Please try again.');
      console.error(err);
      rejectModal.hide();
    });
});
});


// Handles cancel appointment confirmation
document.addEventListener('DOMContentLoaded', function () {
  const cancelConfirmModalHTML = `
    <div class="modal fade" id="cancelConfirmModal" tabindex="-1" aria-labelledby="cancelConfirmModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header" style="background: #00898E; color: white;">
            <h5 class="modal-title">Confirm Cancellation</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to cancel this procedure?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
            <button type="button" class="btn btn-primary" id="btnSetNewAppointment">Set a New Appointment</button>
            <button type="button" class="btn btn-danger" id="btnConfirmCancel">Yes, Cancel</button>
          </div>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', cancelConfirmModalHTML);

  const cancelModal = new bootstrap.Modal(document.getElementById('cancelConfirmModal'));
  let cancelId = null;

  // Intercept Cancel buttons
  const observer = new MutationObserver(() => {
    document.querySelectorAll('button.btn-danger.btn-sm').forEach(btn => {
      if (btn.textContent.trim() === 'Cancel' && !btn.dataset.bound) {
        const originalOnClick = btn.getAttribute('onclick');
        const match = originalOnClick?.match(/\d+/);
        if (!match) return;

        const id = parseInt(match[0]);
        btn.removeAttribute('onclick');
        btn.dataset.bound = 'true';

        btn.addEventListener('click', function () {
          cancelId = id;

          // Hide the appointment details modal before showing confirmation
          const appointmentModal = document.getElementById('appointmentsModal');
          const bsApptModal = bootstrap.Modal.getInstance(appointmentModal);
          if (bsApptModal) {
            bsApptModal.hide();
            appointmentModal.addEventListener('hidden.bs.modal', function onHidden() {
              appointmentModal.removeEventListener('hidden.bs.modal', onHidden);
              cancelModal.show();
            });
          } else {
            cancelModal.show(); // fallback if no modal instance
          }
        });
      }
    });
  });

  observer.observe(document.body, { childList: true, subtree: true });

  // Confirm cancel
  document.getElementById('btnConfirmCancel').addEventListener('click', function() {
  if (!cancelId) return;

  fetch(`/dashboard/cancel_appointment/${cancelId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  })
  .then(res => {
    if (!res.ok) throw new Error('Failed to cancel appointment');
    return res.json();
  })
  .then(data => {
    if (data.success) {
      alert('Appointment cancelled and archived!');
      
      // Remove from UI
      console.log('Removing element:', document.querySelector(`[data-appointment-id="${appointmentId}"]`));
      
      // Close modals
      cancelModal.hide();
      const appointmentModal = bootstrap.Modal.getInstance(
        document.getElementById('appointmentsModal')
      );
      if (appointmentModal) appointmentModal.hide();
    } else {
      alert(data.message || 'Failed to cancel appointment');
    }
  })
  .catch(err => {
    alert(err.message || 'An error occurred. Please try again.');
    console.error(err);
    cancelModal.hide();
  });
});

  // Set new appointment button logic
  document.getElementById('btnSetNewAppointment').addEventListener('click', function () {
    cancelModal.hide();

    const formModal = document.getElementById('addAppointmentModal');
    if (formModal) {
      const bsModal = new bootstrap.Modal(formModal);
      bsModal.show();
    }
  });
});
