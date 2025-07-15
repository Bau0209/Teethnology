document.addEventListener('DOMContentLoaded', function() {
  const calendarEl = document.getElementById('calendar');
  const appointmentInfo = document.querySelector('.appointment-info');
  
  if (!calendarEl) {
    console.error("Calendar element not found!");
    return;
  }

  // Remove any existing custom titles
  const customTitles = document.querySelectorAll('.custom-calendar-title');
  if (customTitles) {
    customTitles.forEach(title => title.remove());
  }

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
      
      // Add dateClick handler
      dateClick: function(info) {
        const selectedDate = info.dateStr;

        // ✅ Skip if the clicked date is in the past
        const today = new Date();
        today.setHours(0, 0, 0, 0); // remove time for accurate comparison
        const clickedDate = new Date(selectedDate);
        
        if (clickedDate < today) {
          return; // ⛔ Do nothing for past dates
        }

        const formattedDate = new Date(selectedDate).toLocaleDateString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric'
        });
        
        // Update the appointment info section
        if (appointmentInfo) {
          appointmentInfo.innerHTML = `
            <h4 class="text-center text-primary fw-bold mb-4">Information</h4>
            <hr>
            <h5 class="text-center text-primary fw-bold mb-4">APPOINTMENT FOR ${formattedDate.toUpperCase()}</h5>
            <p class="fw-bold">Available Time Slots:</p>
            <ul class="list-unstyled">
              <li class="mb-2">8:00am-9:00am</li>
              <li class="mb-2">10:00am-11:00am</li>
              <li class="mb-2">1:00pm-2:00pm</li>
            </ul>
            <button class="book btn btn-primary w-100 py-2" onclick="window.location.href='/form?date=${selectedDate}'">Book Now</button>
          `;
        }
      },
      
      datesSet: function(dateInfo) {
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
          option.selected = year === viewedYear;
          yearSelect.appendChild(option);
        }
        
        yearSelect.addEventListener('change', function() {
          calendar.gotoDate(new Date(parseInt(this.value), calendar.getDate().getMonth(), 1));
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
