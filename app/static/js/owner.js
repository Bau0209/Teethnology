document.addEventListener('DOMContentLoaded', function() {
  const btn = document.getElementById('userDropdownBtn');
  const menu = document.getElementById('userDropdownMenu');
  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
  });
  document.addEventListener('click', function() {
    menu.style.display = 'none';
  });
})


//audio equalizer overlay
var confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
confirmModal.show();

document.addEventListener('DOMContentLoaded', function() {
  const micBtn = document.querySelector('.voice-assistant button');
  const overlay = document.getElementById('audio-equalizer-overlay');

  micBtn.addEventListener('click', function(e) {
    e.preventDefault();
    overlay.style.display = 'flex';
  });

  // Hide overlay when clicking outside the equalizer
  overlay.addEventListener('click', function(e) {
    if (e.target === overlay) {
      overlay.style.display = 'none';
    }
  });
});


// Confirm modal overlay
document.addEventListener('DOMContentLoaded', function() {
  // Dropdown for username
  const btn = document.getElementById('userDropdownBtn');
  const menu = document.getElementById('userDropdownMenu');
  if (btn && menu) {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    });
    document.addEventListener('click', function() {
      menu.style.display = 'none';
    });
  }

  // Audio equalizer and modal logic
  const micBtn = document.querySelector('.voice-assistant button');
  const equalizer = document.getElementById('audio-equalizer-overlay');
  const modal = document.getElementById('confirm-modal-overlay');
  let modalTimeout;

  if (micBtn && equalizer && modal) {
    micBtn.addEventListener('click', function(e) {
      e.preventDefault();
      equalizer.style.display = 'flex';
      modal.style.display = 'none';
      clearTimeout(modalTimeout);
      modalTimeout = setTimeout(function() {
        equalizer.style.display = 'none';
        modal.style.display = 'flex';
      }, 5000); // 5 seconds
    });

    // Hide equalizer when clicking outside
    equalizer.addEventListener('click', function(e) {
      if (e.target === equalizer) {
        equalizer.style.display = 'none';
        clearTimeout(modalTimeout);
      }
    });

    // Hide modal on "No" or "Yes"
    const noBtn = document.querySelector('.modal-no');
    const yesBtn = document.querySelector('.modal-yes');
    if (noBtn) noBtn.onclick = function() { modal.style.display = 'none'; };
    if (yesBtn) yesBtn.onclick = function() { modal.style.display = 'none'; /* Add Yes action here */ };

    // Hide modal if clicking outside content
    modal.addEventListener('click', function(e) {
      if (e.target === modal) modal.style.display = 'none';
    });
  }
});


//o_branches_info.js
document.addEventListener('DOMContentLoaded', function() {
  const images = [
    '../../static/images/quezon clinic example.jpg',
    '../../static/images/quezon clinic example2.jpg',
    '../../static/images/quezon clinic example3.jpg'
  ];
  let current = 0;
  const mainImg = document.getElementById('mainBranchImg');
  const thumbs = document.querySelectorAll('.branch-info-thumb');

  function showImage(idx) {
    current = idx;
    mainImg.src = images[current];
    thumbs.forEach((thumb, i) => {
      thumb.classList.toggle('active', i === current);
    });
  }

  document.querySelector('.slider-arrow-left').onclick = function() {
    showImage((current - 1 + images.length) % images.length);
  };
  document.querySelector('.slider-arrow-right').onclick = function() {
    showImage((current + 1) % images.length);
  };
  thumbs.forEach((thumb, i) => {
    thumb.onclick = () => showImage(i);
  });
});

// Included code
document.querySelector('.voice-assistant button').addEventListener('click', function() {
    document.getElementById('audio-equalizer-overlay').style.display = 'flex';
    setTimeout(function() {
        document.getElementById('audio-equalizer-overlay').style.display = 'none';
    }, 3000);
});