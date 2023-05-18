$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const openBtn = '.updateAccount';
    const modal = '#modal_updateAccount';
    const modalContent = modal + ' .modal-content .ajaxContent';
    const form = modal + ' #accountForm';
    const submitBtnId = 'accountFormSubmit';

    const recalculateResultModal = '#modal_recalculateResult';
    const recalculateResultModalContent = recalculateResultModal + ' .modal-body';

    const modalLoader = '<div class="d-flex justify-content-center pt-20 pb-20"> <div class="spinner spinner-primary spinner-lg"></div> </div>';

    $(document).on('click', openBtn, function (e) {
        $(modal).modal('show');

        $.post($(this).attr('href'), null)
            .done(function (data) {
                if (data.success) {
                    $(modalContent).html(data.render);

                    $.event.trigger('initRecalculateForm', {'form': form});
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

        // Block button
        let btn = KTUtil.getById(submitBtnId);

        KTUtil.addClass(btn, 'disabled');
        KTUtil.btnWait(btn, "spinner spinner-left spinner-white pl-15", "Обработка запроса");

        let formData = $(form).serializeArray();

        $.post($(form).attr('action'), formData)
            .done(function (data) {

                if (data.success) {
                    toastr.success('Аккаунт сохранен', 'Успешно');

                    if (data.hasOwnProperty('recalculate'))
                    {
                        if (data.recalculate.hasOwnProperty('validation')) {
                            $(form).yiiActiveForm('updateMessages', data.recalculate.validation, true);
                        }
                        else
                        {
                            $(modal).modal('toggle');

                            if (data.recalculate.hasOwnProperty('render'))
                            {
                                $.event.trigger('showRecalculateResultModal', {'render': data.recalculate.render});
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
                KTUtil.btnRelease(btn);
                KTUtil.removeClass(btn, 'disabled');
            });
    });

    $(document).on('hidden.bs.modal', modal, function () {
        $(modalContent).html(modalLoader);
    });
});