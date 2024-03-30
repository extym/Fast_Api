$(document).ready(function ()
{
    const priceRangeExactField = '.range-exact';
    const priceRangeBoundField = '.range-bound';

    $(document).on('input', priceRangeExactField, function ()
    {
        let value = $(this).val();
        let boundFields = $(this).closest('.rangeField').find(priceRangeBoundField);

        if (value)
        {
            boundFields.val(null).attr('disabled', true);
        }
        else
        {
            boundFields.attr('disabled', false);
        }
    });
});