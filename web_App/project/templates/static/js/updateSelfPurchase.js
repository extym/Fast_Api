$(document).ready(function () {
    const tableSelector = $('input[name="tableSelector"]').val();
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const updateBtn = tableSelector + ' .updateSelfPurchase';

    const modal = '#modal_selfPurchase';
    const modal_content = modal + ' .ajaxContent';
    const modal_form = modal + ' #selfPurchaseForm';
    const isSelfPurchase_input = modal + ' input[name="isSelfPurchase"]';
    const modal_submit = modal + ' .save-changes';


    $(document).on('click', updateBtn, function (e) {
        let row = $(this).closest('tr');

        let orderNumber = row.attr('data-number');
        let odId = row.attr('data-od-id');

        $(modal).modal('show');

        $.post("/dashboard/order/load-self-purchase-form", {'number': orderNumber, 'odId': odId})
            .done(function (data) {
                if (data.success) {
                    $(modal_content).html(data.render);
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

    $(document).on('click', modal_submit, function (e) {
        e.preventDefault();

        $(modal_submit).addClass('spinner spinner-white spinner-left disabled');
        $(modal_submit).text('Обновление');

        let formData = $(modal_form).serializeArray();

        $.post($(modal_form).attr('action'), formData)
            .done(function (data) {
                if (data.success) {
                    $(modal).modal('hide');

                    $.pjax.reload({container: pjaxContainerId, type: 'POST'});
                    toastr.success('Данные сохранены', 'Успешно')
                }
                else {
                    toastr.error(data.error, 'Ошибка');
                }
            })
            .fail(function (xhr, status, error) {
                toastr.error('Ошибка сервера', 'Ошибка');
            });
    });
});