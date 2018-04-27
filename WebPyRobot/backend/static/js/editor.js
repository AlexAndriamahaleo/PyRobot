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

        $("#entrer").click(function (e) {
            var file = document.getElementById('myfile');

            //console.log(file.files[0].name);

            if(file.files.length)
            {
                var reader = new FileReader();
                reader.onload = function(e)
                {
                    document.getElementById('code_name').setAttribute('value',file.files[0].name);
                    editor.getDoc().setValue(e.target.result);
                };

                reader.readAsBinaryString(file.files[0]);
            }
        });

        $("#code").submit(function () {
            editor.save();
        });

    });
})(jQuery);