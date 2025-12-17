/**
 * Main JavaScript - Library Management System
 * Apple-inspired interactions and animations
 */

// ===== MOBILE NAVIGATION TOGGLE =====
document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');
  
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function() {
      navMenu.classList.toggle('active');
      
      // Animate hamburger icon
      const icon = navToggle.querySelector('.navbar-toggle-icon');
      icon.classList.toggle('active');
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
      const isClickInsideNav = navMenu.contains(event.target);
      const isClickOnToggle = navToggle.contains(event.target);
      
      if (!isClickInsideNav && !isClickOnToggle && navMenu.classList.contains('active')) {
        navMenu.classList.remove('active');
      }
    });
  }
});

// ===== NAVBAR SCROLL EFFECT =====
let lastScroll = 0;
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function() {
  const currentScroll = window.pageYOffset;
  
  if (currentScroll > 100) {
    navbar.classList.add('navbar-scroll');
  } else {
    navbar.classList.remove('navbar-scroll');
  }
  
  lastScroll = currentScroll;
});

// ===== ALERT AUTO-DISMISS =====
document.addEventListener('DOMContentLoaded', function() {
  const alerts = document.querySelectorAll('.alert-dismissible');
  
  alerts.forEach(function(alert) {
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
      fadeOut(alert);
    }, 5000);
  });
});

// ===== SMOOTH SCROLL FOR ANCHOR LINKS =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// ===== FORM VALIDATION ENHANCEMENTS =====
document.addEventListener('DOMContentLoaded', function() {
  const forms = document.querySelectorAll('form');
  
  forms.forEach(function(form) {
    const inputs = form.querySelectorAll('.form-input, .form-select, .form-textarea');
    
    inputs.forEach(function(input) {
      // Add focus/blur animations
      input.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
      });
      
      input.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
        
        // Validate on blur
        if (input.hasAttribute('required') && !input.value.trim()) {
          input.classList.add('error');
        } else {
          input.classList.remove('error');
        }
      });
      
      // Real-time validation
      input.addEventListener('input', function() {
        if (input.classList.contains('error') && input.value.trim()) {
          input.classList.remove('error');
          input.classList.add('success');
        }
      });
    });
  });
});

// ===== CARD HOVER EFFECTS =====
document.addEventListener('DOMContentLoaded', function() {
  const cards = document.querySelectorAll('.card-hover, .bento-hover-lift');
  
  cards.forEach(function(card) {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-8px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });
});

// ===== TABLE ROW CLICK (for clickable tables) =====
document.addEventListener('DOMContentLoaded', function() {
  const clickableRows = document.querySelectorAll('tr[data-href]');
  
  clickableRows.forEach(function(row) {
    row.addEventListener('click', function() {
      window.location.href = this.dataset.href;
    });
    
    // Add pointer cursor
    row.style.cursor = 'pointer';
  });
});

// ===== LOADING SPINNER FOR BUTTONS =====
function showButtonLoading(button) {
  button.classList.add('btn-loading');
  button.disabled = true;
}

function hideButtonLoading(button) {
  button.classList.remove('btn-loading');
  button.disabled = false;
}

// ===== MODAL FUNCTIONS =====
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = 'none';
    document.body.style.overflow = '';
  }
}

// Close modal when clicking backdrop
document.addEventListener('click', function(e) {
  if (e.target.classList.contains('modal-backdrop')) {
    closeModal(e.target.id);
  }
});

// ===== SEARCH ENHANCEMENT =====
document.addEventListener('DOMContentLoaded', function() {
  const searchInputs = document.querySelectorAll('.form-search input');
  
  searchInputs.forEach(function(input) {
    // Add search icon animation
    input.addEventListener('focus', function() {
      this.parentElement.classList.add('searching');
    });
    
    input.addEventListener('blur', function() {
      if (!this.value) {
        this.parentElement.classList.remove('searching');
      }
    });
  });
});

// ===== DROPDOWN ENHANCEMENT (for custom dropdowns) =====
document.addEventListener('DOMContentLoaded', function() {
  const dropdowns = document.querySelectorAll('.dropdown');
  
  dropdowns.forEach(function(dropdown) {
    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.dropdown-menu');
    
    if (toggle && menu) {
      toggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Close other dropdowns
        document.querySelectorAll('.dropdown-menu.show').forEach(function(otherMenu) {
          if (otherMenu !== menu) {
            otherMenu.classList.remove('show');
          }
        });
        
        menu.classList.toggle('show');
      });
    }
  });
  
  // Close dropdowns when clicking outside
  document.addEventListener('click', function() {
    document.querySelectorAll('.dropdown-menu.show').forEach(function(menu) {
      menu.classList.remove('show');
    });
  });
});

// ===== UTILITY FUNCTIONS =====

// Fade out animation
function fadeOut(element, duration = 300) {
  element.style.transition = `opacity ${duration}ms`;
  element.style.opacity = '0';
  
  setTimeout(function() {
    element.style.display = 'none';
    element.remove();
  }, duration);
}

// Fade in animation
function fadeIn(element, duration = 300) {
  element.style.opacity = '0';
  element.style.display = 'block';
  element.style.transition = `opacity ${duration}ms`;
  
  setTimeout(function() {
    element.style.opacity = '1';
  }, 10);
}

// Debounce function for search/filter inputs
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Format number with thousands separator
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// Format currency (VND)
function formatCurrency(amount) {
  return formatNumber(amount) + 'đ';
}

// Copy to clipboard
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(function() {
    showToast('Đã sao chép vào clipboard!', 'success');
  });
}

// Show toast notification
function showToast(message, type = 'info') {
  const toast = document.createElement('div');
  toast.className = `alert alert-${type} alert-dismissible`;
  toast.innerHTML = `
    ${message}
    <button class="alert-close" onclick="this.parentElement.remove()">×</button>
  `;
  toast.style.position = 'fixed';
  toast.style.top = '80px';
  toast.style.right = '20px';
  toast.style.zIndex = '9999';
  toast.style.minWidth = '300px';
  
  document.body.appendChild(toast);
  
  // Auto remove after 3 seconds
  setTimeout(function() {
    fadeOut(toast);
  }, 3000);
}

// ===== BENTO GRID ANIMATIONS =====
document.addEventListener('DOMContentLoaded', function() {
  const bentoItems = document.querySelectorAll('.bento-item');
  
  // Intersection Observer for scroll animations
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, {
    threshold: 0.1
  });
  
  bentoItems.forEach(function(item) {
    observer.observe(item);
  });
});

// ===== TABLE SORTING (optional enhancement) =====
document.addEventListener('DOMContentLoaded', function() {
  const sortableTables = document.querySelectorAll('.table-sortable');
  
  sortableTables.forEach(function(table) {
    const headers = table.querySelectorAll('th[data-sort]');
    
    headers.forEach(function(header) {
      header.style.cursor = 'pointer';
      header.addEventListener('click', function() {
        sortTable(table, this.dataset.sort);
      });
    });
  });
});

function sortTable(table, column) {
  // Table sorting implementation
  const tbody = table.querySelector('tbody');
  const rows = Array.from(tbody.querySelectorAll('tr'));
  
  // Sort logic here...
  // (Implementation depends on data structure)
}

// ===== PRINT FUNCTIONALITY =====
function printPage() {
  window.print();
}

// ===== EXPORT FUNCTIONALITY =====
function exportToCSV(tableId) {
  const table = document.getElementById(tableId);
  if (!table) return;
  
  let csv = [];
  const rows = table.querySelectorAll('tr');
  
  rows.forEach(function(row) {
    const cols = row.querySelectorAll('td, th');
    const rowData = Array.from(cols).map(col => col.textContent.trim());
    csv.push(rowData.join(','));
  });
  
  const csvContent = csv.join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = window.URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = 'export.csv';
  a.click();
  
  window.URL.revokeObjectURL(url);
}

// ===== INIT =====
console.log('Library Management System - Apple Design v1.0');
console.log('Design: Blue Ocean + Pink Pastel + Purple Lavender');
