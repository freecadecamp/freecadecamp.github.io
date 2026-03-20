// main.js – mobile menu, counters, active link, and loadHTML (Updated with Green + Orange Theme)

// ----- loadHTML (reusable) -----
function loadHTML(selector, url) {
    fetch(url)
    .then(res => {
        if (!res.ok) throw new Error('Failed to load ' + url);
        return res.text();
    })
    .then(data => {
        document.getElementById(selector).innerHTML = data;
        // after header loaded, re‑attach mobile menu listener and set active link
        if (selector === 'header') {
            initMobileMenu();
            highlightActiveLink();
            initDropdownMenus(); // initialize any dropdown menus
        }
        // re-initialize counters after content loads
        initCounters();
    })
    .catch(err => console.warn(err));
}

// ----- mobile menu toggle -----
function initMobileMenu() {
    const menuBtn = document.getElementById('menuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    if (menuBtn && mobileMenu) {
        // remove old listener to avoid duplicates
        menuBtn.replaceWith(menuBtn.cloneNode(true));
        const newBtn = document.getElementById('menuBtn');
        newBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            // animate menu open/close
            if (!mobileMenu.classList.contains('hidden')) {
                mobileMenu.style.animation = 'fadeInUp 0.3s ease-out';
            }
        });

        // close on link click
        const links = mobileMenu.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    }
}

// ----- dropdown menus (for future expandable menus) -----
function initDropdownMenus() {
    const dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('click', (e) => {
            e.preventDefault();
            const menu = dropdown.nextElementSibling;
            if (menu && menu.classList.contains('dropdown-menu')) {
                menu.classList.toggle('hidden');
            }
        });
    });
}

// ----- animated counters (enhanced with Green/Orange theme) -----
function initCounters() {
    const counters = document.querySelectorAll('.counter');
    if (counters.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counter = entry.target;
                const target = parseInt(counter.getAttribute('data-target'), 10);
                if (!counter.classList.contains('counted')) {
                    counter.classList.add('counted');
                    let current = 0;
                    const duration = 1500; // 1.5 seconds
                    const stepTime = 20; // milliseconds per step
                    const steps = duration / stepTime;
                    const increment = target / steps;

                    const updateCounter = () => {
                        current += increment;
                        if (current < target) {
                            counter.innerText = Math.ceil(current);
                            setTimeout(updateCounter, stepTime);
                        } else {
                            counter.innerText = target;
                            // add a subtle pulse effect when count completes
                            counter.classList.add('counter-complete');
                            setTimeout(() => {
                                counter.classList.remove('counter-complete');
                            }, 500);
                        }
                    };
                    updateCounter();
                }
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
}

// ----- highlight active link in nav (based on current page) - Updated with Orange Theme -----
function highlightActiveLink() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('nav a[href], #mobileMenu a[href]');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        // remove any existing active classes
        link.classList.remove('text-orange-500', 'font-semibold', 'bg-orange-50', 'text-emerald-600', 'bg-emerald-50');

        if (href === currentPage) {
            link.classList.add('text-orange-500', 'font-semibold');
            // optional background for desktop
            if (!link.closest('#mobileMenu')) {
                link.classList.add('bg-orange-50');
            }
        }
    });
}

// ----- smooth scroll for anchor links -----
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== "#" && href !== "#!") {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
}

// ----- scroll to top button -----
function initScrollToTop() {
    const scrollBtn = document.getElementById('scrollToTop');
    if (scrollBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                scrollBtn.classList.remove('hidden');
                scrollBtn.classList.add('flex');
            } else {
                scrollBtn.classList.add('hidden');
                scrollBtn.classList.remove('flex');
            }
        });

        scrollBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// ----- lazy load images (performance) -----
function initLazyLoad() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// ----- form validation helper -----
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('border-red-500');
            isValid = false;
        } else {
            input.classList.remove('border-red-500');
        }

        // email validation
        if (input.type === 'email' && input.value.trim()) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(input.value.trim())) {
                input.classList.add('border-red-500');
                isValid = false;
            }
        }

        // phone validation (10 digits)
        if (input.type === 'tel' && input.value.trim()) {
            const phoneRegex = /^[0-9]{10}$/;
            if (!phoneRegex.test(input.value.trim())) {
                input.classList.add('border-red-500');
                isValid = false;
            }
        }
    });

    return isValid;
}

// ----- display toast notification -----
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `fixed bottom-5 right-5 px-6 py-3 rounded-lg shadow-lg text-white z-50 animate-fade-in-up ${type === 'success' ? 'bg-green-600' : 'bg-orange-500'}`;
    toast.innerHTML = `
    <div class="flex items-center gap-2">
    <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
    <span>${message}</span>
    </div>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ----- init all components -----
function initAll() {
    initCounters();
    initSmoothScroll();
    initScrollToTop();
    initLazyLoad();
    highlightActiveLink();

    // initialize any forms with submit handling
    const contactForm = document.querySelector('form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (validateForm(contactForm.id)) {
                showToast('Message sent successfully! We will contact you soon.', 'success');
                contactForm.reset();
            } else {
                showToast('Please fill all required fields correctly.', 'error');
            }
        });
    }
}

// ----- run on load and after dynamic content -----
window.addEventListener('DOMContentLoaded', () => {
    initAll();
});

// observe body for dynamic header insertion
const observer = new MutationObserver(() => {
    initCounters();
    highlightActiveLink();
    initScrollToTop();
});
observer.observe(document.body, { childList: true, subtree: true });

// ----- export functions for use in other files (if needed) -----
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        loadHTML,
        initCounters,
        highlightActiveLink,
        validateForm,
        showToast
    };
}
