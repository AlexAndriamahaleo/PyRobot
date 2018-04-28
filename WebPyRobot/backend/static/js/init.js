(function ($) {
    $(function () {

        $(document).ready(function () {
            $('.collapsible').collapsible();

            $('#alert_close').click(function () {
                $("#alert_box").fadeOut("slow", function () {
                });
            });

            $('.button-collapse').sideNav({
                menuWidth: 350,
                closeOnClick: true,
                draggable: true
            });

            $('.carousel').carousel();

            $('.scrollspy').scrollSpy();

            $('.carousel.carousel-slider').carousel();

            $('.modal').modal();

            $('.parallax').parallax();

            $('.materialboxed').materialbox();

            $('.toc-wrapper').pushpin({
                offset: 100
            });

            $('select').material_select();

            $('.chips').material_chip();

            $('ul.tabs').tabs();

            $('i.championship').click(function(event) {
                var modal1 = document.getElementById('modalconfirmation');
                var modal = document.getElementById('modalconfirmation2');
                modal.setAttribute('value', event.target.id);

                modal1.innerHTML = "Vous êtes sur le point de changer de championnat. \n";
                modal1.innerHTML += "Vous allez rejoindre le championnat " ;
                modal1.innerHTML += event.target.id ;
                modal1.innerHTML += ". Voulez-vous continuer ?" ;
                //console.log(event.target.id);
            });

        });


    }); // end of document ready
})(jQuery); // end of jQuery name space