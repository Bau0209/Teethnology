document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  const appointmentsModalEl = document.getElementById('appointmentsModal');
  const appointmentDateSpan = document.getElementById('appointment-date');

  // Remove any existing custom titles
  document.querySelectorAll('.custom-calendar-title').forEach(title => title.remove());

  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    selectable: true,
    dateClick: function(info) {
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
    titleFormat: { month: 'long' }, // Only show month in default title
    height: 'auto',
    datesSet: function(dateInfo) {
      const titleEl = document.querySelector('.fc-toolbar-title');
      if (titleEl) {
        // Clear existing and create new elements
        titleEl.innerHTML = '';
        
        // Month element (uppercase)
        const monthSpan = document.createElement('span');
        monthSpan.className = 'fc-month-display';
        monthSpan.textContent = dateInfo.view.currentStart
          .toLocaleString('default', { month: 'long' })
          .toUpperCase();
        
        // Year dropdown element
        const yearSelect = document.createElement('select');
        yearSelect.className = 'fc-year-select';
        
        // Add year options (current year ±5 years)
        const currentYear = new Date().getFullYear();
        const viewedYear = dateInfo.view.currentStart.getFullYear();
        
        for (let year = currentYear - 25; year <= currentYear + 5; year++) {
          const option = document.createElement('option');
          option.value = year;
          option.textContent = year;
          option.selected = year === viewedYear;
          yearSelect.appendChild(option);
        }
        
        // Handle year change
        yearSelect.addEventListener('change', function() {
          const newDate = new Date(
            parseInt(this.value),
            calendar.getDate().getMonth(),
            1
          );
          calendar.gotoDate(newDate);
        });
        
        titleEl.appendChild(monthSpan);
        titleEl.appendChild(yearSelect);
      }
    }
  });

  calendar.render();
});