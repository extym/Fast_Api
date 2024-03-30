$(document).ready(function ()
{
    $('body').tooltip({selector: '[data-toggle="tooltip"]'});

    $(document).ajaxComplete(function() {
        $('body').tooltip({selector: '[data-toggle="tooltip"]'});
    });
});