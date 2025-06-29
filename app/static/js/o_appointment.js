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
    dateClick: function (info) {
      const clickedDate = new Date(info.dateStr);
      appointmentDateSpan.textContent = clickedDate.toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      });
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
