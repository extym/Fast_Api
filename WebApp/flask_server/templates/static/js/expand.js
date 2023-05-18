$(document).ready(function ()
{
    const searchModelName = $('input[name="searchModelName"]').val();
    const tableSelector = $('input[name="tableSelector"]').val();
    const filtersForm = $('input[name="filtersFormSelector"]').val();

    const expandBtn = tableSelector + ' .expandInfo';
    const groupingInput = 'select[name="' + searchModelName + '[grouping]"]';
    const forceGroupingInput = 'input[name="' + searchModelName + '[forceGrouping]"]';
    const dateRangeName_input = 'input[name="' + searchModelName + '[dateRangeName]"]';
    const dateRangeFromInput = 'input[name="' + searchModelName + '[dateRangeFrom]"]';
    const dateRangeToInput = 'input[name="' + searchModelName + '[dateRangeTo]"]';
    const wbIdInput = 'input[name="' + searchModelName + '[wbId]"]';

    const grouping = ['without', 'day', 'week', 'month', 'year', 'all'];


    $(document).on('click', expandBtn, function (e)
    {
        let rowData = $(this).closest('tr');
        let currentGrouping = $(groupingInput).val();

        if (grouping.includes(currentGrouping))
        {
            if (currentGrouping !== 'without')
            {
                let wbId = rowData.data('wb-id');
                let dateFrom = rowData.data('date-from');
                let dateTo = rowData.data('date-to');

                if (wbId != null && dateFrom != null && dateTo != null)
                {
                    $(dateRangeName_input).val('custom');

                    $(groupingInput).val(grouping[grouping.indexOf(currentGrouping) - 1]);
                    $(forceGroupingInput).val(1);

                    $(wbIdInput).val(wbId);
                    $(dateRangeFromInput).val(dateFrom);
                    $(dateRangeToInput).val(dateTo);

                    $(filtersForm).yiiActiveForm('submitForm');
                }
            }
        }
    });
});