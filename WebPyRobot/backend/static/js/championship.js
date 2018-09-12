function searchChamp() {
    var input, filter, table, li, p, i;
    input = document.getElementById("searchChamp_id");
    filter = input.value.toUpperCase();
    table = document.getElementById("resultChamp");
    li = table.getElementsByTagName("li");
    for (i = 0; i < li.length; i++) {
        p = li[i].getElementsByTagName("p")[0];
        if (p) {
            if (p.innerHTML.toUpperCase().indexOf(filter) > -1) {
                li[i].style.display = "";
            } else {
                li[i].style.display = "none";
            }
        }
    }
}

var championship_new_name = document.getElementById("id_name");
championship_new_name.setAttribute('data-length', '60');

var championship_pass = document.getElementById("id_secret_pass");
championship_pass.setAttribute('data-length', '60');

function displayPrivateChamp() {
    div_champ = document.getElementById("private_champ");
    console.log(div_champ.innerHTML);
    if (div_champ.style.visibility === 'hidden') {
        div_champ.style.visibility = '';
    } else {
        div_champ.style.visibility = 'hidden';
    }
}