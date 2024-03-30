$(document).ready(function ()
{
    $(document).on('click', '#hardParse', function ()
    {
        KTApp.blockPage({
            overlayColor: '#000000',
            state: 'primary',
            message: 'Выполняется запрос'
        });

        $.post("/dashboard/order/parse", {})
            .done(function (data)
            {
                toastr.success('Данные получены', 'Успешно');
            })
            .fail(function (xhr, status, error)
            {
                toastr.error('Ошибка сервера', 'Ошибка');
            })
            .always(function ()
            {
                $('#modal_updateLog').modal('show');

                KTApp.unblockPage();
            });
    });
});