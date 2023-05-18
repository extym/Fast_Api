$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const checkboxSelector = '.select-item';
    const massActionsButtonSelector = '.mass-actions-button';
    const selectAllButtonSelector = '.select-all-items';

    const inactiveSelectedSelector = '.mass-actions .inactive-selected';
    const activeSelectedSelector = '.mass-actions .active-selected';
    const deleteSelectedSelector = '.mass-actions .delete-selected';

    const ajaxTableDataSelector = '.ajax-table-data';
    const blockElement = '.card';

    $(document).on('click', inactiveSelectedSelector + ", " + activeSelectedSelector, function (event) {
        let selectedItems = $(checkboxSelector + ':checked');
        let state = $(this).data('state');
        let itemsArray = [];

        if (selectedItems.length) {
            selectedItems.each(function () {
                let itemId = $(this).closest('tr').find('input[name="item_id"]').val();

                itemsArray.push(itemId);
            });

            $.post('/dashboard/keys/change-active', {'accountIds': JSON.stringify(itemsArray), 'state': state})
                .done(function (data) {
                    if (data.success) {
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

        event.preventDefault();
    });

    $(document).on('click', deleteSelectedSelector, function (event) {
        Swal.fire({
            title: 'Вы уверены?',
            text: "Отменить это действие будет невозможно",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Да, удалить',
            cancelButtonText: 'Отмена'
        }).then((result) => {
            if (result.isConfirmed) {
                KTApp.block(blockElement, {message: "Обработка..."});

                let selectedItems = $(checkboxSelector + ':checked');
                let accountIds = [];

                if (selectedItems.length) {
                    selectedItems.each(function () {
                        let itemId = $(this).closest('tr').find('input[name="item_id"]').val();

                        accountIds.push(itemId);
                    });

                    $.post('/dashboard/keys/delete', {'accountIds': JSON.stringify(accountIds)})
                        .done(function (data) {
                            if (data.success) {
                                toastr.success('Аккаунты удалены', 'Успешно');

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
            }
        });

        event.preventDefault();
    });

    // Скрытие кнопки массовых действий
    $(document).ajaxSuccess(function () {
        setTimeout(function () {
            $(massActionsButtonSelector).fadeOut(100);
        }, 300);
    });

    // Скрытие и отображение кнопки массовых действий
    $(document).on('click', checkboxSelector, function (event) {
        let selectedItems = $(checkboxSelector + ':checked');

        if (selectedItems.length) {
            $(massActionsButtonSelector).fadeIn(100);
        }
        else {
            $(massActionsButtonSelector).fadeOut(100);
        }
    });

    // Выбрать все, отключить все
    $(document).on('click', selectAllButtonSelector, function (event) {
        if ($(this).is(':checked')) {
            $(checkboxSelector).attr('checked', 'checked');
            $(massActionsButtonSelector).fadeIn(100);
        }
        else {
            $(checkboxSelector).removeAttr('checked');
            $(massActionsButtonSelector).fadeOut(100);
        }
    });
});