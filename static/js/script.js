document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initStatsCounter();
  initTeacherModals();
  initGalleryFilterAndLightbox();
  initRegistrationWizard();
  initBackToTop();
  initCaptcha();
  initMobileDropdown();
});

/* ==========================================================================
   STICKY NAVBAR
   ========================================================================== */
function initNavbar() {
  const header = document.getElementById('main-header');
  if (!header) return;

  // Only enable scroll-based class on transparent (homepage) header
  if (header.classList.contains('header-transparent')) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 60) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }, { passive: true });
  }
}

/* ==========================================================================
   MOBILE CAMPUS DROPDOWN TOGGLE
   ========================================================================== */
function initMobileDropdown() {
  const isMobile = () => window.innerWidth <= 768;

  const dropdownTrigger = document.querySelector('.dropdown-trigger');
  const dropMenu = document.querySelector('.dropdown .drop-item');

  if (!dropdownTrigger || !dropMenu) return;

  dropdownTrigger.addEventListener('click', (e) => {
    if (!isMobile()) return; // on desktop, CSS hover handles it
    e.preventDefault();
    const isOpen = dropMenu.style.display === 'flex' || dropMenu.style.display === 'block';
    dropMenu.style.display = isOpen ? 'none' : 'block';
    const icon = dropdownTrigger.querySelector('.dropdown-icon');
    if (icon) icon.style.transform = isOpen ? '' : 'rotate(180deg)';
  });

  // Close mobile menu when a dropdown link is clicked
  dropMenu.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      if (!isMobile()) return;
      const menuToggle = document.getElementById('menu-toggle');
      if (menuToggle) menuToggle.checked = false;
      dropMenu.style.display = 'none';
    });
  });

  // Close mobile menu when a regular nav link is clicked
  document.querySelectorAll('.nav-link:not(.dropdown-trigger)').forEach(link => {
    link.addEventListener('click', () => {
      if (!isMobile()) return;
      const menuToggle = document.getElementById('menu-toggle');
      if (menuToggle) menuToggle.checked = false;
    });
  });
}

/* ==========================================================================
   STATISTICS COUNTER (INTERSECTION OBSERVER)
   ========================================================================== */
function initStatsCounter() {
  const statNumbers = document.querySelectorAll('.stat-number');
  if (statNumbers.length === 0) return;

  const animateCounter = (el) => {
    const target = parseInt(el.getAttribute('data-target'), 10);
    if (isNaN(target)) return;
    
    let count = 0;
    const speed = target / 50; // anim speed
    
    const updateCount = () => {
      count += speed;
      if (count < target) {
        el.innerText = Math.floor(count) + (el.innerText.includes('%') ? '%' : '+');
        setTimeout(updateCount, 20);
      } else {
        el.innerText = target + (el.innerText.includes('%') ? '%' : '+');
      }
    };
    updateCount();
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  statNumbers.forEach(num => {
    // Save target number
    const currentText = num.innerText.replace('+', '').replace('%', '');
    const val = parseInt(currentText, 10);
    num.setAttribute('data-target', val);
    num.innerText = '0' + (num.innerText.includes('%') ? '%' : '+');
    observer.observe(num);
  });
}

/* ==========================================================================
   TEACHER MODALS
   ========================================================================== */
function initTeacherModals() {
  const viewProfileButtons = document.querySelectorAll('.view-profile-btn');
  
  viewProfileButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const card = e.target.closest('.teacher-card');
      const name = card.querySelector('h3').innerText;
      const title = card.querySelector('.teacher-title').innerText;
      const sub = card.querySelector('.teacher-subject').innerText;
      const imageSrc = card.querySelector('.teacher-img').src;
      
      const qual = card.getAttribute('data-qualification') || 'Not Specified';
      const exp = card.getAttribute('data-experience') || 'Not Specified';
      const bio = card.getAttribute('data-bio') || 'No biography available.';
      
      // Create Modal Dynamic layout
      const modalHtml = `
        <div class="modal active" id="teacher-profile-modal">
          <div class="modal-content">
            <span class="modal-close" onclick="closeModal()">&times;</span>
            <div class="modal-body">
              <div class="teacher-modal-layout">
                <img src="${imageSrc}" class="teacher-modal-img" alt="${name}">
                <div>
                  <h3 style="margin-bottom: 0.25rem;">${name}</h3>
                  <p class="teacher-title" style="margin-bottom: 0.5rem;">${title}</p>
                  <p class="teacher-subject" style="margin-bottom: 1rem;">${sub}</p>
                  <p><strong>Qualification:</strong> ${qual}</p>
                  <p><strong>Experience:</strong> ${exp}</p>
                  <p style="margin-top: 1rem;">${bio}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;
      
      document.body.insertAdjacentHTML('beforeend', modalHtml);
      
      // Keyboard Accessibility (Esc key to close)
      document.addEventListener('keydown', handleEscClose);
      
      // Close modal on click outside
      const modal = document.getElementById('teacher-profile-modal');
      modal.addEventListener('click', (event) => {
        if (event.target === modal) {
          closeModal();
        }
      });
    });
  });
}

window.closeModal = function() {
  const modal = document.getElementById('teacher-profile-modal') || document.querySelector('.modal');
  if (modal) {
    modal.remove();
    document.removeEventListener('keydown', handleEscClose);
  }
};

function handleEscClose(e) {
  if (e.key === 'Escape') {
    closeModal();
  }
}

/* ==========================================================================
   GALLERY FILTER & LIGHTBOX
   ========================================================================== */
function initGalleryFilterAndLightbox() {
  const filterButtons = document.querySelectorAll('.filter-btn');
  const galleryItems = document.querySelectorAll('.gallery-item');
  
  if (filterButtons.length > 0) {
    filterButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        // Active states
        filterButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        const category = btn.getAttribute('data-filter');
        
        galleryItems.forEach(item => {
          const itemCat = item.getAttribute('data-category');
          if (category === 'All' || itemCat === category) {
            item.classList.remove('hide');
          } else {
            item.classList.add('hide');
          }
        });
      });
    });
  }

  // Lightbox
  const lightbox = document.getElementById('gallery-lightbox');
  if (!lightbox) return;
  
  const lightboxImg = lightbox.querySelector('.lightbox-img');
  let currentIndex = 0;
  let visibleItems = [];

  const updateLightboxImage = () => {
    const targetItem = visibleItems[currentIndex];
    if (targetItem) {
      const img = targetItem.querySelector('img');
      lightboxImg.src = img.src;
      lightboxImg.alt = img.alt;
    }
  };

  galleryItems.forEach((item) => {
    item.addEventListener('click', () => {
      // Find currently visible items
      visibleItems = Array.from(galleryItems).filter(i => !i.classList.contains('hide'));
      currentIndex = visibleItems.indexOf(item);
      
      lightbox.style.display = 'flex';
      updateLightboxImage();
      
      // Accessibility Focus Lock / Key Navigation
      document.addEventListener('keydown', handleLightboxKeys);
    });
  });

  window.closeLightbox = function() {
    lightbox.style.display = 'none';
    document.removeEventListener('keydown', handleLightboxKeys);
  };

  window.changeLightboxImage = function(direction) {
    if (visibleItems.length === 0) return;
    currentIndex += direction;
    
    if (currentIndex < 0) {
      currentIndex = visibleItems.length - 1;
    } else if (currentIndex >= visibleItems.length) {
      currentIndex = 0;
    }
    updateLightboxImage();
  };

  function handleLightboxKeys(e) {
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowRight') changeLightboxImage(1);
    if (e.key === 'ArrowLeft') changeLightboxImage(-1);
  }

  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) {
      closeLightbox();
    }
  });
}

/* ==========================================================================
   REGISTRATION ADMISSION WIZARD (MULTI-STEP)
   ========================================================================== */
function initRegistrationWizard() {
  const wizard = document.getElementById('registration-wizard');
  if (!wizard) return;

  const steps = wizard.querySelectorAll('.wizard-step');
  const panels = wizard.querySelectorAll('.wizard-panel-step');
  const nextBtn = wizard.querySelector('.btn-next');
  const prevBtn = wizard.querySelector('.btn-prev');
  const submitBtn = wizard.querySelector('.btn-submit');
  
  let currentStepIndex = 0;

  const showStep = (index) => {
    panels.forEach((p, idx) => {
      p.classList.toggle('active', idx === index);
    });

    steps.forEach((s, idx) => {
      s.classList.toggle('active', idx === index);
      s.classList.toggle('completed', idx < index);
    });

    // Update buttons
    prevBtn.style.display = index === 0 ? 'none' : 'block';
    if (index === panels.length - 1) {
      nextBtn.style.display = 'none';
      submitBtn.style.display = 'block';
      buildReviewContent();
    } else {
      nextBtn.style.display = 'block';
      submitBtn.style.display = 'none';
    }
  };

  const validateStep = (index) => {
    const currentPanel = panels[index];
    const requiredInputs = currentPanel.querySelectorAll('[required]');
    let isValid = true;
    
    requiredInputs.forEach(input => {
      if (!input.value.trim()) {
        isValid = false;
        input.classList.add('error');
        input.style.borderColor = 'var(--danger-color)';
      } else {
        input.classList.remove('error');
        input.style.borderColor = '';
      }
    });

    // Specific field validations
    if (index === 0) { // Student Info
      const dob = currentPanel.querySelector('input[type="date"]');
      if (dob && !dob.value) isValid = false;
    }
    if (index === 2) { // Contact Info
      const mob = currentPanel.querySelector('input[name="mob"]');
      if (mob && (mob.value.length !== 10 || isNaN(mob.value))) {
        isValid = false;
        mob.style.borderColor = 'var(--danger-color)';
      }
    }
    
    return isValid;
  };

  const buildReviewContent = () => {
    const reviewContent = document.getElementById('review-content');
    if (!reviewContent) return;

    let html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; text-align: left;">';
    
    const fields = [
      { label: 'Student Name', name: 'fname' },
      { label: "Mother's Name", name: 'mname' },
      { label: 'Date of Birth', name: 'dob' },
      { label: 'Gender', name: 'gender' },
      { label: 'Religion', name: 'religion' },
      { label: 'Category', name: 'category' },
      { label: 'Place of Birth', name: 'pob' },
      { label: 'Email', name: 'email' },
      { label: 'Mobile No.', name: 'mob' },
      { label: 'Parent Aadhar', name: 'p_adhar' },
      { label: 'Student Aadhar', name: 'c_adhar' },
      { label: 'Street', name: 'street' },
      { label: 'Landmark', name: 'landmark' },
      { label: 'State', name: 'state' },
      { label: 'Pincode', name: 'pincode' }
    ];

    fields.forEach(f => {
      const input = wizard.querySelector(`[name="${f.name}"]`);
      let value = input ? input.value : '';
      if (input && input.tagName === 'SELECT') {
        value = input.options[input.selectedIndex].text;
      }
      html += `<div><strong>${f.label}:</strong> <span style="color: var(--secondary-text);">${value || 'N/A'}</span></div>`;
    });

    html += '</div>';
    reviewContent.innerHTML = html;
  };

  nextBtn.addEventListener('click', () => {
    if (validateStep(currentStepIndex)) {
      currentStepIndex++;
      showStep(currentStepIndex);
    } else {
      showToast("Please fill all required fields correctly before moving next.", "danger");
    }
  });

  prevBtn.addEventListener('click', () => {
    currentStepIndex--;
    showStep(currentStepIndex);
  });

  showStep(currentStepIndex);
}

/* ==========================================================================
   BACK TO TOP BUTTON
   ========================================================================== */
function initBackToTop() {
  const backToTop = document.querySelector('.back-to-top');
  if (!backToTop) return;
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      backToTop.classList.add('visible');
    } else {
      backToTop.classList.remove('visible');
    }
  });
  
  backToTop.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* ==========================================================================
   CAPTCHA SYSTEM
   ========================================================================== */
function initCaptcha() {
  const refreshBtn = document.getElementById('captcha-refresh');
  const captchaInput = document.getElementById('captcha-input');
  
  if (refreshBtn) {
    refreshBtn.addEventListener('click', (e) => {
      e.preventDefault();
      generateCaptcha();
    });
  }
  
  if (captchaInput) {
    captchaInput.addEventListener('input', validateCaptcha);
  }
  
  generateCaptcha();
}

window.generateCaptcha = function() {
  const captchaDisplay = document.getElementById('captcha-display');
  const captchaInput = document.getElementById('captcha-input');
  const captchaStatus = document.getElementById('captcha-status');
  const submitBtn = document.querySelector('button[type="submit"]');
  
  if (!captchaDisplay) return;
  
  if (captchaInput) captchaInput.value = '';
  if (captchaStatus) {
    captchaStatus.innerHTML = '';
    captchaStatus.className = '';
  }
  if (submitBtn) submitBtn.disabled = true;
  
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789';
  let captchaCode = '';
  for (let i = 0; i < 6; i++) {
    captchaCode += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  
  captchaDisplay.innerText = captchaCode;
  captchaDisplay.setAttribute('data-code', captchaCode);
};

window.validateCaptcha = function() {
  const captchaDisplay = document.getElementById('captcha-display');
  const captchaInput = document.getElementById('captcha-input');
  const captchaStatus = document.getElementById('captcha-status');
  const submitBtn = document.querySelector('button[type="submit"]');
  
  if (!captchaDisplay || !captchaInput) return;
  
  const expected = captchaDisplay.getAttribute('data-code');
  const entered = captchaInput.value.trim();
  
  if (entered.toLowerCase() === expected.toLowerCase()) {
    if (captchaStatus) {
      captchaStatus.innerHTML = '<i class="fas fa-check-circle" style="color:var(--success-color);"></i> Match';
      captchaStatus.style.color = 'var(--success-color)';
    }
    if (submitBtn) submitBtn.disabled = false;
  } else {
    if (captchaStatus) {
      if (entered.length > 0) {
        captchaStatus.innerHTML = '<i class="fas fa-times-circle" style="color:var(--danger-color);"></i> Mismatch';
        captchaStatus.style.color = 'var(--danger-color)';
      } else {
        captchaStatus.innerHTML = '';
      }
    }
    if (submitBtn) submitBtn.disabled = true;
  }
};

/* ==========================================================================
   TOASTS (HELPER)
   ========================================================================== */
window.showToast = function(msg, type = "success") {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }
  
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const icon = type === "success" ? "fa-check-circle" : "fa-exclamation-circle";
  
  toast.innerHTML = `
    <i class="fas ${icon}" style="color: var(--${type === 'success' ? 'success' : 'danger'}-color); font-size: 1.25rem;"></i>
    <span>${msg}</span>
  `;
  
  container.appendChild(toast);
  
  setTimeout(() => {
    toast.remove();
  }, 4000);
};