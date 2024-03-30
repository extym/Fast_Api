$(document).on('pjax:beforeSend', function () {
    KTApp.block('.pjax-block', {message: "Обработка..."});
});

$(document).on('pjax:end', function () {
    KTApp.unblock('.pjax-block');
});