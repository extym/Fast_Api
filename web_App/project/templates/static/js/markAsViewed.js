$(document).ready(function () {
    const button = '#kt_quick_panel_toggle';
    const unseenNotification = '#unseenNotificationCount';

    $(document).on('click', button, function (e) {
        $.post('/dashboard/notification/mark-as-viewed', {}, function (data) {
           $(unseenNotification).remove();
        });
    });
});