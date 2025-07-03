document.addEventListener('DOMContentLoaded', function() {
    // Calendar functionality
    let currentDate = new Date();
    let selectedDate = null;
    
    const monthYearElement = document.getElementById('currentMonthYear');
    const calendarBody = document.getElementById('calendarBody');
    const selectedDateElement = document.getElementById('selectedDate');
    const prevMonthButton = document.getElementById('prevMonth');
    const nextMonthButton = document.getElementById('nextMonth');
    
    // Generate calendar
    function generateCalendar() {
        // Clear previous calendar
        calendarBody.innerHTML = '';
        
        // Set month and year header
        const monthNames = ["January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"];
        monthYearElement.textContent = `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
        
        // Get first day of month and total days in month
        const firstDay = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).getDay();
        const daysInMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
        
        let date = 1;
        
        // Create calendar rows
        for (let i = 0; i < 6; i++) {
            // Stop if we've gone through all days
            if (date > daysInMonth) break;
            
            const row = document.createElement('tr');
            
            // Create cells for each day of the week
            for (let j = 0; j < 7; j++) {
                const cell = document.createElement('td');
                
                if (i === 0 && j < firstDay) {
                    // Empty cells before first day of month
                    cell.textContent = '';
                } else if (date > daysInMonth) {
                    // Empty cells after last day of month
                    cell.textContent = '';
                } else {
                    // Cells with dates
                    cell.textContent = date;
                    cell.classList.add('calendar-day');
                    
                    // Highlight today
                    const today = new Date();
                    if (date === today.getDate() && 
                        currentDate.getMonth() === today.getMonth() && 
                        currentDate.getFullYear() === today.getFullYear()) {
                        cell.classList.add('bg-primary', 'text-white', 'rounded-circle');
                    }
                    
                    // Add click event
                    cell.addEventListener('click', function() {
                        selectDate(this, date);
                    });
                    
                    date++;
                }
                
                row.appendChild(cell);
            }
            
            calendarBody.appendChild(row);
        }
    }
    
    // Select date function
    function selectDate(cell, day) {
        // Remove previous selection
        const selectedCells = document.querySelectorAll('.selected');
        selectedCells.forEach(c => c.classList.remove('selected', 'bg-info', 'text-white', 'rounded-circle'));
        
        // Add selection to clicked cell
        cell.classList.add('selected', 'bg-info', 'text-white', 'rounded-circle');
        
        // Update selected date display
        const monthNames = ["January", "February", "March", "April", "May", "June",
                          "July", "August", "September", "October", "November", "December"];
        selectedDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), day);
        selectedDateElement.textContent = `${monthNames[selectedDate.getMonth()]} ${day}, ${selectedDate.getFullYear()}`;
    }
    
    // Month navigation
    prevMonthButton.addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() - 1);
        generateCalendar();
    });
    
    nextMonthButton.addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() + 1);
        generateCalendar();
    });
    
    // Initialize calendar
    generateCalendar();
});