(function ($) {
    $(function () {
        var editor = CodeMirror.fromTextArea(document.getElementById('ia'), {
            mode: 'python',
            theme: 'cobalt',
            autoCloseBrackets: true,
            indentUnit: 4,
            lineNumbers: true,
            fixedGutter: true,
            matchBrackets: true,
            dragDrop: true,
            allowDropFileTypes : ["text/x-python","text/plain"],
            extraKeys: {"Ctrl-Space": "autocomplete"},
            globalVars: true
        });
        $(".save").click(function (e) {
            $("#code").submit();
        });
        $("#code").submit(function () {
            editor.save();
        });
    });
})(jQuery);
