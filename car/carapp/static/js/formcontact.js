document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('contactForm');
    const fields = form.querySelectorAll('input[required], textarea[required]');
    const phoneRegex = /^\+?1?\d{9,15}$/;

    // Функция для показа ошибки
    function showError(input, message) {
        const errorMessage = form.querySelector(`.error-message[data-error-for="${input.name}"]`);
        errorMessage.textContent = message;
        errorMessage.style.color = 'red';
    }

    // Функция для скрытия ошибки
    function hideError(input) {
        const errorMessage = form.querySelector(`.error-message[data-error-for="${input.name}"]`);
        errorMessage.textContent = '';
    }

    // Проверка каждого поля
    function validateField(input) {
        if (!input.value.trim()) {
            showError(input, 'Поле обязательно для заполнения.');
            return false;
        }
        if (input.name === 'number' && !phoneRegex.test(input.value.trim())) {
            showError(input, 'Введите номер телефона в формате "+999999999".');
            return false;
        }
        if (input.name === 'check' && !input.checked) {
            showError(input, 'Вы должны согласиться с условиями.');
            return false;
        }
        hideError(input);
        return true;
    }

    // Добавление событий на поля
    fields.forEach(function (field) {
        field.addEventListener('input', function () {
            validateField(field); // Проверка при вводе
        });

        field.addEventListener('blur', function () {
            validateField(field); // Проверка при потере фокуса
        });
    });

    // Проверка всей формы при отправке
    form.addEventListener('submit', function (e) {
        let isValid = true;
        fields.forEach(function (field) {
            if (!validateField(field)) {
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault(); // Остановить отправку формы
        }
    });
});