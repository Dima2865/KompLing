// Нарисовать стрелочки в заголовках таблицы
function setSortLabels() {
    // Параметры запроса
    const params = new URLSearchParams(window.location.search)

    // Определяем поле для сортировки
    let id = params.get('sort')

    // Если не в списке, игнорируем
    if (!ids.includes(id))
        return

    // Порядок сортировки
    let order = parseInt(params.get('order'))

    // 0 по умолчанию
    if (isNaN(order) || order > 1)
        order = 0

    // Получаем тэг заголовка
    const header = $('#' + id)

    // Добавляем соответствующую стрелку
    header.append(`<i class="arrow ${order ? 'down' : 'up'}"></i>`)

    // И добавляем коллбэк для обратной сортировки
    header.click(function () {
        sortBy(id, 1 - order, params.get('only'))
    })
}

function sortBy(column, order=0, only=null) {
    let params = {page: 0, sort: column, order: order}

    if (only != null)
        params.only = only

    location.assign(`${window.location.pathname}?${
        jQuery.param(params)
    }`)
}

window.onload = function () {
    const params = new URLSearchParams(window.location.search)

    $('.iSortable').click(function () {
        sortBy(this.id, 0, params.get('only'))
    })

    setSortLabels()
}
