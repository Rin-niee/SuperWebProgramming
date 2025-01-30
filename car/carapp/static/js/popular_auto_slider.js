// document.addEventListener("DOMContentLoaded", () => {
//     // Функция для движения слайдов
//     function move(panel, direction) {
//         let offset = panel.offset; // Начальный сдвиг для этой панели
//         let translateWidth = panel.querySelector('.popular_auto_item').offsetWidth + 16;
//         let maxOffset = panel.swipper.scrollWidth - panel.swipper.offsetWidth; // Максимальный сдвиг (последний элемент)

//         // Ограничиваем движение слайдов
//         offset += direction * (translateWidth + 30);
//         if (offset > 0) {
//             offset = 0; // Ограничение для движения влево
//         }
//         if (offset < -maxOffset) {
//             offset = -maxOffset; // Ограничение для движения вправо
//         }

//         panel.offset = offset; // Обновляем сдвиг
//         panel.swipper.style.transform = `translateX(${offset}px)`; // Применяем трансформацию
//     }

//     // Обработчик событий для всех панелей
//     let panels = document.querySelectorAll('.popular_auto');
//     panels.forEach(panel => {
//         let swipper = panel.querySelector('.swipper');
//         let offset = 20; // Начальный сдвиг
//         panel.offset = offset; // Присваиваем сдвиг панеле
//         panel.swipper = swipper; // Присваиваем элемент слайдера

//         // Обработчик кликов на панели
//         panel.addEventListener('click', event => {
//             let parent = event.target.parentNode;
//             let objects = panel.getElementsByClassName('popular_auto_item');
//             let index_g = 0;
//             let element_next = null;

//             // Проверка на навигацию вправо
//             if (event.target.classList.contains('nav_right')) {
//                 for (let i = 0; i < objects.length; i++) {
//                     let element = objects[i];
//                     if (element.classList.contains('item_big') && element.parentNode.id == parent.id) {
//                         index_g = i + 1;
//                         if (index_g < objects.length) { // Проверка на наличие следующего элемента
//                             element_next = objects[index_g];
//                             move(panel, -1);
//                             element.classList.remove('item_big');
//                         }
//                     }
//                 }
//                 if (element_next) {
//                     element_next.classList.add('item_big');
//                 }
//             }

//             // Проверка на навигацию влево
//             if (event.target.classList.contains('nav_left')) {
//                 for (let i = 0; i < objects.length; i++) {
//                     let element = objects[i];
//                     if (element.classList.contains('item_big') && element.parentNode.id == parent.id) {
//                         index_g = i - 1;
//                         if (index_g >= 0) { // Проверка на наличие предыдущего элемента
//                             element_next = objects[index_g];
//                             move(panel, 1);
//                             element.classList.remove('item_big');
//                         }
//                     }
//                 }
//                 if (element_next) {
//                     element_next.classList.add('item_big');
//                 }
//             }
//         });
//     });
// });






document.addEventListener("DOMContentLoaded", () => {
    // Функция для движения слайдов
    function move(panel, element, direction) {
        let offset = panel.offset; // Начальный сдвиг для этой панели
        let translateWidth = element.offsetWidth + 14;
        // let maxOffset = panel.swipper.scrollWidth - panel.swipper.offsetWidth; // Максимальный сдвиг (последний элемент)
        console.log(translateWidth);
        console.log(panel.querySelector('.popular_auto_item'));
        // Ограничиваем движение слайдов
        panel.offset += direction * (translateWidth + 30);
        // panel.offset = offset; // Обновляем сдвиг
        panel.swipper.style.transform = `translateX(${panel.offset}px)`; // Применяем трансформацию
    }

    // Обработчик событий для всех панелей
    let panels = document.querySelectorAll('.popular_auto');
    panels.forEach(panel => {
        let swipper = panel.querySelector('.swipper');
        let offset = 20; // Начальный сдвиг
        panel.offset = offset; // Присваиваем сдвиг панеле
        panel.swipper = swipper; // Присваиваем элемент слайдера

        // Обработчик кликов на панели
        panel.addEventListener('click', event => {
            let parent = event.target.parentNode;
            let objects = panel.getElementsByClassName('popular_auto_item');
            let index_g = 0;
            let element_next = null;

            // Проверка на навигацию вправо
            if (event.target.classList.contains('nav_right')) {
                for (let i = 0; i < objects.length; i++) {
                    let element = objects[i];
                    if (element.classList.contains('item_big') && element.parentNode.id == parent.id) {
                        index_g = i + 1;
                        if (index_g < objects.length) { // Проверка на наличие следующего элемента
                            element_next = objects[index_g];
                            move(panel, element_next, -1);
                            element.classList.remove('item_big');
                        }
                    }
                }
                if (element_next) {
                    element_next.classList.add('item_big');
                }
            }

            // Проверка на навигацию влево
            if (event.target.classList.contains('nav_left')) {
                for (let i = 0; i < objects.length; i++) {
                    let element = objects[i];
                    if (element.classList.contains('item_big') && element.parentNode.id == parent.id) {
                        index_g = i - 1;
                        if (index_g >= 0) { 
                            element_next = objects[index_g];
                            move(panel, element_next, 1);
                            element.classList.remove('item_big');
                        }
                    }
                }
                if (element_next) {
                    element_next.classList.add('item_big');
                }
            }
        });
    });
});
