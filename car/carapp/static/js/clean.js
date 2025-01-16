$('.empty_btn').click(function(e) {
    e.preventDefault();
    localStorage.removeItem('selectedBrand');
    localStorage.removeItem('selectedModel');
    // Очищаем поля бренда и модели
    $('#brand').val('');
    $('#model').html('<option value="">Модель авто</option>');  // Очищаем список моделей

    // Удаляем сохраненные данные из localStorage
    localStorage.removeItem('selectedBrand');
    localStorage.removeItem('selectedModel');
});