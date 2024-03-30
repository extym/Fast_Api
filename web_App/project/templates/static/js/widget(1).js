$(document).ready(function ()
{
    const wrapper = '#recalculateWidget';
    const recalculateForm = wrapper + ' .recalculateForm';
    const activeInput = wrapper + ' input[name="Recalculate[active]"]';
    const dateRangeInput = wrapper + ' input[name="Recalculate[dateRange]"]';
    const dateFromInput = wrapper + ' input[name="Recalculate[dateFrom]"]';
    const dateToInput = wrapper + ' input[name="Recalculate[dateTo]"]';
    const updateTypeRadio = wrapper + ' input[name="Recalculate[updateType]"]';
    const updateAllCheckbox = wrapper + ' input[name="Recalculate[updateType]"].updateAll';
    const updateRangeCheckbox = wrapper + ' input[name="Recalculate[updateType]"].updateByRange';
    const dateTimeRangeWrapper = wrapper + ' .dateTimeRangeWrapper';

    const timeSelectInput = wrapper + ' .timeSelect';
    const timeSelectFrom = wrapper + ' #recalculateDateFrom';
    const timeSelectTo = wrapper + ' #recalculateDateTo';

    const recalculateAlreadyFixedInput = wrapper + ' input[name="Recalculate[recalculateAlreadyFixed]"]';
    const recalculateFixedHiddenOptions = wrapper + ' .recalculateFixedHiddenOptions';

    const useCustomRateInput = wrapper + ' input[name="Recalculate[useCustomRate]"]';
    const useCustomRateHiddenOptions = wrapper + ' .setCustomRate';

    const commissionInputWrapper = '.commissionInputWrapper';
    const commissionTypeInput = '.commissionTypeInput';
    const commissionValueInput = '.commissionValueInput';
    const commissionType = '.selectType .type';
    const commissionTypeValue = '.typeValue';
    const commissionValueDescription = '.valueDescription';

    const customCommissionType = 'input[name="Recalculate[customCommissionType]"]';
    const customLogisticType = 'input[name="Recalculate[customLogisticType]"]';
    const recalculateCommissionInput = 'input[name="Recalculate[recalculateCommission]"]';
    const useCustomCommissionInput = 'input[name="Recalculate[useCustomCommission]"]';

    const recalculateResultModal = '#modal_recalculateResult';
    const recalculateResultModalContent = recalculateResultModal + ' .modal-body';

    $(document).on('change', '.numberInput', function (e)
    {
        $(this).val(function (index, currentValue)
        {
            return currentValue.replace(/,/g, '.');
        });
    });


    $(document).on('change', updateTypeRadio, function ()
    {
        let updateType = $(updateTypeRadio + ':checked').val();

        if (updateType === 'ALL')
        {
            $(dateTimeRangeWrapper).addClass('disabled');
        }
        else
        {
            $(dateTimeRangeWrapper).removeClass('disabled');
        }
    });

    $(document).on('change', recalculateCommissionInput, function ()
    {
        if ($(this).is(':checked'))
        {
            $('.recalculateCommissionHiddenOptions').fadeIn(300);
        }
        else
        {
            $('.recalculateCommissionHiddenOptions').fadeOut(300);
        }
    });

    $(document).on('change', useCustomCommissionInput, function ()
    {
        let value = $(this).val();

        if (value == 1)
        {
            $('.customCommission').fadeIn(300);
        }
        else
        {
            $('.customCommission').fadeOut(300);
        }
    });

    $(document).on('click', commissionType, function ()
    {
        let inputWrapper = $(this).closest(commissionInputWrapper);
        let typeInput = inputWrapper.find(commissionTypeInput);
        let valueInput = inputWrapper.find(commissionValueInput);
        let description = inputWrapper.find(commissionValueDescription);

        let type = $(this).data('value');
        let typeName = $(this).data('name');
        let paramType = inputWrapper.data('type');

        let value = valueInput.val();

        if (value)
        {
            let descriptionText = (value > 0 ? 'Увеличение' : 'Уменьшение') + ' ' + (paramType == 'commission' ? (type == 'percent' ? 'процента комиссии' : 'комиссии') : 'логистики') + ' на ' + Math.abs(value) + (type == 'percent' ? '%' : '₽');
            description.text(descriptionText);

            if (value > 0)
            {
                description.removeClass('down').addClass('up');
            }
            else
            {
                description.removeClass('up').addClass('down');
            }
        }
        else
        {
            description.text('');
        }

        inputWrapper.find(commissionTypeValue).text(typeName);
        typeInput.val(type);
    });

    $(document).on('input', commissionValueInput, function ()
    {
        let inputWrapper = $(this).closest(commissionInputWrapper);
        let typeInput = inputWrapper.find(commissionTypeInput);
        let description = inputWrapper.find(commissionValueDescription);

        let type = typeInput.val();
        let value = $(this).val();
        let paramType = inputWrapper.data('type');

        if (value)
        {
            let descriptionText = (value > 0 ? 'Увеличение' : 'Уменьшение') + ' ' + (paramType == 'commission' ? (type == 'percent' ? 'процента комиссии' : 'комиссии') : 'логистики') + ' на ' + Math.abs(value) + (type == 'percent' ? '%' : '₽');
            description.text(descriptionText);

            if (value > 0)
            {
                description.removeClass('down').addClass('up');
            }
            else
            {
                description.removeClass('up').addClass('down');
            }
        }
        else
        {
            description.text('');
        }
    });


    $(document).on('change', activeInput, function ()
    {
        if ($(this).is(':checked'))
        {
            $(recalculateForm).addClass('active');
            $(activeInput).val(1);
        }
        else
        {
            $(recalculateForm).removeClass('active');
            $(activeInput).val(0);
        }
    });

    $(document).on('change', recalculateAlreadyFixedInput, function ()
    {
        if ($(this).is(':checked'))
        {
            $(recalculateFixedHiddenOptions).fadeIn();
        }
        else
        {
            $(recalculateFixedHiddenOptions).fadeOut();
        }
    });

    $(document).on('change', useCustomRateInput, function ()
    {
        $(useCustomRateHiddenOptions).toggleClass('disabled');
    });


    $(document).on('initRecalculateForm', function (event, data)
    {
        $(data.form).yiiActiveForm('add', {
            id: 'recalculate-daterange',
            name: 'Recalculate[dateRange]',
            container: '.field-recalculate-daterange',
            input: '#recalculate-daterange',
            error: '.help-block'
        });

        $(data.form).yiiActiveForm('add', {
            id: 'recalculate-usdrate',
            name: 'Recalculate[usdRate]',
            container: '.field-usdRate',
            input: '#recalculate-usdrate',
            error: '.help-block'
        });

        $(data.form).yiiActiveForm('add', {
            id: 'recalculate-cnyrate',
            name: 'Recalculate[cnyRate]',
            container: '.field-cnyRate',
            input: '#recalculate-cnyrate',
            error: '.help-block'
        });

        initDateRangeSelect();
        initTimeRangeSelect();
    });

    $(document).on('showRecalculateResultModal', function (event, data)
    {
        if ($(recalculateResultModal).length)
        {
            $(recalculateResultModalContent).html(data.render);

            setTimeout(function ()
            {
                $(recalculateResultModal).modal('show');
            }, 1000);
        }
    });

    function initTimeRangeSelect()
    {
        $(timeSelectInput).timepicker({
            minuteStep: 15,
            showSeconds: false,
            showMeridian: false,
            defaultTime: null
        });
    }


    $(document).on('change', updateTypeRadio, function ()
    {
        if ($(this).val() == 'ALL')
        {
            $('.costPriceUpdateInfo').css('display', 'block');

            $('.costPriceUpdateInfo .text').text('Себестоиомсть товара сохранится и будет использоваться при расчете будущих заказов и отчетов');
            $('.costPriceUpdateInfo .text').removeClass('text-warning text-danger').addClass('text-success');

            $('input[name="Recalculate[saveProduct]"]').val(1);
        }
        else
        {
            let dateTo = $(dateToInput).val();

            if (dateTo)
            {
                let today = new Date().toISOString().slice(0, 10);

                if (new Date(dateTo) >= new Date(today))
                {
                    $('.costPriceUpdateInfo').css('display', 'block');

                    $('.costPriceUpdateInfo .text').text('Себестоиомсть товара сохранится и будет использоваться при расчете будущих заказов и отчетов');
                    $('.costPriceUpdateInfo .text').removeClass('text-warning text-danger').addClass('text-success');

                    $('input[name="Recalculate[saveProduct]"]').val(1);
                }
                else
                {
                    $('.costPriceUpdateInfo').css('display', 'block');

                    $('.costPriceUpdateInfo .text').text('Себестоиомсть будет пересчитана только для заказов и отчетов за выбранный период. Актуальная себестоимость товара не изенится');
                    $('.costPriceUpdateInfo .text').removeClass('text-success text-danger').addClass('text-warning');

                    $('input[name="Recalculate[saveProduct]"]').val(0);
                }
            }
            else
            {
                $('.costPriceUpdateInfo .text').text('Выберите период');
                $('.costPriceUpdateInfo .text').removeClass('text-success text-warning').addClass('text-danger');
            }
        }
    });


    function initDateRangeSelect()
    {
        const picker = new Litepicker({
            element: $(dateRangeInput)[0],
            format: 'DD.MM.YYYY',
            singleMode: false,
            lang: 'ru-RU',
            // position: 'bottom right',
            autoApply: true,
            tooltipText: {"one": "день", "few": "дня", "many": "дней"},
            buttonText: {"apply": "Применить", "cancel": "Отмена", "previousMonth": "<i class='flaticon2-left-arrow'></i>", "nextMonth": "<i class='flaticon2-right-arrow'></i>"},
            plugins: ['mobilefriendly']
        });

        picker.on('selected', (startDate, endDate) =>
        {
            let dateFrom = startDate.format('YYYY-MM-DD');
            let dateTo = endDate.format('YYYY-MM-DD');

            $(updateRangeCheckbox).prop('checked', true);

            // Set time
            $(timeSelectFrom).timepicker('setTime', '00:00');
            $(timeSelectTo).timepicker('setTime', '23:59');

            $(dateFromInput).val(dateFrom);
            $(dateToInput).val(dateTo);

            // Deactivate saveProduct function if end date not equal or less than today
            if ($('.costPriceUpdateInfo .text').length)
            {
                let today = new Date().toISOString().slice(0, 10);

                if (new Date(dateTo) >= new Date(today))
                {
                    $('.costPriceUpdateInfo').css('display', 'block');

                    $('.costPriceUpdateInfo .text').text('Себестоиомсть товара сохранится и будет использоваться при расчете будущих заказов');
                    $('.costPriceUpdateInfo .text').removeClass('text-warning text-danger').addClass('text-success');

                    $('input[name="Recalculate[saveProduct]"]').val(1);
                }
                else
                {
                    $('.costPriceUpdateInfo').css('display', 'block');

                    $('.costPriceUpdateInfo .text').text('Себестоиомсть будет пересчитана только для заказов и отчетов за выбранный период. Актуальная себестоимость товара не изенится');
                    $('.costPriceUpdateInfo .text').removeClass('text-success text-danger').addClass('text-warning');

                    $('input[name="Recalculate[saveProduct]"]').val(0);
                }
            }
        });
    }
});