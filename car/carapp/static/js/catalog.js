$(document).ready(function() {
    // Функция для загрузки моделей
    function loadModels(brand_id) {
        if (brand_id) {
            // Запросим модели для выбранного бренда
            $.ajax({
                url: '/ajax/load-models/',  // Путь для асинхронной загрузки моделей
                data: {
                    'brand_id': brand_id
                },
                success: function(data) {
                    // Очищаем текущие значения в поле модели
                    $('#model').html('<option value="">Модель авто</option>');
                    // Добавляем новые опции моделей
                    $.each(data, function(index, model) {
                        $('#model').append('<option value="' + model.model + '">' + model.model + '</option>');
                    });

                    // Восстанавливаем сохраненную модель, если она есть
                    const savedModel = localStorage.getItem('selectedModel');
                    if (savedModel) {
                        $('#model').val(savedModel);
                    }
                }
            });
        } else {
            // Если бренд не выбран, очищаем список моделей
            $('#model').html('<option value="">Модель авто</option>');
        }
    }

    // Слушаем изменение бренда
    $('#brand').change(function() {
        var brand_id = $(this).val();
        loadModels(brand_id);  // Загружаем модели при изменении бренда

        // Сохраняем выбранный бренд в localStorage
        localStorage.setItem('selectedBrand', brand_id);
    });

    // Слушаем изменение модели
    $('#model').change(function() {
        // Сохраняем выбранную модель в localStorage
        localStorage.setItem('selectedModel', $(this).val());
    });

    // Проверяем, есть ли сохраненный бренд в localStorage
    const savedBrand = localStorage.getItem('selectedBrand');
    if (savedBrand) {
        $('#brand').val(savedBrand);  // Устанавливаем сохраненный бренд
        loadModels(savedBrand);  // Загружаем модели для сохраненного бренда
    }

    // // Сортировка — это можно также отслеживать, если нужно
    // $('#sort').change(function() {
    //     $(this).closest('form').submit();  // Отправляем форму при изменении сортировки
    // });
});


$(document).ready(function() {
    // Автоматическая отправка формы при изменении поля сортировки или порядка
    $('#sort_field, #sort_order').change(function() {
        $(this).closest('form').submit();  // Отправляем форму при изменении любого из полей
    });
});
