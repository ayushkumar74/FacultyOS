/**
 * FACULTYOS — CLIENT INTERACTION ENGINE (PHASE 7)
 * High-Performance Vanilla JavaScript
 * Zero External Framework Dependencies & Accessibility Compliant
 */

document.addEventListener('DOMContentLoaded', () => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // -------------------------------------------------------------
    // 1. Mobile Responsive Sidebar Toggle & Backdrop
    // -------------------------------------------------------------
    const sidebarToggle = document.getElementById('sidebarToggle');
    const appSidebar = document.getElementById('appSidebar');

    if (sidebarToggle && appSidebar) {
        let backdrop = document.querySelector('.sidebar-backdrop');
        if (!backdrop) {
            backdrop = document.createElement('div');
            backdrop.className = 'sidebar-backdrop';
            document.body.appendChild(backdrop);
        }

        function toggleSidebar(forceState) {
            const shouldOpen = typeof forceState === 'boolean' ? forceState : !appSidebar.classList.contains('show');
            if (shouldOpen) {
                appSidebar.classList.add('show');
                backdrop.classList.add('active');
                document.body.style.overflow = 'hidden';
            } else {
                appSidebar.classList.remove('show');
                backdrop.classList.remove('active');
                document.body.style.overflow = '';
            }
        }

        sidebarToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            toggleSidebar();
        });

        backdrop.addEventListener('click', () => toggleSidebar(false));

        // Close on ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && appSidebar.classList.contains('show')) {
                toggleSidebar(false);
            }
        });
    }

    // -------------------------------------------------------------
    // 2. Numerical Metric Count-Up Animation
    // -------------------------------------------------------------
    const counterElements = document.querySelectorAll('[data-counter-target]');
    if (counterElements.length > 0) {
        counterElements.forEach(el => {
            const target = parseFloat(el.getAttribute('data-counter-target'));
            if (isNaN(target)) return;
            const isFloat = el.getAttribute('data-counter-float') === 'true';

            if (prefersReducedMotion) {
                el.textContent = isFloat ? target.toFixed(1) : target;
                return;
            }

            const duration = 750; // ms
            const startTime = performance.now();

            function updateCounter(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                // Ease out cubic
                const ease = 1 - Math.pow(1 - progress, 3);
                const currentVal = ease * target;

                el.textContent = isFloat ? currentVal.toFixed(1) : Math.round(currentVal);

                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    el.textContent = isFloat ? target.toFixed(1) : target;
                }
            }
            requestAnimationFrame(updateCounter);
        });
    }

    // -------------------------------------------------------------
    // 3. Scroll-Triggered Section Reveals (IntersectionObserver)
    // -------------------------------------------------------------
    const revealItems = document.querySelectorAll('.reveal-on-scroll');
    if (revealItems.length > 0) {
        if ('IntersectionObserver' in window && !prefersReducedMotion) {
            const observer = new IntersectionObserver((entries, obs) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-revealed');
                        obs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.12 });

            revealItems.forEach(item => observer.observe(item));
        } else {
            revealItems.forEach(item => item.classList.add('is-revealed'));
        }
    }

    // -------------------------------------------------------------
    // 4. Live Table Search & Filter
    // -------------------------------------------------------------
    const tableSearchInputs = document.querySelectorAll('[data-table-filter]');
    tableSearchInputs.forEach(input => {
        const targetTableId = input.getAttribute('data-table-filter');
        const targetTable = document.getElementById(targetTableId);
        if (!targetTable) return;

        input.addEventListener('input', () => {
            const query = input.value.toLowerCase().trim();
            const rows = targetTable.querySelectorAll('tbody tr:not(.empty-state-row)');
            let visibleCount = 0;

            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                const matches = text.includes(query);
                row.style.display = matches ? '' : 'none';
                if (matches) visibleCount++;
            });

            // Toggle custom empty search state row if present
            const emptyNotice = targetTable.querySelector('.empty-search-notice');
            if (emptyNotice) {
                emptyNotice.style.display = (visibleCount === 0 && rows.length > 0) ? '' : 'none';
            }
        });
    });

    // -------------------------------------------------------------
    // 5. Auto-Dismiss Flash Alerts
    // -------------------------------------------------------------
    const autoAlerts = document.querySelectorAll('.saas-alert-dismissible');
    autoAlerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.35s ease, transform 0.35s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-6px)';
            setTimeout(() => alert.remove(), 350);
        }, 5500);
    });

    // -------------------------------------------------------------
    // 6. Interactive Landing Page PBAS Simulator
    // -------------------------------------------------------------
    const simForm = document.getElementById('pbasSimulatorForm');
    if (simForm) {
        const tInput = document.getElementById('simTeaching');
        const rInput = document.getElementById('simResearch');
        const wInput = document.getElementById('simWorkshops');
        const pInput = document.getElementById('simProjects');

        const scoreDisplay = document.getElementById('simTotalScore');
        const gradeBadge = document.getElementById('simGradeBadge');
        const casPill = document.getElementById('simCasPill');

        function updateSimulator() {
            const t = Math.min(40, Math.max(0, parseFloat(tInput?.value || 0)));
            const r = Math.min(30, Math.max(0, parseFloat(rInput?.value || 0)));
            const w = Math.min(15, Math.max(0, parseFloat(wInput?.value || 0)));
            const p = Math.min(15, Math.max(0, parseFloat(pInput?.value || 0)));

            const total = (t + r + w + p).toFixed(1);
            if (scoreDisplay) scoreDisplay.textContent = total;

            // Update Progress Bar
            const progBar = document.getElementById('simProgressBar');
            if (progBar) progBar.style.width = `${Math.min(100, total)}%`;

            // Performance Grade
            if (gradeBadge) {
                if (total >= 80) {
                    gradeBadge.textContent = 'Grade A+ Outstanding';
                    gradeBadge.className = 'saas-badge saas-badge-green';
                } else if (total >= 70) {
                    gradeBadge.textContent = 'Grade A Very Good';
                    gradeBadge.className = 'saas-badge saas-badge-blue';
                } else if (total >= 55) {
                    gradeBadge.textContent = 'Grade B Good';
                    gradeBadge.className = 'saas-badge saas-badge-amber';
                } else {
                    gradeBadge.textContent = 'Grade C Satisfactory';
                    gradeBadge.className = 'saas-badge saas-badge-neutral';
                }
            }

            // CAS Promotion Eligibility
            if (casPill) {
                if (total >= 75) {
                    casPill.innerHTML = '<i class="bi bi-award-fill me-1"></i> Meets Criteria for CAS Promotion Screening';
                    casPill.className = 'saas-badge saas-badge-green';
                } else {
                    casPill.innerHTML = '<i class="bi bi-clock-history me-1"></i> Progression In Progress (Need 75.0+ pts)';
                    casPill.className = 'saas-badge saas-badge-amber';
                }
            }
        }

        [tInput, rInput, wInput, pInput].forEach(inp => {
            if (inp) {
                inp.addEventListener('input', updateSimulator);
            }
        });

        // Initialize simulator values on load
        updateSimulator();
    }
});

// -----------------------------------------------------------------
// 7. Global Evaluator Account Fill Function
// -----------------------------------------------------------------
window.fillAccount = function(username, password, roleLabel) {
    const uInput = document.getElementById('id_username');
    const pInput = document.getElementById('id_password');
    const feedback = document.getElementById('fillFeedback');
    const feedbackMsg = document.getElementById('fillFeedbackMsg');

    if (uInput && pInput) {
        uInput.value = username;
        pInput.value = password;

        [uInput, pInput].forEach(el => {
            el.classList.remove('cred-flash-highlight');
            void el.offsetWidth; // Reflow
            el.classList.add('cred-flash-highlight');
        });

        if (feedback && feedbackMsg) {
            feedbackMsg.innerHTML = `<strong>${roleLabel}</strong> credentials loaded. Click <strong>Sign In to Workspace</strong> to proceed.`;
            feedback.classList.remove('d-none');
            feedback.classList.add('d-flex');
        }

        pInput.focus();
    }
};
