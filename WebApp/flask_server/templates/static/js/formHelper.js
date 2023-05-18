// Focus on the input and move cursor at the end
function moveCursorToEnd(inputSelector) {
    setTimeout(function(){
        const input = $(inputSelector)[0];
        input.selectionStart = input.selectionEnd = input.value.length;
        input.focus();
    }, 0)
}