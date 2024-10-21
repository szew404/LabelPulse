document.addEventListener('DOMContentLoaded', function () {
    const isPopup = window.location.search.includes('_popup=1');
    const form = document.querySelector('form');
    const saveBtn = document.querySelector('[name="_save"]');
    const spinner = document.createElement('div');

    spinner.className = 'loading-spinner';
    spinner.style.display = 'none';
    form.appendChild(spinner);

    saveBtn.addEventListener('click', function () {
        spinner.style.display = 'block';

        if (isPopup) {
            form.style.opacity = '0.5';
        }
    });
});