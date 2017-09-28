$(document).ready(function(){
    $(".card").hide()
    $("#cardweapon1").show()
    $(".openCard").click(function () {
        $(".card").hide()
        $("#card"+this.id).show()
    })
});