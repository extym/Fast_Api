$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();
    const toggleAutoWithdrawalSwitch = 'input[name="toggleAutoWithdrawal"]';

    $(document).on('change', toggleAutoWithdrawalSwitch, function () {
        let url = $(this).attr('data-url');

        $.post(url)
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