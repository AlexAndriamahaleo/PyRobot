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
            extraKeys: {"Ctrl-Space": "autocomplete", "Option-Space": "autocomplete"},
            globalVars: true
        });

        $(".save").click(function (e) {
            $("#code").submit();
        });

        $("#code").submit(function () {
            editor.save();
        });

        $(".script-1").click(function (e) {
            console.log("script-1");
            $("#code").submit();
        });

        $(".script-2").click(function (e) {
            console.log("script-2")
        });

        $(".script-3").click(function (e) {
            console.log("script-3")
        });

    });
})(jQuery);
