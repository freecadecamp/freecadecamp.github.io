/* ================================================================
   VARAM SUSTAINABLE SOLUTIONS — Corporate Enhancement JS
================================================================ */
(function() {
  'use strict';

  /* ── 1. Page Ripple Transition ── */
  function injectRipple() {
    const ripple = document.createElement('div');
    ripple.id = 'page-ripple';
    document.body.appendChild(ripple);

    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('mailto:') ||
          href.startsWith('tel:') || href.startsWith('http') ||
          link.hasAttribute('target')) return;
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const dest = href;
        ripple.classList.add('active');
        setTimeout(() => { window.location.href = dest; }, 520);
      });
    });
  }

  /* ── 2. Scroll Progress Bar ── */
  function injectScrollProgress() {
    const bar = document.createElement('div');
    bar.id = 'scroll-progress';
    document.body.appendChild(bar);

    function update() {
      const scrollTop = window.scrollY || document.documentElement.scrollTop;
      const docH = document.documentElement.scrollHeight - window.innerHeight;
      const pct = docH > 0 ? (scrollTop / docH) * 100 : 0;
      bar.style.width = pct + '%';
    }
    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  /* ── 3. Navbar Scroll Effect + Active Page ── */
  function enhanceNavbar() {
    const nav = document.querySelector('nav.fixed');
    if (!nav) return;

    // Scroll shadow
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 50);
    }, { passive: true });

    // Active page highlight
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    nav.querySelectorAll('a[href]').forEach(a => {
      if (a.getAttribute('href') === currentPage) {
        a.classList.add('nav-active');
      }
    });
    // Mobile menu active too
    const mobileMenu = document.getElementById('mobileMenu');
    if (mobileMenu) {
      mobileMenu.querySelectorAll('a[href]').forEach(a => {
        if (a.getAttribute('href') === currentPage) {
          a.style.background = 'linear-gradient(135deg, rgba(27,140,78,0.12), rgba(245,124,0,0.08))';
          a.style.color = '#1B8C4E';
        }
      });
    }
  }

  /* ── 4. Scroll Reveal ── */
  function setupScrollReveal() {
    // Auto-add reveal classes to section children
    document.querySelectorAll('section > div, section .grid > div, section .flex > div').forEach((el, i) => {
      if (!el.classList.contains('reveal') &&
          !el.classList.contains('reveal-left') &&
          !el.classList.contains('reveal-right') &&
          !el.closest('nav') &&
          !el.closest('#lang-fab') &&
          !el.closest('#back-to-top')) {
        el.classList.add('reveal');
        const delay = (i % 5);
        if (delay > 0) el.classList.add('reveal-d' + delay);
      }
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
      observer.observe(el);
    });
  }

  /* ── 5. Counter Animation ── */
  function setupCounters() {
    const counters = document.querySelectorAll('.counter[data-target]');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        const target = +el.dataset.target;
        const duration = 2400; // 2.4 seconds for smooth counting
        const step = target / (duration / 16);
        let current = 0;
        const timer = setInterval(() => {
          current = Math.min(current + step, target);
          el.textContent = Math.floor(current);
          if (current >= target) {
            el.textContent = target;
            clearInterval(timer);
          }
        }, 16);
        observer.unobserve(el);
      });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
  }

  /* ── 6. Back to Top ── */
  function injectBackToTop() {
    const btn = document.createElement('button');
    btn.id = 'back-to-top';
    btn.setAttribute('aria-label', 'Back to top');
    btn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    document.body.appendChild(btn);

    window.addEventListener('scroll', () => {
      btn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });

    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── 7. WhatsApp FAB ── */
  function injectWhatsApp() {
    const wa = document.createElement('a');
    wa.id = 'wa-fab';
    wa.href = 'https://wa.me/919841722118?text=Hello%20VARAM%20Sustainable%20Solutions!%20I%27m%20interested%20in%20your%20clean%20cooking%20solutions.';
    wa.target = '_blank';
    wa.rel = 'noopener noreferrer';
    wa.setAttribute('aria-label', 'Chat on WhatsApp');
    wa.innerHTML = '<i class="fab fa-whatsapp"></i>';
    document.body.appendChild(wa);
  }

  /* ── 8. Google Translate FAB ── */
  function injectTranslateFAB() {
    // Hidden GT container for Google Translate initialization
    const gtDiv = document.createElement('div');
    gtDiv.id = 'google_translate_element';
    gtDiv.style.display = 'none';
    document.body.appendChild(gtDiv);

    // Language data
    const languages = [
      { code: 'en',    label: '🇬🇧 English' },
      { code: 'ta',    label: '🇮🇳 தமிழ்' },
      { code: 'hi',    label: '🇮🇳 हिन्दी' },
      { code: 'te',    label: '🇮🇳 తెలుగు' },
      { code: 'kn',    label: '🇮🇳 ಕನ್ನಡ' },
      { code: 'ml',    label: '🇮🇳 മലയാളം' },
      { code: 'bn',    label: '🇮🇳 বাংলា' },
      { code: 'mr',    label: '🇮🇳 मराठी' },
      { code: 'gu',    label: '🇮🇳 ગુજરાતી' },
      { code: 'fr',    label: '🇫🇷 Français' },
      { code: 'de',    label: '🇩🇪 Deutsch' },
      { code: 'zh-CN', label: '🇨🇳 中文' },
      { code: 'ar',    label: '🇸🇦 العربية' },
      { code: 'es',    label: '🇪🇸 Español' },
    ];

    // FAB container
    const fab = document.createElement('div');
    fab.id = 'lang-fab';

    // Panel
    const panel = document.createElement('div');
    panel.id = 'lang-panel';
    panel.innerHTML = `<h4><i class="fas fa-globe" style="color:#1B8C4E;font-size:13px;"></i> Select Language</h4>`;

    const grid = document.createElement('div');
    grid.id = 'custom-lang-grid';

    let activeLangCode = localStorage.getItem('varamLang') || 'en';

    function setLanguageCookie(code) {
      // Set the Google Translate cookie
      const cookieVal = code === 'en' ? '/en/en' : '/en/' + code;
      document.cookie = 'googtrans=' + cookieVal + '; path=/';
      // Also try domain-specific
      document.cookie = 'googtrans=' + cookieVal + '; domain=' + window.location.hostname + '; path=/';
    }

    function doTranslate(code) {
      activeLangCode = code;
      localStorage.setItem('varamLang', code);

      // Update button states
      grid.querySelectorAll('button').forEach(b => {
        b.classList.toggle('active-lang', b.dataset.lang === code);
      });

      if (code === 'en') {
        // Restore English (original)
        setLanguageCookie('en');
        // Remove translation class from body
        document.documentElement.classList.remove('translated');
        // Reload page to clear translation
        setTimeout(() => {
          window.location.reload();
        }, 200);
        return;
      }

      // Set cookie for translation
      setLanguageCookie(code);

      // Try to trigger Google Translate via the widget
      function triggerTranslate(attempts) {
        // Look for the Google Translate select dropdown
        const select = document.querySelector('.goog-te-combo');
        if (select) {
          select.value = code;
          select.dispatchEvent(new Event('change', { bubbles: true }));
          return true;
        }

        // If not found, try finding and clicking the translate button/element
        const elements = document.querySelectorAll('[role="option"]');
        for (let el of elements) {
          if (el.textContent.includes(code) || el.getAttribute('data-language') === code) {
            el.click();
            return true;
          }
        }

        if (attempts < 50) {
          setTimeout(() => triggerTranslate(attempts + 1), 100);
        } else {
          // Fallback: reload page with cookie set
          window.location.reload();
        }
      }

      triggerTranslate(0);
    }

    languages.forEach(lang => {
      const btn = document.createElement('button');
      btn.dataset.lang = lang.code;
      btn.textContent = lang.label;
      if (lang.code === activeLangCode) btn.classList.add('active-lang');
      btn.addEventListener('click', () => {
        doTranslate(lang.code);
        panel.classList.remove('open');
        fabBtn.classList.remove('open');
      });
      grid.appendChild(btn);
    });

    panel.appendChild(grid);

    // FAB button
    const fabBtn = document.createElement('button');
    fabBtn.id = 'lang-fab-btn';
    fabBtn.setAttribute('aria-label', 'Change language');
    fabBtn.setAttribute('title', 'Change language');
    fabBtn.innerHTML = '<i class="fas fa-globe-asia"></i>';

    fabBtn.addEventListener('click', () => {
      const open = panel.classList.toggle('open');
      fabBtn.classList.toggle('open', open);
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!fab.contains(e.target)) {
        panel.classList.remove('open');
        fabBtn.classList.remove('open');
      }
    });

    fab.appendChild(panel);
    fab.appendChild(fabBtn);
    document.body.appendChild(fab);

    // Load Google Translate widget
    const script = document.createElement('script');
    script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
    script.async = true;
    script.onerror = () => {
      console.warn('Google Translate failed to load');
    };
    document.head.appendChild(script);

    // Initialize Google Translate
    window.googleTranslateElementInit = function() {
      try {
        new google.translate.TranslateElement({
          pageLanguage: 'en',
          includedLanguages: 'en,ta,hi,te,kn,ml,bn,mr,gu,pa,ur,fr,de,zh-CN,ar,ja,ko,es',
          layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
          autoDisplay: false
        }, 'google_translate_element');
      } catch(e) {
        console.warn('Google Translate init error:', e);
      }
    };

    // Apply saved language on page load after short delay
    if (activeLangCode && activeLangCode !== 'en') {
      setTimeout(() => {
        doTranslate(activeLangCode);
      }, 1500);
    }
  }

  /* ── 9. Smooth Section Entrance (beyond hero) ── */
  function enhanceSections() {
    document.querySelectorAll('section').forEach((sec, i) => {
      if (i === 0) return; // skip hero
      sec.style.opacity = '0';
      sec.style.transform = 'translateY(20px)';
      sec.style.transition = 'opacity 0.6s ease, transform 0.6s ease';

      const obs = new IntersectionObserver(([entry]) => {
        if (entry.isIntersecting) {
          sec.style.opacity = '1';
          sec.style.transform = 'translateY(0)';
          obs.unobserve(sec);
        }
      }, { threshold: 0.06 });
      obs.observe(sec);
    });
  }

  /* ── 10. Hover micro-interaction on nav desktop links ── */
  function navMicroInteraction() {
    document.querySelectorAll('nav .hidden.md\\:flex a').forEach(link => {
      link.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-1px)';
      });
      link.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
      });
    });
  }

  /* ── INIT ── */
  document.addEventListener('DOMContentLoaded', () => {
    injectRipple();
    injectScrollProgress();
    enhanceNavbar();
    setupScrollReveal();
    setupCounters();
    injectBackToTop();
    injectWhatsApp();
    injectTranslateFAB();
    enhanceSections();
    navMicroInteraction();
  });

})();
