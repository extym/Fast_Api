$(document).ready(function () {
    const pjaxContainer = $('input[name="pjaxContainerId"]').val();

    // Wizard elements
    const stepsContent = '.stepContent';
    const stepsList = '.wizard-step';

    // Modal
    const modal = '#modal_createAccountWizard';
    const form = '#createAccountWizard';

    const stepInput = 'input[name="step"]';
    const accountIdInput = 'select[name="accountId"]';

    // Steps content
    const step1 = modal + ' #step1content';
    const step2 = modal + ' #step2content';
    const step3 = modal + ' #step3content';
    const step4 = modal + ' #step4content';

    const errorsContainer = '.errorsWrapper';

    // Wizard's navigation buttons
    let prevButton = modal + ' #prev-step';
    let nextButton = modal + ' #next-step';
    let closeButton = modal + ' #close';
    let submitButton = modal + ' #submitWizard';


    // Initialize objects
    let wizardForm = initWizard();

    // Autofocus on modal shown
    $(document).on('shown.bs.modal', modal, function () {
        setTimeout(function () {
            $('input[name="Account[name]"]').focus();
        }, 150);
    });

    // Restore wizard after close
    $(document).on('hidden.bs.modal', modal, function () {
        // Remove finish classes
        $(submitButton).find('.spinner').addClass('d-none');
        $(stepsContent).removeClass('opacity-50');
        $(stepsList).removeClass('opacity-50');

        // Activate all buttons, hide close button
        $(submitButton).removeAttr('disabled');
        $(submitButton).removeClass('d-none');
        $(closeButton).addClass('d-none');

        // Clear previous errors
        $(errorsContainer).empty();

        // Go to the first step
        wizardForm.goTo(1);
    });


    // Custom navigation handlers
    $(document).on('click', prevButton, function () {
        wizardForm.goPrev();
    });

    $(document).on('click', nextButton, function () {
        let currentStep = wizardForm.getStep();
        $(stepInput).val(currentStep);

        // Get form data
        let formData = $(form).serializeArray();

        // Send Ajax request
        $.ajax({
            type: "POST",
            url: "/dashboard/keys/create-wizard",
            dataType: "json",
            cache: false,
            data: formData,
            success: function (response) {
                if (response.success) {
                    let nextStepName = eval('step' + (currentStep + 1));

                    // Render the next step
                    $(nextStepName).html(response['data']['nextStepRender']);

                    // Go to the next step
                    wizardForm.goNext();
                    $(errorsContainer).empty();

                    // Focus on the first input
                    setTimeout(function () {
                        let firstInput = $(nextStepName).find('input').get(0);

                        if (firstInput.length !== 0) {
                            firstInput.focus();
                        }
                    }, 150);
                } else {
                    if (response.hasOwnProperty('error')) {
                        // Clear previous errors
                        $(errorsContainer).empty();

                        if (typeof response.error === 'object') {
                            $.each(response.error, function (key, val) {
                                $(errorsContainer).append('<p class="text-danger mb-2">' + val + '</p>');
                            });
                        } else {
                            $(errorsContainer).html('<p class="text-danger">' + response.error + '</p>');
                        }
                    }
                }
            },
            error: function (response) {
                toastr.error('ошибка сервера', 'Ошибка');
            }
        });
    });

    // Form submit
    $(document).on('submit', form, function (e) {
        e.preventDefault();

        if (wizardForm.isLastStep()) {
            $(stepInput).val(wizardForm.getStep());

            let formData = $(form).serializeArray();

            // Disable buttons
            $(nextButton).prop('disabled', true);
            $(prevButton).prop('disabled', true);
            $(submitButton).prop('disabled', true);

            // Add spinner to finish button
            $(submitButton).find('.spinner').removeClass('d-none');

            // Opacity wizard elements
            $(stepsContent).addClass('opacity-50');
            $(stepsList).addClass('opacity-50');

            // Send Ajax request
            $.ajax({
                type: "POST",
                url: '/dashboard/keys/create-wizard',
                dataType: "json",
                cache: false,
                data: formData,
                success: function (response) {
                    if (response.success) {
                        $(modal).modal('hide');

                        // Refresh table
                        toastr.success('Аккаунт добавлен', 'Успешно');
                        $.pjax.reload({container: pjaxContainer, type: 'POST'});

                        $.event.trigger('keyCreated');
                    } else {
                        if (response.hasOwnProperty('error')) {
                            // Clear previous errors
                            $(errorsContainer).empty();

                            if (typeof response.error === 'object') {
                                $.each(response.error, function (key, val) {
                                    $(errorsContainer).append('<p class="text-danger mb-2">' + val + '</p>');
                                });
                            } else {
                                $(errorsContainer).html('<p class="text-danger">' + response.error + '</p>');
                            }

                            // Reset submit button
                            $(submitButton).find('.spinner').addClass('d-none');

                            // Activate all buttons, hide close button
                            $(submitButton).find('.spinner').addClass('d-none');
                            $(stepsContent).removeClass('opacity-50');
                            $(stepsList).removeClass('opacity-50');

                            $(nextButton).prop('disabled', false);
                            $(prevButton).prop('disabled', false);
                            $(submitButton).prop('disabled', false);
                        }
                    }
                },
                error: function (response) {
                    toastr.error('ошибка сервера', 'Ошибка');

                    // Reset submit button
                    $(submitButton).find('.spinner').addClass('d-none');

                    // Activate all buttons, hide close button
                    $(submitButton).find('.spinner').addClass('d-none');
                    $(stepsContent).removeClass('opacity-50');
                    $(stepsList).removeClass('opacity-50');

                    $(nextButton).prop('disabled', false);
                    $(prevButton).prop('disabled', false);
                    $(submitButton).prop('disabled', false);
                }
            });
        } else {
           $(nextButton).trigger('click');
        }
    });

    $(document).on('click', submitButton, function () {
        $(form).submit();
    });

    // --------------------------------------------------------------------------------------------

    function initWizard() {
        var wizardEl = document.querySelector('#processFileWizard');

        // Initialize wizard object
        return new KTWizard(wizardEl, {
            startStep: 1,
            clickableSteps: false,
            navigation: false
        });
    }
});
