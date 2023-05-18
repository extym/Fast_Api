$(document).ready(function () {
    const apiKeyCheckBox = '.js-toggle-api-key';
    const apiKeyBlock = '.api-key-for-update';

    const statApiKeyCheckBox = '.js-toggle-stat-api-key';
    const statApiKeyBlock = '.stat-api-key-for-update';

    $(document).on('change', apiKeyCheckBox, function () {
        toggleBlock(apiKeyCheckBox, apiKeyBlock);
    });

    $(document).on('change', statApiKeyCheckBox, function () {
        toggleBlock(statApiKeyCheckBox, statApiKeyBlock);
    });

    const toggleBlock = function (checkbox, targetBlock) {
        $(targetBlock).toggleClass('d-none');

        if (!$(checkbox).is(':checked')) {
            $(targetBlock).find('input').val('');
        }
    };
});
