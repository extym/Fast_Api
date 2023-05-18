$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const openBtn = '#createAccount';
    const modal = '#modal_createAccount';
    const modalContent = modal + ' .modal-content .ajaxContent';
    const form = modal + ' #accountForm';

    const modalLoader = '<div class="d-flex justify-content-center pt-20 pb-20"> <div class="spinner spinner-primary spinner-lg"></div> </div>';


    $(document).on('click', openBtn, function (e) {
        $(modal).modal('show');

        $.post("/dashboard/keys/load-form", null)
            .done(function (data) {
                if (data.success) {
                    $(modalContent).html(data.render);

                    // Autofocus
                    setTimeout(function () {
                        $(modalContent).find('input').get(0).focus();
                    }, 100);
                } else {
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

        let formData = $(form).serializeArray();

        $.post($(form).attr('action'), formData)
            .done(function (data) {
                if (data.success) {
                    $(modal).modal('toggle');
                    toastr.success('Аккаунт добавлен', 'Успешно');

                    if (pjaxContainerId) {
                        $.pjax.reload({container: pjaxContainerId, type: 'POST'});
                    }
                } else {
                    if (data.validation) {
                        $(form).yiiActiveForm('updateMessages', data.validation, true);
                    } else {
                        toastr.error(data.error, 'Ошибка');
                    }
                }
            })
            .fail(function (xhr, status, error) {
                toastr.error('Ошибка сервера', 'Ошибка');
            });
    });

    $(document).on('hidden.bs.modal', modal, function () {
        $(modalContent).html(modalLoader);
    });
});