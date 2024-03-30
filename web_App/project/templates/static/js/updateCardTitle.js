$(document).ready(function () {
    const pjaxContainerId = $('input[name="pjaxContainerId"]').val();

    const updateButton_selector = '.updateCardTitle';
    const saveButton_selector = '.saveCardTitle';
    const wrapper_selector = '.product_cardTitle_wrapper';
    const value_selector = '.value';

    const inputWrapper_selector = '<div class="input-group"><input type="text" class="form-control form-control-sm" placeholder="Введите наименование товара"><div class="input-group-append"><button class="btn btn-sm btn-icon btn-primary saveCardTitle" type="button"><i class="fas fa-check icon-nm"></i></button></div></div>';
    const input_selector = 'input';


    $(document).on('click', updateButton_selector, function () {
        let button = $(this);
        let wrapper = button.closest(wrapper_selector);
        let text = wrapper.find(value_selector);

        let inputWrapper = $(inputWrapper_selector);
        let input = inputWrapper.find(input_selector);
        let saveBtn = inputWrapper.find(saveButton_selector);

        let value = button.data('value');
        let wbId = button.data('wbid');


        button.hide();
        text.hide();
        wrapper.append(inputWrapper);

        // Show/hide input
        input.val(value).show().focus();


        // Click outside the element
        $(document).on('click', function (event) {
            if ($(event.target).closest(wrapper).length === 0) {
                wrapper.trigger('hideWithoutSave');
            }
        });

        // Press Esc
        $(document).on('keypress', function (e) {
            if (e.which === 27) {
                wrapper.trigger('hideWithoutSave');
            }
        });

        // Press Enter
        $(document).on('keypress', function (e) {
            if (e.which === 13) {
                wrapper.trigger('hideAndSave');
            }
        });

        saveBtn.on('click', function (e) {
            wrapper.trigger('hideAndSave');
        });


        // Close input without save
        wrapper.on('hideWithoutSave', function () {
            inputWrapper.hide();
            button.show();
            text.show();
        });

        // Close input without save
        wrapper.on('hideAndSave', function () {
            let cardTitle = $(input).val();

            if (!$.isEmptyObject(cardTitle)) {
                $.post("/dashboard/product/update-card-title", {wbId: wbId, cardTitle: cardTitle})
                    .done(function (data) {
                        if (data.success) {
                            text.html(cardTitle);
                            button.data('value', cardTitle);
                        }
                        else {
                            toastr.error(data.error, 'Ошибка');
                        }
                    })
                    .fail(function (xhr, status, error) {
                        toastr.error('Ошибка сервера', 'Ошибка');
                    });

                inputWrapper.remove();
                button.show();
                text.show();
            }
        });
    });
});