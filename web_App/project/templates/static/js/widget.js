$(document).ready(function () {
    const modal = $('#modal_firstTutorial');

    // Get settings
    const show = parseInt(modal.find('input[name="showFirstTutorialModal"]').val());
    const step = parseInt(modal.find('input[name="firstTutorialStep"]').val());

    if (show === 0) {  //if (show === 1) {  //<-- itis default code TODO
        setTimeout(function () {
            modal.modal('show');
        }, 300);
    }

    $(document).on('click', '#finishFirstTutorial', function () {
        $.post('/dashboard/widget-actions/end-first-tutorial', null)
            .done(function (data) {
                $(modal).modal('hide');
            })
            .fail(function (xhr, status, error) {
                toastr.error('Ошибка сервера', 'Ошибка');
            });
    });

    $(document).on('keyCreated', function (event, data) {
        if (step === 1) {
            $.post('/dashboard/widget-actions/refresh-tutorial', null)
                .done(function (data) {
                    $(modal).find('#firstTutorialAjaxContent').html(data);

                    setTimeout(function () {
                        $(modal).modal('show');
                    }, 300);
                })
                .fail(function (xhr, status, error) {
                    toastr.error('Ошибка сервера', 'Ошибка');
                });
        }
    });
});