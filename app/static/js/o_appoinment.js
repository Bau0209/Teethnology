document.addEventListener('DOMContentLoaded', function () {
  // Elements
  const calendar = document.getElementById('calendar');
  const monthLabel = document.getElementById('calendar-month');
  const yearSelect = document.getElementById('calendar-year');
  const prevBtn = document.getElementById('prev-month');
  const nextBtn = document.getElementById('next-month');
  const addBtn = document.querySelector('#appointmentsModal .btn-add');
  const appointmentForm = document.getElementById('appointmentForm');
  const appointmentsModalEl = document.getElementById('appointmentsModal');
  const addAppointmentModalEl = document.getElementById('addAppointmentModal');
  const requestAddBtn = document.querySelector('.request-add-btn .btn-add'); // Add button in appointment_request.html

  // State
  let today = new Date();
  let currentMonth = today.getMonth();
  let currentYear = today.getFullYear();

  // Helper Functions
  function formatDateForDisplay(dateString) {
    const options = { month: 'long', day: 'numeric', year: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-US', options);
  }

  function populateYearSelect() {
    yearSelect.innerHTML = '';
    for (let y = currentYear - 10; y <= currentYear + 10; y++) {
      const opt = document.createElement('option');
      opt.value = y;
      opt.textContent = y;
      yearSelect.appendChild(opt);
    }
    yearSelect.value = currentYear;
  }

  // Calendar Rendering
  function renderCalendar(month, year) {
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const monthNames = [
      "January", "February", "March", "April", "May", "June",
      "July", "August", "September", "October", "November", "December"
    ];

    monthLabel.textContent = monthNames[month];

    // Generate calendar HTML
    let html = '<table class="calendar-table"><thead><tr>';
    const days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
    days.forEach(d => html += `<th>${d}</th>`);
    html += '</tr></thead><tbody><tr>';

    // Empty cells before first day
    for (let i = 0; i < firstDay; i++) html += '<td></td>';

    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      html += `<td><button class="calendar-day" data-date="${dateStr}">${day}</button></td>`;
      if ((firstDay + day) % 7 === 0) html += '</tr><tr>';
    }

    html += '</tr></tbody></table>';
    calendar.innerHTML = html;

    // Add day button event listeners
    document.querySelectorAll('.calendar-day').forEach(btn => {
      // Hover effects
      btn.addEventListener('mouseenter', () => btn.classList.add('hovered'));
      btn.addEventListener('mouseleave', () => btn.classList.remove('hovered'));

      // Updated click handler with accessibility improvements
      btn.addEventListener('click', () => {
        const date = btn.dataset.date;
        const formattedDate = formatDateForDisplay(date);
        document.getElementById('appointment-date').textContent = formattedDate;

        // Show modal with accessibility considerations
        const modal = new bootstrap.Modal(appointmentsModalEl, {
          backdrop: true,
          keyboard: true,
          focus: true
        });
        modal.show();

        // After modal is shown, move focus to the modal header
        setTimeout(() => {
          const modalTitle = document.querySelector('#appointmentModalLabel');
          if (modalTitle) {
            modalTitle.focus();
          }
        }, 100);
      });
    });
  }

  // Initial Setup
  populateYearSelect();
  renderCalendar(currentMonth, currentYear);

  // Navigation Handlers
  prevBtn.addEventListener('click', () => {
    currentMonth--;
    if (currentMonth < 0) {
      currentMonth = 11;
      currentYear--;
      yearSelect.value = currentYear;
    }
    renderCalendar(currentMonth, currentYear);
  });

  nextBtn.addEventListener('click', () => {
    currentMonth++;
    if (currentMonth > 11) {
      currentMonth = 0;
      currentYear++;
      yearSelect.value = currentYear;
    }
    renderCalendar(currentMonth, currentYear);
  });

  yearSelect.addEventListener('change', () => {
    currentYear = parseInt(yearSelect.value, 10);
    renderCalendar(currentMonth, currentYear);
  });

  // Add button handler for appointments modal
  if (addBtn) {
    addBtn.addEventListener('click', () => {
      const modal = bootstrap.Modal.getInstance(appointmentsModalEl);
      modal.hide(); // Close the appointment modal

      // Open the add appointment modal
      const addModal = new bootstrap.Modal(addAppointmentModalEl, {
        backdrop: true,
        keyboard: true,
        focus: true
      });
      addModal.show();

      // Move focus to first form field when add modal opens
      setTimeout(() => {
        const firstInput = document.querySelector('#addAppointmentModal input');
        if (firstInput) {
          firstInput.focus();
        }
      }, 100);
    });
  }

  // Add button handler in appointment_request.html
  if (requestAddBtn) {
    requestAddBtn.addEventListener('click', () => {
        const addModal = new bootstrap.Modal(addAppointmentModalEl, {
            backdrop: true,
            keyboard: true,
            focus: true
        });
        addModal.show();
        // Move focus to the first form field when add modal opens
        setTimeout(() => {
            const firstInput = document.querySelector('#addAppointmentModal input');
            if (firstInput) {
                firstInput.focus();
            }
        }, 100);
    });
}


  // Form submission with accessibility feedback
  if (appointmentForm) {
    appointmentForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Here you would typically validate and submit the form
      // For accessibility, you should provide success/error feedback

      const modal = bootstrap.Modal.getInstance(addAppointmentModalEl);
      modal.hide();

      // Return focus to the calendar after modal closes
      setTimeout(() => {
        const firstDayBtn = document.querySelector('.calendar-day');
        if (firstDayBtn) {
          firstDayBtn.focus();
        }
      }, 100);
    });
  }

  // Reset form on modal close
  if (addAppointmentModalEl) {
    addAppointmentModalEl.addEventListener('hidden.bs.modal', function () {
      if (appointmentForm) {
        appointmentForm.reset();
      }
    });
  }

  // Reset appointment date on modal close
  if (appointmentsModalEl) {
    appointmentsModalEl.addEventListener('hidden.bs.modal', function () {
      const appointmentDate = document.getElementById('appointment-date');
      if (appointmentDate) {
        appointmentDate.textContent = '';
      }
    });
  }

  // Trap focus inside modals when open (accessibility)
  document.addEventListener('keydown', function(e) {
    const openModal = document.querySelector('.modal.show');
    if (openModal) {
      const focusable = openModal.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      const firstFocusable = focusable[0];
      const lastFocusable = focusable[focusable.length - 1];

      if (e.key === 'Tab') {
        if (e.shiftKey && document.activeElement === firstFocusable) {
          e.preventDefault();
          lastFocusable.focus();
        } else if (!e.shiftKey && document.activeElement === lastFocusable) {
          e.preventDefault();
          firstFocusable.focus();
        }
      }
    }
  });
});
