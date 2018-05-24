(function ($) {
    $(function () {

        $(document).ready(function () {
            $('.collapsible').collapsible();

            $('input#input_text, textarea#textarea1').characterCounter();

            $('#alert_close').click(function () {
                $("#alert_box").fadeOut("slow", function () {
                });
            });

            $('.button-collapse').sideNav({
                menuWidth: 250,
                closeOnClick: true,
                draggable: true
            });


            $('.dropdown-button').dropdown({
                    inDuration: 300,
                    outDuration: 225,
                    constrainWidth: false, // Does not change width of dropdown to that of the activator
                    hover: true, // Activate on hover
                    gutter: 0, // Spacing from edge
                    belowOrigin: true, // Displays dropdown below the button
                    alignment: 'left', // Displays dropdown with edge aligned to the left of button
                    stopPropagation: false // Stops event propagation
                }
            );


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
                console.log(event.target.attributes.getNamedItem('data-mode').value);
                var champ_mode = event.target.attributes.getNamedItem('data-mode').value;

                var name_championship = document.getElementById('name_championship');
                name_championship.setAttribute('value', event.target.id);

                var modal1 = document.getElementById('modalconfirmation');

                var button_yes = document.getElementById('confirm_champ');
                var button_no = document.getElementById('not_confirm_champ');
                var input_secret = document.getElementById('secret');

                if(champ_mode == 'False'){
                    input_secret.style.visibility = 'hidden';
                    modal1.innerHTML = "Vous êtes sur le point de changer de championnat. <br/>";
                    modal1.innerHTML += "<br/>Vous allez rejoindre le championnat " ;
                    modal1.innerHTML += event.target.id ;
                    modal1.innerHTML += ". <br/><br/>Voulez-vous continuer ?" ;
                }
                else {
                    input_secret.style.visibility = '';
                    modal1.innerHTML = "Vous êtes sur le point de changer de championnat. <br/>";
                    modal1.innerHTML += "Vous allez rejoindre le championnat " ;
                    modal1.innerHTML += event.target.id ;
                    modal1.innerHTML += ". <br/>Veuillez entrer le code secret" ;
                    button_yes.value = 'Continuer';
                    button_no.innerHTML = 'Retour'
                }



                //console.log(event.target.id);
            });

            $('.finish').click(function () {
                if (is_replay != "yes") {
                    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
                    var socket = new WebSocket(ws_scheme + '://' + window.location.host + "/" + opponent + "-notifications/");
                    socket.onopen = function () {
                        var message = {
                            msg_content: "Le combat contre " + playername + " est terminé",
                            msg_type: "notification",
                            msg_class: "success",
                            is_versus: is_versus
                        };
                        socket.send(JSON.stringify(message));
                    };
                    if (socket.readyState == WebSocket.OPEN) socket.onopen();
                }
            });

        });


    }); // end of document ready
})(jQuery); // end of jQuery name space