$(document).ready(function () {
    const widgetWrapper = '#currencyWidget';

    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const openModalBtn = '#currencyBtn';
    const saveBtn = '#saveCurrency';
    const modal = '#modal_currency';

    const currencyInfoInput = 'input[name="currencyInfo"]';

    const enableRealUsdRateInput = 'input[name="enableRealUsdRate"]';
    const enableRealCnyRateInput = 'input[name="enableRealCnyRate"]';

    const userUsdRateInput = 'input[name="userUsdRate"]';
    const userCnyRateInput = 'input[name="userCnyRate"]';

    const enableUsdMultiplierInput = 'input[name="enableUsdMultiplier"]';
    const enableCnyMultiplierInput = 'input[name="enableCnyMultiplier"]';

    const usdMultiplierInput = 'input[name="usdMultiplier"]';
    const cnyMultiplierInput = 'input[name="cnyMultiplier"]';

    const usdRateInput = 'input[name="usdRate"]';
    const cnyRateInput = 'input[name="cnyRate"]';

    let currencyInfo = $.parseJSON($(currencyInfoInput).val());


    $(document).on('click', saveBtn, function () {
        let formData = $('#currencyInfoForm').serializeArray();

        $.post("/dashboard/currency/load", formData)
            .done(function (data) {
                if (data.success) {
                    $(modal).modal('toggle');
                    if (pjaxContainerId) {
                        $.pjax.reload({container: pjaxContainerId, type: 'POST'});
                    }

                    $(widgetWrapper + ' .currencyWidgetBtn').html(data.render.btn);
                    $(widgetWrapper + ' .currencyWidgetModal .modal-body').html(data.render.modal);

                    if(data.hasOwnProperty('recalculate')) {
                        if (data.recalculate.hasOwnProperty('render')) {
                            $.event.trigger('showRecalculateResultModal', {'render': data.recalculate.render});
                        }
                    }
                }
                else {
                    toastr.error(data.error, 'Ошибка');
                }
            })
            .fail(function (xhr, status, error) {
                toastr.error('Ошибка сервера', 'Ошибка');
            });
    });


    $(document).on('change', enableRealUsdRateInput, function () {
        if ($(this).is(':checked')) {
            $(usdRateInput).addClass('inactive');
            $(usdRateInput).prop('readonly', true);

            $(enableUsdMultiplierInput).prop('checked', false);
            $(usdMultiplierInput).prop('disabled', true);
            $(usdMultiplierInput).val(null);

            $(usdRateInput).val(currencyInfo.realRate.USD.value);
        }
        else {
            $(usdRateInput).removeClass('inactive');
            $(usdRateInput).prop('readonly', false);
        }
    });

    $(document).on('change', enableRealCnyRateInput, function () {
        if ($(this).is(':checked')) {
            $(cnyRateInput).addClass('inactive');
            $(cnyRateInput).prop('readonly', true);

            $(enableCnyMultiplierInput).prop('checked', false);
            $(cnyMultiplierInput).prop('disabled', true);
            $(cnyMultiplierInput).val(null);

            $(cnyRateInput).val(currencyInfo.realRate.CNY.value);
        }
        else {
            $(cnyRateInput).removeClass('inactive');
            $(cnyRateInput).prop('readonly', false);
        }
    });


    $(document).on('change', enableUsdMultiplierInput, function () {
        if ($(this).is(':checked')) {
            $(usdMultiplierInput).prop('disabled', false);

            $(enableRealUsdRateInput).prop('checked', false);
            $(usdRateInput).val(currencyInfo.realRate.USD.value);

            $(usdRateInput).addClass('inactive');
            $(usdRateInput).prop('readonly', true);

        }
        else {
            $(usdMultiplierInput).prop('disabled', true);

            $(enableRealUsdRateInput).prop('checked', true);
            $(usdRateInput).val(currencyInfo.realRate.USD.value);

            $(usdRateInput).addClass('inactive');
            $(usdRateInput).prop('readonly', true);
        }
    });


    $(document).on('change', enableCnyMultiplierInput, function () {
        if ($(this).is(':checked')) {
            $(cnyMultiplierInput).prop('disabled', false);

            $(enableRealCnyRateInput).prop('checked', false);
            $(cnyRateInput).val(currencyInfo.realRate.CNY.value);

            $(cnyRateInput).addClass('inactive');
            $(cnyRateInput).prop('readonly', true);

        }
        else {
            $(cnyMultiplierInput).prop('disabled', true);

            $(enableRealCnyRateInput).prop('checked', true);
            $(cnyRateInput).val(currencyInfo.realRate.CNY.value);

            $(cnyRateInput).addClass('inactive');
            $(cnyRateInput).prop('readonly', true);
        }
    });


    $(document).on('click', openModalBtn, function () {
        $(modal).modal('show');
    });
});