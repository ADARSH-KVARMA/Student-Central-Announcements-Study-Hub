document.addEventListener('DOMContentLoaded', function() {
    const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
    const mainNav = document.querySelector('nav.main-nav');

    if (mobileNavToggle && mainNav) {
        mobileNavToggle.addEventListener('click', function() {
            mainNav.classList.toggle('open');
            mobileNavToggle.classList.toggle('open');
            const isExpanded = mainNav.classList.contains('open');
            mobileNavToggle.setAttribute('aria-expanded', isExpanded);
        });

        document.addEventListener('click', function(event) {
            const isClickInsideToggle = mobileNavToggle.contains(event.target);
            const isClickInsideNav = mainNav.contains(event.target);
            const isNavOpen = mainNav.classList.contains('open');

            if (isNavOpen && !isClickInsideNav && !isClickInsideToggle) {
                mainNav.classList.remove('open');
                mobileNavToggle.classList.remove('open');
                mobileNavToggle.setAttribute('aria-expanded', false);
            }
        });
    }
});

const days = document.querySelectorAll('.day');
const popup = document.getElementById('dayPopup');
const popupCloseBtn = document.querySelector('.day-popup-close');
const popupDayTitle = document.getElementById('popupDayTitle');
const popupTaskList = document.getElementById('popupTaskList');

days.forEach(day => {
    day.addEventListener('click', function() {
        const dayName = this.getAttribute('data-day');
        const tasksHTML = this.querySelector('.day-tasks ul').innerHTML;

        popupDayTitle.textContent = dayName;
        popupTaskList.innerHTML = tasksHTML;
        popup.classList.add('open'); // Add 'open' class to trigger transition
        popup.style.display = "block"; // Ensure it's displayed
    });
});

popupCloseBtn.addEventListener('click', function() {
    popup.classList.remove('open'); // Remove 'open' class for closing transition
    setTimeout(() => {
        popup.style.display = "none"; // Hide after the transition
    }, 300); // Match the transition duration
});

// Close the popup if the user clicks outside of it
window.addEventListener('click', function(event) {
    if (event.target == popup) {
        popup.classList.remove('open'); // Remove 'open' class for closing transition
        setTimeout(() => {
            popup.style.display = "none"; // Hide after the transition
        }, 300); // Match the transition duration
    }
});