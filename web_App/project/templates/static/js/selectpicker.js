$(document).ready(function () {
    const options = {deselectAllText: 'Отключить все', selectAllText: 'Выбрать все'};

    $('.selectpicker').selectpicker(options);

    $(document).on('ajaxComplete', function (event, request, settings) {
        $('.selectpicker').selectpicker(options);
    });
});