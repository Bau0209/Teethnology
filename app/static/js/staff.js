document.addEventListener('DOMContentLoaded', function () {
  const calendarEl = document.getElementById('calendar');
  const appointmentsListEl = document.querySelector('.appointments-sidebar .appointments-list');

  if (!calendarEl || !appointmentsListEl) {
    console.error("Missing calendar or appointments list element.");
    return;
  }

  // Sample appointment data — replace this with real dynamic data if needed
  const appointmentData = [
    {
      appointment_id: 1,
      date: '2025-07-16',
      time: '10:00am - 11:00am',
      patient_name: 'Juan Dela Cruz',
      patient_type: 'New',
      contact: '09123456789',
      email: 'juan@example.com',
      status: 'done'
    },
    {
      appointment_id: 2,
      date: '2025-07-16',
      time: '1:00pm - 2:00pm',
      patient_name: 'Maria Santos',
      patient_type: 'Returning',
      contact: '09123456790',
      email: 'maria@example.com',
      status: 'in-progress'
    },
    {
      appointment_id: 3,
      date: '2025-07-17',
      time: '3:00pm - 4:00pm',
      patient_name: 'Pedro Reyes',
      patient_type: 'New',
      contact: '09123456791',
      email: 'pedro@example.com',
      status: 'not-started'
    }
  ];

  // Remove any existing custom titles
  document.querySelectorAll('.custom-calendar-title').forEach(title => title.remove());

  try {
    const calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      selectable: true,
      events: [],
      headerToolbar: {
        left: 'prev',
        center: 'title',
        right: 'next'
      },
      titleFormat: { month: 'long' },
      height: 'auto',

      // ✅ Show appointments in right panel when date is clicked
      dateClick: function (info) {
        const clickedDate = info.dateStr;

        const matches = appointmentData.filter(a => a.date === clickedDate);
        appointmentsListEl.innerHTML = ''; // Clear old items

        if (matches.length === 0) {
          appointmentsListEl.innerHTML = '<p class="text-muted px-2">No appointments on this date.</p>';
        } else {
          matches.forEach(a => {
            const item = document.createElement('div');
            item.classList.add('appointment-item');

            // 🟢 Add status class
            if (a.status === 'done') {
              item.classList.add('done');
            } else if (a.status === 'in-progress') {
              item.classList.add('in-progress');
            } else {
              item.classList.add('not-started');
            }

            const finalUrl = appointmentDetailUrl.replace('__ID__', a.appointment_id);
            item.innerHTML = `
              <div class="appointment-time">${a.time}</div>
              <div class="appointment-name">${a.patient_name}</div>
              <a href="${finalUrl}" class="view-details">View Details</a>
            `;
            appointmentsListEl.appendChild(item);
          });
        }
      },

      // Preserve custom toolbar title
      datesSet: function (dateInfo) {
        const titleEl = document.querySelector('.fc-toolbar-title');
        if (!titleEl) return;

        titleEl.innerHTML = '';

        const monthSpan = document.createElement('span');
        monthSpan.className = 'fc-month-display';
        monthSpan.textContent = dateInfo.view.currentStart
          .toLocaleDateString('default', { month: 'long' })
          .toUpperCase();

        const yearSelect = document.createElement('select');
        yearSelect.className = 'fc-year-select';

        const currentYear = new Date().getFullYear();
        const viewedYear = dateInfo.view.currentStart.getFullYear();

        for (let year = currentYear - 10; year <= currentYear + 10; year++) {
          const option = document.createElement('option');
          option.value = year;
          option.textContent = year;
          if (year === viewedYear) option.selected = true;
          yearSelect.appendChild(option);
        }

        yearSelect.addEventListener('change', function () {
          const newDate = new Date(parseInt(this.value), calendar.getDate().getMonth(), 1);
          calendar.gotoDate(newDate);
        });

        titleEl.appendChild(monthSpan);
        titleEl.appendChild(yearSelect);
      }
    });

    calendar.render();
  } catch (error) {
    console.error("Error initializing calendar:", error);
  }
});
