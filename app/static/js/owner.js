document.addEventListener('DOMContentLoaded', function () {
  // Toggle user dropdown
  const btn = document.getElementById('userDropdownBtn');
  const menu = document.getElementById('userDropdownMenu');
  if (btn && menu) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    });
    document.addEventListener('click', function () {
      menu.style.display = 'none';
    });
  }

  // Sidebar navigation using fetch (SPA-like)
  document.querySelectorAll('.sidebar a').forEach(link => {
    link.addEventListener('click', function (e) {
      const url = this.href;

      // If it's an anchor link or external, allow default
      if (url.startsWith('#') || url.startsWith('http')) return;

      e.preventDefault(); // prevent full reload

      fetch(url)
        .then(res => res.text())
        .then(html => {
          const parser = new DOMParser();
          const doc = parser.parseFromString(html, 'text/html');
          const newContent = doc.querySelector('#main-content');

          if (newContent) {
            document.querySelector('#main-content').innerHTML = newContent.innerHTML;

            // Push to browser history
            window.history.pushState({}, '', url);

            // Re-initialize dynamic scripts if needed
            initDynamicFeatures();
          }
        })
        .catch(err => {
          console.error('Page load failed:', err);
          alert('Failed to load the page. Please try again.');
        });
    });
  });

  // Listen for browser back/forward buttons
  window.addEventListener('popstate', function () {
    fetch(window.location.href)
      .then(res => res.text())
      .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newContent = doc.querySelector('#main-content');
        if (newContent) {
          document.querySelector('#main-content').innerHTML = newContent.innerHTML;
          initDynamicFeatures();
        }
      });
  });

  // Audio equalizer + modal logic
  initDynamicFeatures(); // Call once initially
});

function initDynamicFeatures() {
  const micBtn = document.querySelector('.voice-assistant button');
  const equalizer = document.getElementById('audio-equalizer-overlay');
  const modal = document.getElementById('confirm-modal-overlay');
  let modalTimeout;

  if (micBtn && equalizer) {
    micBtn.addEventListener('click', function (e) {
      e.preventDefault();
      equalizer.style.display = 'flex';
      if (modal) modal.style.display = 'none';
      clearTimeout(modalTimeout);
      modalTimeout = setTimeout(() => {
        equalizer.style.display = 'none';
        if (modal) modal.style.display = 'flex';
      }, 5000);
    });

    equalizer.addEventListener('click', function (e) {
      if (e.target === equalizer) {
        equalizer.style.display = 'none';
        clearTimeout(modalTimeout);
      }
    });
  }

  if (modal) {
    const noBtn = document.querySelector('.modal-no');
    const yesBtn = document.querySelector('.modal-yes');
    if (noBtn) noBtn.onclick = () => modal.style.display = 'none';
    if (yesBtn) yesBtn.onclick = () => modal.style.display = 'none';
    modal.addEventListener('click', e => {
      if (e.target === modal) modal.style.display = 'none';
    });
  }

  // --- Image Slider Functionality ---
  const mainImg = document.getElementById('mainBranchImg');
  const thumbnails = document.querySelectorAll('.branch-info-thumb');
  const imageList = [];

  thumbnails.forEach((thumb, index) => {
    imageList.push(thumb.getAttribute('data-src'));

    // Add click to set main image
    thumb.onclick = () => {
      mainImg.src = thumb.getAttribute('data-src');
      mainImg.setAttribute('data-index', index);
      updateActiveThumb(index);
    };
  });

  // Update active thumbnail
  function updateActiveThumb(index) {
    thumbnails.forEach(thumb => thumb.classList.remove('active'));
    const active = document.querySelector(`.branch-info-thumb[data-index="${index}"]`);
    if (active) active.classList.add('active');
  }

  // Arrow navigation
  document.querySelectorAll('.slider-arrow').forEach(button => {
    button.onclick = (e) => {
      const dir = button.classList.contains('slider-arrow-right') ? 1 : -1;
      let currentIndex = parseInt(mainImg.getAttribute('data-index'));
      if (isNaN(currentIndex)) currentIndex = 0;

      const nextIndex = (currentIndex + dir + imageList.length) % imageList.length;
      mainImg.src = imageList[nextIndex];
      mainImg.setAttribute('data-index', nextIndex);
      updateActiveThumb(nextIndex);
    };
  });

}


