$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();
    const button = '.toggleActive';

    $(document).on('click', button, function (event) {
        let row = $(this).closest('tr');
        let accountId = row.attr('data-key');

        $.post('/dashboard/keys/toggle-active', {'accountId': accountId})
            .done(function (data) {
                if (data.success) {
                    if (pjaxContainerId) {
                        $.pjax.reload({container: pjaxContainerId, type: 'POST'});
                    }
                } else {
                    toastr.error(data.error, 'Ошибка');

                }
            })
            .fail(function (xhr, status, error) {
                toastr.error('Ошибка сервера', 'Ошибка');
            });
    });
});