$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const widgetWrapper = '#quickSearchWidget';
    const form = widgetWrapper + ' #quickSearchWidgetForm';
    const input = widgetWrapper + ' #quickSearchInput';
    const additionalForms = widgetWrapper + ' #quickSearchWidgetAdditionalForms';

    let typingTimer;
    let doneTypingInterval = 1500;

    // Prevent form submit then press enter and timer is triggered
    let allowSubmit = false;


    // Start/reset timer then typing
    $(document).on('keyup', input, function (e) {
        clearTimeout(typingTimer);

        if (e.which !== 13) {
            if ($(input).val()) {
                allowSubmit = true;
                typingTimer = setTimeout(doneTyping, doneTypingInterval);
            }
        }
    });

    // Submit quick search
    $(document).on('submit', form, function (e) {
        e.preventDefault();

        let additionalFormsList = $(additionalForms).val();
        let formsToSerialize = '#quickSearchWidgetForm';

        if (additionalFormsList) {
            formsToSerialize += ', ' + additionalFormsList;
        }

        $.pjax.reload({
            type: 'POST',
            url: window.location.href,
            container: pjaxContainerId,
            data: $(formsToSerialize).serialize(),
            timeout: 10000
        });

        allowSubmit = false;
    });

    // Move cursor at the end of input after pjax loaded
    $(document).on('pjax:end', function () {
        // moveCursorToEnd(input);
    });

    function doneTyping() {
        if (allowSubmit) {
            $(form).submit();
        }
    }

});