/* ============================================
   Portfolio — main.js
   ============================================ */

// Mobile nav toggle
function setupMobileNav() {
    const toggle = document.getElementById('navToggle');
    const nav    = document.getElementById('siteNav');
    if (!toggle || !nav) return;

    toggle.addEventListener('click', () => nav.classList.toggle('open'));

    nav.querySelectorAll('a').forEach(link =>
        link.addEventListener('click', () => nav.classList.remove('open'))
    );
}

// Active nav link based on current page URL
function setActiveNavLink() {
    const links = document.querySelectorAll('.site-nav a');
    const path  = window.location.pathname;

    links.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (!href) return;

        // Root path — only match exactly
        if (href === '/' && path === '/') {
            link.classList.add('active');
        } else if (href !== '/' && path.startsWith(href)) {
            link.classList.add('active');
        }
    });
}

// Animate skill bars (triggered by IntersectionObserver)
function animateSkillBars(container) {
    container.querySelectorAll('.skill-bar-fill').forEach(bar => {
        const pct = bar.getAttribute('data-percent') || '0';
        bar.style.width = pct + '%';
    });
}

function setupSkillBarsObserver() {
    const section = document.querySelector('.skills-section');
    if (!section) return;

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateSkillBars(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.25 });

    observer.observe(section);
}

// Animate counters
function animateCounters() {
    document.querySelectorAll('.counter').forEach(counter => {
        const target   = parseInt(counter.getAttribute('data-target')) || 0;
        const duration = 1400;
        const step     = target / (duration / 16);
        let current    = 0;

        const tick = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(tick);
            }
            counter.textContent = Math.floor(current);
        }, 16);
    });
}

function setupCounterObserver() {
    const targets = document.querySelectorAll('.counter');
    if (!targets.length) return;

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.disconnect();
            }
        });
    }, { threshold: 0.4 });

    observer.observe(targets[0].closest('section') || targets[0]);
}

// Init on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
    setupMobileNav();
    setActiveNavLink();
    setupSkillBarsObserver();
    setupCounterObserver();
});
