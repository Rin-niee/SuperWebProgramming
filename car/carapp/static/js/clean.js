$(document).ready(function() {
    $('.empty_btn').click(function(e) {
        e.preventDefault(); // Предотвращает стандартное поведение кнопки

        // Очищаем поля бренда и модели
        $('#brand').val('');
        $('#model').html('<option value="">Модель авто</option>');  // Очищаем список моделей

        // Удаляем сохраненные данные из localStorage
        localStorage.removeItem('selectedBrand');
        localStorage.removeItem('selectedModel');

        // Получаем целевой URL из атрибута data-target-url
        const targetPage = $(this).data('target-url');

        // Проверяем текущий URL
        if (window.location.href !== targetPage) {
            // Если текущая страница не целевая, переходим на целевую страницу
            window.location.href = targetPage;
        } else {
            // // Если уже на целевой странице, ничего не делаем
            // console.log("Вы уже на целевой странице.");
        }
    });
});
