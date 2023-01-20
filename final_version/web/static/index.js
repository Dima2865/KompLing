// Эта функция отправляет запрос по адресу /parse, который
// инициализирует парсинг новостей с первой страницы
function updateDatabaseRecords() {
    // Прилепляем уведомление о загрузке
    $("#upd-results-records").html(`Fetching...`)
    let n = $('#parse-input-records').val()

    // Посылаем запрос при помощи jquery
    $.getJSON(`/parse?n=${n}`, function (data) {
        // Это коллбэк на результат запроса

        // Находим тэг где кнопка
        const results = $("#upd-results-records")

        // Если успешно
        if (data.code === 200) {
            if (data.count > 0)
                results.html(`Success! ${data.count} articles added`)
            else
                results.html(`No articles was found or updated`)

        } else {
            results.html(`Error: ${data.code} ${data.name}`)
        }

    }).fail(function (data) {
        //Коллбэк на ошибку
        $("#upd-results-records").html(`Error: ${data.status} ${data.statusText}`)
    })

}


function updateDatabaseByDate() {
    // Прилепляем уведомление о загрузке
    $("#upd-results-by-date").html(`Fetching...`)
    let date = $('#parse-input-by-date').val()

    // Посылаем запрос при помощи jquery
    $.getJSON(`/parse?date=${date}`, function (data) {
        // Это коллбэк на результат запроса

        // Находим тэг где кнопка
        const results = $("#upd-results-by-date")

        // Если успешно
        if (data.code === 200) {
            if (data.count > 0)
                results.html(`Success! ${data.count} articles added`)
            else
                results.html(`No articles was found or updated`)

        } else {
            results.html(`Error: ${data.code} ${data.name}`)
        }

    }).fail(function (data) {
        //Коллбэк на ошибку
        $("#upd-results-by-date").html(`Error: ${data.status} ${data.statusText}`)
    })

}


var previous = 1

function validate(input_field) {
    const pattern = /^((\w+)-?(\w+)?)?$/

    if (pattern.test(input_field.value))
        previous = input_field.value
    else
        input_field.value = previous
}
