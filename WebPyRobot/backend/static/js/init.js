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

        });


    }); // end of document ready
})(jQuery); // end of jQuery name space