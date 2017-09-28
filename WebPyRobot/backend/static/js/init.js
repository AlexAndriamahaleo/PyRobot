(function($){
  $(function(){

    $('.button-collapse').sideNav();
	$('.carousel').carousel();
	$('.modal-trigger').leanModal();
	$('.scrollspy').scrollSpy();

	$('.toc-wrapper').pushpin({
		offset: 100
		});


  }); // end of document ready
})(jQuery); // end of jQuery name space