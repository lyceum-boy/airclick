// Динамический расчёт отступа при адаптивной шапке сайта.
document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.querySelector('.navbar.fixed-top');
    if (navbar) {
        document.body.style.paddingTop = `${navbar.offsetHeight}px`;
    }
});
