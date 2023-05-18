$(document).ready(function ()
{
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();
    const button = '#refreshPjax';

    if (pjaxContainerId)
    {
        $(document).on('click', button, function () {
            $.pjax.reload({container: pjaxContainerId, type: 'POST'});
        });
    }
});