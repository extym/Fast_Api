$(document).ready(function () {
    tippy('[data-tippy-content]', {
        // interactive: true,
        theme: 'light'
    });

    $(document).on('ajaxComplete', function (event, request, settings) {
        tippy('[data-tippy-content]', {
            // interactive: true,
            theme: 'light'
        });
    });
});