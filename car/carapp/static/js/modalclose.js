document.addEventListener("DOMContentLoaded", function () {
    // Находим все ссылки с классом close_modal_and_scroll
    const closeAndScrollLinks = document.querySelectorAll(".close_modal_and_scroll");

    closeAndScrollLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            // Закрываем модальное окно
            const modal = document.getElementById("economyWindow");
            if (modal) {
                modal.close(); // Закрываем окно
            }
        });
    });
});