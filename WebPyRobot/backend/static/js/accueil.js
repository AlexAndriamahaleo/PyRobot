function searchPlayerChamp() {
    var input, filter, table, li, div, i;
    input = document.getElementById("PlayerChamp");
    filter = input.value.toUpperCase();
    table = document.getElementById("resultPlayerChamp");
    li = table.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        div = li[i].getElementsByTagName("div")[0];
        //console.log(div);
        if (div) {
            if (div.innerHTML.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }
}

function searchPlayerVersus() {
    var input, filter, table, li, div, i;
    input = document.getElementById("modeVersus");
    filter = input.value.toUpperCase();
    table = document.getElementById("resultPlayerVersus");
    li = table.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        div = li[i].getElementsByTagName("div")[0];
        if (div) {
            if (div.innerHTML.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }
}