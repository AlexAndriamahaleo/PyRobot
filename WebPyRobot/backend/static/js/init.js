(function ($) {
    $(function () {

        $('.button-collapse').sideNav();

        $('.carousel').carousel();

        $('.carousel.carousel-slider').carousel();
        //$('.modal-trigger').leanModal();
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
        });

        $(document).ready(function () {
            $('.carousel').carousel();
        });


    }); // end of document ready
})(jQuery); // end of jQuery name space