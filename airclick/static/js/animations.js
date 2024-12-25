document.addEventListener("DOMContentLoaded", function () {
    // Найти все кнопки на странице.
    const buttons = document.querySelectorAll(".btn");

    buttons.forEach((button) => {
        // Добавляет событие при наведении.
        button.addEventListener("mouseover", () => {
            button.classList.add("btn-hover");
        });

        // Убирает эффект после наведения.
        button.addEventListener("mouseout", () => {
            button.classList.remove("btn-hover");
        });
    });

    // Найти все карточки на странице.
    const cards = document.querySelectorAll(".animated-card");

    cards.forEach((card) => {
        // Добавляет событие при наведении.
        card.addEventListener("mouseover", () => {
            card.style.transform = "rotate(1deg)";
        });

        // Убирает эффект после наведения.
        card.addEventListener("mouseout", () => {
            card.style.transform = "rotate(0)";
        });
    });
});
