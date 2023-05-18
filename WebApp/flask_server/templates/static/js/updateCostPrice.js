$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();
    const tableSelector = $('input[name="tableSelector"]').val();
    const updateBtn = tableSelector + ' .updateCostPrice';

    const modal = '#modal_updateCostPrice';
    const modalContent = modal + ' .ajaxContent';
    const form = modal + ' #updateProductForm';
    const submitBtn = modal + ' button[type="submit"]';

    const recalculateResultModal = '#modal_recalculateResult';
    const recalculateResultModalContent = recalculateResultModal + ' .modal-body';

    const modalLoader = '<div class="d-flex justify-content-center pt-20 pb-20"> <div class="spinner spinner-primary spinner-lg"></div> </div>';

    $(document).on('click', updateBtn, function (e) {
        let wbId = $(this).closest('tr').attr('data-wb-id');

        $(modal).modal('show');

        $.post("/dashboard/product/load-form", {'wbId': wbId, 'fields': ['costPrice']})
            .done(function (data) {
                if (data.success) {
                    $(modalContent).html(data.render);

                    if ($(form).length !== 0) {
                        if (data['initRecalculateWidget']) {
                            $.event.trigger('initRecalculateForm', {'form': form});
                        }

                        setTimeout(function () {
                            moveCursorToEnd('input[name="Product[costPrice]"]');
                        }, 300);
                    }
                }
                else {
                    toastr.error(data.error, 'Ошибка');
                }
            })
            .fail(function (xhr, status, error) {
                toastr.error('Ошибка сервера', 'Ошибка');
            });

        e.preventDefault();
    });

    $(document).on('submit', form, function (e) {
        e.preventDefault();

        KTUtil.addClass($(submitBtn)[0], 'disabled');
        KTUtil.btnWait($(submitBtn)[0], "spinner spinner-left spinner-white pl-15", "Обработка запроса")

        let formData = $(form).serializeArray();

        $.post($(form).attr('action'), formData)
            .done(function (data) {
                if (data.success) {
                    toastr.success('Товар сохранен', 'Успешно');

                    if (data.hasOwnProperty('recalculate'))
                    {
                        if (data.recalculate.hasOwnProperty('validation')) {
                            $(form).yiiActiveForm('updateMessages', data.recalculate.validation, true);
                        }
                        else
                        {
                            $(modal).modal('toggle');

                            if (data.recalculate.hasOwnProperty('render')) {
                                if ($(recalculateResultModal).length) {
                                    $(recalculateResultModalContent).html(data.recalculate.render);

                                    setTimeout(function(){
                                        $(recalculateResultModal).modal('show');
                                    }, 1000);
                                }
                            }
                        }
                    }
                    else
                    {
                        $(modal).modal('toggle');
                    }

                    if (pjaxContainerId) {
                        $.pjax.reload({container: pjaxContainerId, type: 'POST'});
                    }
                }
                else {
                    if (data.hasOwnProperty('validation')) {
                        $(form).yiiActiveForm('updateMessages', data.validation, true);
                    }
                    else {
                        toastr.error(data.error, 'Ошибка');
                    }
                }
            })
            .fail(function (xhr, status, error) {
                toastr.error('Ошибка сервера', 'Ошибка');
            })
            .always(function() {
                KTUtil.btnRelease($(submitBtn)[0]);
                KTUtil.removeClass($(submitBtn)[0], 'disabled');
            });
    });

    $(document).on('hidden.bs.modal', modal, function () {
        $(modalContent).html(modalLoader);
    });
});