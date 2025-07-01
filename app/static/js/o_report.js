class DateSelector {
  constructor(container) {
    this.container = document.querySelector(container);
    this.currentYear = new Date().getFullYear();
    this.currentMonth = new Date().getMonth();
    this.currentDayRange = '1-25';
    
    // Initialize
    this.initYears();
    this.initMonths();
    this.initDayRanges();
    this.setupEventListeners();
  }
  
  initYears() {
    const dropdown = this.container.querySelector('.year-dropdown');
    const years = [2023, 2024, 2025, 2026];
    
    dropdown.innerHTML = years.map(year => `
      <li>
        <a class="dropdown-item ${year === this.currentYear ? 'active' : ''}" 
           href="#" data-year="${year}">
          ${year}-${year}
        </a>
      </li>
    `).join('');
  }
  
  initMonths() {
    const dropdown = this.container.querySelector('.month-dropdown');
    const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
    
    dropdown.innerHTML = months.map((month, index) => `
      <li>
        <a class="dropdown-item ${index === this.currentMonth ? 'active' : ''}" 
           href="#" data-month="${index}">
          ${month}-${month}
        </a>
      </li>
    `).join('');
  }
  
  initDayRanges() {
    const dropdown = this.container.querySelector('.day-dropdown');
    const ranges = ['1-7', '1-15', '1-25', '1-31'];
    
    dropdown.innerHTML = ranges.map(range => `
      <li>
        <a class="dropdown-item ${range === this.currentDayRange ? 'active' : ''}" 
           href="#" data-range="${range}">
          ${range}
        </a>
      </li>
    `).join('') + `
      <li><hr class="dropdown-divider"></li>
      <li><a class="dropdown-item" href="#" data-range="custom">Custom Range...</a></li>
    `;
  }
  
  setupEventListeners() {
    // Year selection
    this.container.querySelectorAll('.year-dropdown .dropdown-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const year = parseInt(e.target.dataset.year);
        this.currentYear = year;
        this.container.querySelector('.selected-year').textContent = `${year}-${year}`;
        this.updateActiveState('.year-dropdown', year, 'year');
      });
    });
    
    // Month selection
    this.container.querySelectorAll('.month-dropdown .dropdown-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const monthIndex = parseInt(e.target.dataset.month);
        this.currentMonth = monthIndex;
        const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
        const month = months[monthIndex];
        this.container.querySelector('.selected-month').textContent = `${month}-${month}`;
        this.updateActiveState('.month-dropdown', monthIndex, 'month');
      });
    });
    
    // Day range selection
    this.container.querySelectorAll('.day-dropdown .dropdown-item').forEach(item => {
      item.addEventListener('click', (e) => {
        e.preventDefault();
        const range = e.target.dataset.range;
        if (range === 'custom') {
          alert('Custom range selector would open here');
          return;
        }
        this.currentDayRange = range;
        this.container.querySelector('.selected-day').textContent = range;
        this.updateActiveState('.day-dropdown', range, 'range');
      });
    });
  }
  
  updateActiveState(dropdownClass, value, type) {
    // Remove active class from all items
    this.container.querySelectorAll(`${dropdownClass} .dropdown-item`).forEach(item => {
      item.classList.remove('active');
    });
    
    // Add active class to selected item
    const selector = `${dropdownClass} .dropdown-item[data-${type}="${value}"]`;
    const activeItem = this.container.querySelector(selector);
    if (activeItem) activeItem.classList.add('active');
  }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new DateSelector('.date-selector-container');
});