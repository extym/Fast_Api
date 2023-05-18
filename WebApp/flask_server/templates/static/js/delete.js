$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();
    const deleteBtn = '.deleteAccount';

    $(document).on('click', deleteBtn, function (e) {
        let accountId = $(this).closest('tr').attr('data-key');

        if (accountId) {
            Swal.fire({
                title: 'Вы уверены?',
                text: "Отменить это действие будет невозможно",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Да, удалить',
                cancelButtonText: 'Отмена'
            }).then((result) => {
                if (result.isConfirmed) {
                    $.post('/dashboard/keys/delete', {'accountId': accountId})
                        .done(function (data) {
                            if (data.success) {
                                toastr.success('Аккаунт удален', 'Успешно');

                                if (pjaxContainerId) {
                                    $.pjax.reload({container: pjaxContainerId, type: 'POST'});
                                }
                            }
                            else {
                                toastr.error(data.error, 'Ошибка');
                            }
                        })
                        .fail(function (xhr, status, error) {
                            toastr.error('Ошибка сервера', 'Ошибка');
                        });
                }
            });
        }
        else {
            toastr.error('Не удалось получить ID аккаунта', 'Ошибка');
        }

        e.preventDefault();
    });
});