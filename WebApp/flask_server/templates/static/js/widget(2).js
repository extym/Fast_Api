$(document).ready(function () {
    // Static variables
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();
    const filterFormSelector = $('input[name="switchTaxType_filterFormSelector"]').val();
    const inputName = $('input[name="switchTaxType_inputName"]').val();

    const widget = '#taxTypeSwitchWidget';
    const switchTaxType = widget + ' input[name="switchTaxType"]';
    const taxTypeName = widget + ' .name';

    $(document).on('change', switchTaxType, function () {
        $(taxTypeName).removeClass('active');

        if ($(this).is(':checked')) {
            $(taxTypeName + '[data-tax-type=2]').addClass('active');
            $('input[name="' + inputName +'"]').val(2);
        } else {
            $(taxTypeName + '[data-tax-type=1]').addClass('active');
            $('input[name="' + inputName +'"]').val(1);
        }

        $('#filtersForm').submit();
    });
});