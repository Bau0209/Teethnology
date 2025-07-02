function handleAccept(id) {
  fetch(`/owner/appointments/${id}/status`, {
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
  fetch(`/owner/appointments/${id}/status`, {
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
  fetch(`/owner/procedures/${appointmentId}/status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status: 'completed' }),
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert('Procedure marked as completed.');
      location.reload();
    } else {
      alert(data.message);
    }
  })
  .catch(err => {
    alert('An error occurred.');
    console.error(err);
  });
}

function handleCancel(appointmentId) {
  fetch(`/owner/procedures/${appointmentId}/status`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status: 'cancelled' }),
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      alert('Procedure cancelled.');
      location.reload();
    } else {
      alert(data.message);
    }
  })
  .catch(err => {
    alert('An error occurred.');
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
          const isDisabled = a.status === 'cancelled' ? 'disabled' : '';

          buttonsHTML = `
            <div class="d-flex gap-2 mt-3">
              <button class="btn btn-success btn-sm" ${isDisabled} onclick="handleComplete(${a.appointment_id})">Completed</button>
              <button class="btn btn-danger btn-sm" ${isDisabled} onclick="handleCancel(${a.appointment_id})">Cancel</button>
            </div>
          `;
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

    new bootstrap.Modal(appointmentsModalEl).show();
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
