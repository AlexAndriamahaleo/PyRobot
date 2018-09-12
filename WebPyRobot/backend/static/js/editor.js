(function ($) {
    $(function () {
        var editor = CodeMirror.fromTextArea(document.getElementById('ia'), {
            mode: 'python',
            theme: 'dracula',
            keyMap: 'sublime',
            autoCloseBrackets: true,
            lineWrapping: true,
            foldGutter: true,
            gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
            indentWithTabs: false,
            indentUnit: 4,
            smartindent: true,
            lineNumbers: true,
            fixedGutter: true,
            matchBrackets: true,
            dragDrop: true,
            allowDropFileTypes: ["text/x-python", "text/plain"],
            //extraKeys: {"Ctrl-Space": "autocomplete", "Option-Space": "autocomplete"},
            globalVars: true
        });

        var request = new XMLHttpRequest();
        request.open("GET", "/static/tern/pyrobot.json", false);
        request.send(null);
        server = new CodeMirror.TernServer({defs: [JSON.parse(request.responseText)]});
        editor.setOption("extraKeys", {
            "Ctrl-Space": function (cm) {
                server.complete(cm);
            },
            "Ctrl-I": function (cm) {
                server.showType(cm);
            },
            "Ctrl-O": function (cm) {
                server.showDocs(cm);
            },
            "Alt-.": function (cm) {
                server.jumpToDef(cm);
            },
            "Alt-,": function (cm) {
                server.jumpBack(cm);
            },
            "Ctrl-Q": function (cm) {
                server.rename(cm);
            },
            "Ctrl-.": function (cm) {
                server.selectName(cm);
            }
        });

        editor.on("cursorActivity", function (cm) {
            server.updateArgHints(cm);
        });

        editor.on("keypress", function (cm) {
            //server.complete(cm);
            server.updateArgHints(cm);
        });

        $(".save").click(function (e) {
            $("#code").submit();
        });

        $("#entrer").click(function (e) {
            var file = document.getElementById('myfile');

            if (file.files.length) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    document.getElementById('code_name').setAttribute('value', file.files[0].name);
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