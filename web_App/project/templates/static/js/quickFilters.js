$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const filtersForm = $('input[name="filtersFormSelector"]').val();
    const searchModelName = $('input[name="searchModelName"]').val();

    // Toolbar filters ----------------------------------------------------------------------------
    const quickDateFilterItems = '#dateRangeList .item';
    const customDateRangeToolbar_input = 'input[name="customDateRange_toolbar"]';
    const quickDateFilterItems_m = '#dateRangeList_mobile .dropdown-item';
    // End toolbar filters ------------------------------------------------------------------------

    const dateRangeName_input = filtersForm + ' input[name="' + searchModelName + '[dateRangeName]"]';
    const dateRangeFrom_input = filtersForm + ' input[name="' + searchModelName + '[dateRangeFrom]"]';
    const dateRangeTo_input = filtersForm + ' input[name="' + searchModelName + '[dateRangeTo]"]';

    // Force grouping
    const forceGrouping_input = 'input[name="' + searchModelName + '[forceGrouping]"]';

    // Reload plugins after pjax-call
    $(document).ajaxComplete(function () {
        initDateRangeSelect();
    });

    // Init plugins
    initDateRangeSelect();

    $(document).on('click', quickDateFilterItems + ', ' + quickDateFilterItems_m, function (event) {
        let dateRangeName = $(this).data('name');

        // Set ActiveForm values
        $(dateRangeName_input).val(dateRangeName);
        $(forceGrouping_input).val(0);

        // Submit the form
        $.pjax.reload({
            type: 'POST',
            url: window.location.href,
            container: pjaxContainerId,
            data: $('#quickSearchWidgetForm, #filtersForm').serialize(),
            timeout: 10000
        });
    });

    function initDateRangeSelect() {
        const picker = new Litepicker({
            element: document.getElementById('toolbarCustomDate'),
            format: 'DD.MM.YYYY',
            startDate: $(dateRangeFrom_input).val(),
            endDate: $(dateRangeTo_input).val(),
            singleMode: false,
            lang: 'ru-RU',
            position: 'bottom right',
            autoApply: false,
            tooltipText: {"one": "день", "few": "дня", "many": "дней"},
            buttonText: {
                "apply": "Применить",
                "cancel": "Отмена",
                "previousMonth": "<i class='flaticon2-left-arrow'></i>",
                "nextMonth": "<i class='flaticon2-right-arrow'></i>"
            },
            plugins: ['mobilefriendly']
        });

        picker.on('button:apply', (startDate, endDate) => {
            let dateFrom = startDate.format('YYYY-MM-DD');
            let dateTo = endDate.format('YYYY-MM-DD');

            $(dateRangeName_input).val('custom');
            $(dateRangeFrom_input).val(dateFrom);
            $(dateRangeTo_input).val(dateTo);

            $.pjax.reload({
                type: 'POST',
                url: window.location.href,
                container: pjaxContainerId,
                data: $('#quickSearchWidgetForm, #filtersForm').serialize(),
                timeout: 10000
            });
        });
    }
});