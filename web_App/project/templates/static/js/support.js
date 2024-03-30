$(document).ready(function () {
    const copyBtn = '#copyUserId';

    $(document).on('click', copyBtn, function () {
        let value = $(this).data('value');

        // Copy the text inside the text field
        navigator.clipboard.writeText("ID аккаунта: " + value);
        toastr.success('Скопировано');
    });

    $(document).on('click', '.openSupportModal', function () {
        $('.modal').modal('hide');

        setTimeout(function () {
            $('#modal_support').modal('show');
        }, 300);
    });
});