$(document).ready(function ()
{
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const modal = '#modal_filters';
    const filtersForm = '#filtersForm';

    // Date range filter
    const customDateRangeModal_input = 'input[name="customDateRange_modal"]';
    const dateRangeName_input = 'input[name="WildberriesOrderSearch[dateRangeName]"]';
    const dateRangeFrom_input = 'input[name="WildberriesOrderSearch[dateRangeFrom]"]';
    const dateRangeTo_input = 'input[name="WildberriesOrderSearch[dateRangeTo]"]';

    // Price range filter
    const priceRangeSlider = '#priceRangeSlider';
    const priceRangeMin_input = 'input[name="priceRangeMin"]';
    const priceRangeMax_input = 'input[name="priceRangeMax"]';
    let priceFrom_input = 'input[name="WildberriesOrderSearch[priceFrom]"]';
    let priceTo_input = 'input[name="WildberriesOrderSearch[priceTo]"]';

    // Accounts filter
    const selectAccounts_dropdown = '#selectAccounts';
    const selectAccounts_input = 'input[name="WildberriesOrderSearch[accountIds]"]';

    // Grouping select
    const selectGrouping_dropdown = '#selectGrouping';
    const forceGroup_input = 'input[name="WildberriesOrderSearch[forceGrouping]"]';

    // Base variables
    const applyModalFilters = '#applyModalFilters';


    // Reload plugins after pjax-call
    $(document).on('pjax:end', function ()
    {
        initDateRangeSelect();
    });

    // Init plugins
    initDateRangeSelect();


    // Account select
    $(document).on("changed.bs.select", selectAccounts_dropdown, function (e, clickedIndex, newValue, oldValue)
    {
        $(selectAccounts_input).val(JSON.stringify($(this).val()));
    });

    // Grouping select
    $(document).on("changed.bs.select", selectGrouping_dropdown, function (e, clickedIndex, newValue, oldValue)
    {
        $(forceGroup_input).val(1);
    });

    // Apply filters
    $(document).on('click', applyModalFilters, function (event)
    {
        $(filtersForm).submit();
    });

    // Form submit
    $(document).on('submit', filtersForm, function (e) {
        e.preventDefault();

        $(modal).modal('hide');

        // Timeout for preventing gray screen
        setTimeout(function () {
            $.pjax.reload({
                type: 'POST',
                url: window.location.href,
                container: pjaxContainerId,
                data: $('#quickSearchWidgetForm, #filtersForm').serialize(),
                timeout: 10000
            });
        }, 100);
    });

    function initDateRangeSelect()
    {
        const picker = new Litepicker({
            element: document.getElementById('customDateRangeFilter'),
            format: 'DD.MM.YYYY',
            startDate: $(dateRangeFrom_input).val(),
            endDate: $(dateRangeTo_input).val(),
            singleMode: false,
            lang: 'ru-RU',
            position: 'bottom right',
            autoApply: true,
            tooltipText: {"one":"день","few":"дня", "many": "дней"},
            buttonText: {"apply":"Применить","cancel":"Отмена","previousMonth":"<i class='flaticon2-left-arrow'></i>","nextMonth":"<i class='flaticon2-right-arrow'></i>"},
            plugins: ['mobilefriendly']
        });

        picker.on('selected', (startDate, endDate) => {
            let dateFrom = startDate.format('YYYY-MM-DD');
            let dateTo = endDate.format('YYYY-MM-DD');

            $(dateRangeName_input).val('custom');
            $(dateRangeFrom_input).val(dateFrom);
            $(dateRangeTo_input).val(dateTo);
        });
    }
});