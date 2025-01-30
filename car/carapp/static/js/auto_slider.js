document.addEventListener("DOMContentLoaded", () => {
    // Функция для движения слайдов
    function move(panel, direction) {
        // let offset = panel.offset; // Начальный сдвиг для этой панели
        let translateWidth = panel.objects[0].offsetWidth;
        console.log(translateWidth);
        // Ограничиваем движение слайдов
        panel.offset += direction * translateWidth;
        panel.swipper.style.transform = `translateX(${panel.offset}px)`; // Применяем трансформацию
    }

    function move_triggers(panel, i){
        // let offset = panel.offset; // Начальный сдвиг для этой панели
        let translateWidth = panel.objects[0].offsetWidth;
        console.log(translateWidth);
        // Ограничиваем движение слайдов
        panel.offset = -i * translateWidth;
        panel.swipper.style.transform = `translateX(${panel.offset}px)`; // Применяем трансформацию
    }

    function change_active(panel, i, direction) {
        // console.log(panel.triggers);
        let active = panel.getElementsByClassName('active_img');
        console.log(active);
        active[0].classList.remove('active_img');
        panel.triggers[i].classList.add('active_img');
    }
    // Обработчик событий для всех панелей
    let panels = document.querySelectorAll('.auto_slider');
    // console.log(panels)
    panels.forEach(panel => {
        let swipper = panel.querySelector('.swipper');
        let offset = 0; // Начальный сдвиг
        panel.offset = offset; // Присваиваем сдвиг панеле
        panel.swipper = swipper; // Присваиваем элемент слайдера
        // console.log(swipper);
        let index_g = 0;

        // Обработчик кликов на панели
        panel.addEventListener('click', event => {
            let parent = event.target.parentNode;
            let objects = panel.getElementsByClassName('big_image');
            let triggers = panel.getElementsByClassName('mini_foto');
            panel.objects = objects;
            panel.triggers = triggers;
            // console.log(panel.triggers);

            // Проверка на навигацию вправо
            if (event.target.classList.contains('nav_right')) {
                // console.log("right");
                // console.log(event.target);
                let active = panel.getElementsByClassName('active_img');
                index= Array.from(triggers).indexOf(active[0])+1;
                move(panel, -1);
                change_active(panel, index, -1);
            }

            // Проверка на навигацию влево
            if (event.target.classList.contains('nav_left')) {
                // console.log("left");
                // console.log(event.target);
                let active = panel.getElementsByClassName('active_img');
                index= Array.from(triggers).indexOf(active[0])-1;
                move(panel, 1);
                change_active(panel, index, 1);
            }

            if (event.target.classList.contains('mini_foto')) {
                console.log("im a tirget")
                index = Array.from(triggers).indexOf(event.target);
                move_triggers(panel, index);
                change_active(panel, index, -1);
                // console.log(index);
            }
        });
    });
});
