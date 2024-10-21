document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const saveBtn = document.querySelector('[name="_save"]');
    const spinner = document.createElement('div');

    spinner.className = 'loading-spinner';
    spinner.style.display = 'none';

    form.appendChild(spinner);

    saveBtn.addEventListener('click', function () {
        spinner.style.display = 'block';
    });
});
