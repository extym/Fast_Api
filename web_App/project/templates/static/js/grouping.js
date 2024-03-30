// Not used since grouping was moved to filter modal

$(document).ready(function ()
{
    const searchModelName = $('input[name="searchModelName"]').val();
    const filtersForm = $('input[name="filtersFormSelector"]').val();

    const dropdown = '#groupingDropdown';
    const items = dropdown + ' .dropdown-item';

    // Input in filters form
    const input = 'input[name="' + searchModelName + '[grouping]"]';
    const forceInput = 'input[name="' + searchModelName + '[forceGrouping]"]';


    $(document).on('click', items, function (e)
    {
        let selectedGrouping = $(this).data('value');

        $(input).val(selectedGrouping);
        $(forceInput).val(1);

        $(filtersForm).yiiActiveForm('submitForm');
        e.preventDefault();
    });
});