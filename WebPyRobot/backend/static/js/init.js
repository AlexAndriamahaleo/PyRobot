(function ($) {
    $(function () {

        $('.button-collapse').sideNav();

        $('.carousel').carousel();

        $('.carousel.carousel-slider').carousel();

        $(document).ready(function () {
            $('.modal').modal();
        });

        $('.scrollspy').scrollSpy();

        $(document).ready(function () {
            $('.parallax').parallax();
        });
        $(document).ready(function () {
            $('.materialboxed').materialbox();
        });
        $('.toc-wrapper').pushpin({
            offset: 100
        });


        $(document).ready(function () {
            $('.collapsible').collapsible();
            $('#alert_close').click(function(){
                $( "#alert_box" ).fadeOut( "slow", function() {
                });
              });
        });

        $(document).ready(function () {
            $('.carousel').carousel();
        });


    }); // end of document ready
})(jQuery); // end of jQuery name space