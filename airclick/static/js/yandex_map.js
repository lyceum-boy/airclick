ymaps.ready(init);

function init() {
    // Создание карты.
    const myMap = new ymaps.Map("map", {
        center: [59.860382, 30.499457], // Координаты главного офиса AirClick.
        zoom: 16, // Уровень масштабирования.
    });

    // Добавляем метку.
    const myPlacemark = new ymaps.Placemark(
        [59.860382, 30.499457], // Координаты офиса.
        {
            hintContent: "AirClick, главный офис", // Текст хинта.
        },
        {
            preset: "islands#redIcon", // Визуальный стиль метки.
            iconCaption: "Главный офис: наб. Октябрьская, 122/2, оф. 74",
        }
    );

    myMap.geoObjects.add(myPlacemark);

    // Открытие хинта автоматически при загрузке карты.
    myPlacemark.hint.open(myMap.getCenter());
}
