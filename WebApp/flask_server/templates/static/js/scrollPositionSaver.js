$(document).ready(function ()
{
    let scrollPos = 0;

    $(document).on("mousewheel", function() {
        scrollPos = $(document).scrollTop();
    });

    $(document).on('ajaxComplete', function (event, request, settings) {
        $(document).scrollTop(scrollPos);
    });
});