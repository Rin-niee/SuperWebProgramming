function formatPhoneNumber(input) {
    // Удаляем все символы, кроме цифр
    let value = input.value.replace(/\D/g, '');

    // Если номер меньше 1, возвращаем
    if (value.length < 1) {
        input.value = '+7';
        return;
    }

    // Если номер больше 1, добавляем код страны
    if (value.length === 1) {
        input.value = '+7';
        return;
    }

    // Форматируем номер
    let formattedNumber = '+7 ';
    if (value.length > 1) {
        formattedNumber += value.substring(1, 4); // 3 цифры
    }
    if (value.length >= 4) {
        formattedNumber += ' ' + value.substring(4, 7); // 2 цифры
    }
    if (value.length >= 6) {
        formattedNumber += ' ' + value.substring(7, 9); // 2 цифры
    }
    if (value.length >= 8) {
        formattedNumber += ' ' + value.substring(9, 11); // 2 цифры
    }

    input.value = formattedNumber.trim();
}


function handleSubmit() {
    const nameInput = document.getElementById('user_name');
    const phoneInput = document.getElementById('user_phone');
    const questInput = document.getElementById('user_quest');
    const checkInput = document.getElementById('user_agreement');

    // Проверка имени на корректность (только русские буквы и пробелы)
    const nameRegex = /^[А-Яа-яЁё\s]+$/;
    if (!nameRegex.test(nameInput.value)) {
        alert('Имя должно содержать только русские буквы и пробелы.');
        return false;
    }
    // Проверка номера телефона на соответствие формату
    const phoneRegex = /^\+7 \d{3} \d{3} \d{2} \d{2}$/; // Обновленный формат с пробелами
    if (!phoneRegex.test(phoneInput.value)) {
        alert('Номер телефона должен соответствовать формату +7 999 999 99 99.');
        return false;
    }

    if (!checkInput.checked) {
        alert('Пожалуйста, подтвердите согласие на обработку персональных данных.'); // Сообщение об ошибке
        return false;
    }
    // Если все проверки пройдены, форма отправляется
    const formData = new FormData();
    formData.append('name', nameInput.value);
    formData.append('number', phoneInput.value);
    formData.append('message', questInput.value);
    formData.append('check', checkInput.checked);

    fetch('', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // Добавляем CSRF токен
        }
    })
    .then(response => response.json())
    .then(data => {
        // Обработка успешного ответа
        alert('Форма успешно отправлена!');
        // Вы можете обновить UI или выполнить другие действия здесь
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });

    return false; // Предотвращаем стандартное поведение формы
}