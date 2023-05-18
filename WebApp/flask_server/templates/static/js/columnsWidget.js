$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const widgetWrapperSelector = '#columnsWidgetWrapper';
    const modalSelector = '#modal_columnsWidget';
    const columnsListSelector = '#columnsWrapper';
    const visibilityCheckboxesSelector = 'input[name="visibility"]';
    const columnsNameSelector = 'input[name="columnsName"]';
    const columnsTypeSelector = 'input[name="columnsType"]';
    const toggleAllInputSelector = 'input[name="toggleAll"]';

    const toggleAllButton = '#toggleAll';
    const saveButton = '.saveColumns';
    const resetButton = '.resetColumns';


    initSortable(columnsListSelector);


    $(document).on('pjax:end', function () {
        initSortable(columnsListSelector);
    });

    $(document).on('click', saveButton, function () {
        let widgetWrapper = $(this).closest(widgetWrapperSelector);
        let columnsName = widgetWrapper.find(columnsNameSelector).val();

        let columnsType = null;

        if (widgetWrapper.find(columnsTypeSelector).length) {
            columnsType = widgetWrapper.find(columnsTypeSelector).val();
        }

        if (columnsName) {
            let visibilityCheckboxes = widgetWrapper.find(visibilityCheckboxesSelector);
            let data = {};

            visibilityCheckboxes.each(function () {
                data[$(this).val()] = $(this).is(':checked') ? 1 : 0;
            });

            if (data) {
                $.post('/dashboard/settings/save-columns', {
                    'columns': data,
                    'columnsName': columnsName,
                    'columnsType': columnsType
                })
                    .done(function (data) {
                        if (data.success) {
                            toastr.success('Данные сохранены', 'Успешно');

                            $(modalSelector).modal('hide');

                            setTimeout(function () {
                                if (pjaxContainerId) {
                                    $.pjax.reload({container: pjaxContainerId, type: 'POST'});
                                }
                            }, 100);
                        } else {
                            toastr.error(data.error, 'Ошибка');
                        }
                    })
                    .fail(function (xhr, status, error) {
                        toastr.error('Ошибка сервера', 'Ошибка');
                    });
            }
        }
    });

    $(document).on('click', resetButton, function () {
        let widgetWrapper = $(this).closest(widgetWrapperSelector);
        let columnsName = widgetWrapper.find(columnsNameSelector).val();

        let columnsType = null;

        if (widgetWrapper.find(columnsTypeSelector).length) {
            columnsType = widgetWrapper.find(columnsTypeSelector).val();
        }

        if (columnsName) {
            Swal.fire({
                title: 'Вы уверены?',
                text: 'Сбросить настройки колонок до заводских',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Подтвердить действие',
                cancelButtonText: 'Отмена'
            }).then((result) => {
                if (result.isConfirmed) {
                    $.post('/dashboard/settings/reset-settings', {
                        'settingName': columnsName,
                        'settingType': columnsType
                    })
                        .done(function (data) {
                            if (data.success) {
                                toastr.success('Данные сохранены', 'Успешно');

                                $(modalSelector).modal('hide');

                                $(modalSelector).on('hidden.bs.modal', function () {
                                    if (pjaxContainerId) {
                                        $.pjax.reload({container: pjaxContainerId, type: 'POST'});
                                    }
                                })
                            } else {
                                toastr.error(data.error, 'Ошибка');
                            }
                        })
                        .fail(function (xhr, status, error) {
                            toastr.error('Ошибка сервера', 'Ошибка');
                        });
                }
            });
        }
    });

    $(document).on('click', toggleAllButton, function () {
        let widgetWrapper = $(this).closest(widgetWrapperSelector);
        let visibilityCheckboxes = widgetWrapper.find(visibilityCheckboxesSelector);

        let toggleStatus = parseInt($(toggleAllInputSelector).val());

        if (toggleStatus === 1) {
            visibilityCheckboxes.prop('checked', false);
            $(toggleAllInputSelector).val(0);
        } else {
            visibilityCheckboxes.prop('checked', true);
            $(toggleAllInputSelector).val(1);
        }
    });
});

function initSortable(elementsSelector) {
    if ($(elementsSelector).length !== 0) {
        Sortable.create($(elementsSelector).get(0), {
            ghostClass: 'drag',
            handle: '.handle',
            scroll: true,
            scrollSensitivity: 250,
            forceFallback: true,
            easing: 'cubic-bezier(0.2, 0, 0, 1)',
            animation: 150,
        });
    }
}