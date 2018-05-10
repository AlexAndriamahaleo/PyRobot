var myErrors =
            "\nVotre mot de passe ne peut pas être trop similaire à vos autres informations personnelles.\n" +
            "Votre mot de passe doit contenir au moins 8 caractères.\n" +
            "Votre mot de passe ne peut pas être un mot de passe couramment utilisé.\n" +
            "Votre mot de passe ne peut pas être entièrement numérique.\n\n";
var helptext = document.getElementsByClassName("helptext");
helptext[0].innerText = myErrors;

var myLabels = [
    "Nouveau mot de passe",
    "Nouveau mot de passe (confirmation)"
];
var labels = document.getElementsByTagName('LABEL');
for (var i = 0; i < labels.length; i++) {
    labels[i].innerHTML = myLabels[i];
}

var myObjectErrors = {
    'similar' : 'Votre mot de passe est trop similaire à une de vos infos personnelles',
    'common' : 'Votre mot de passe est trop commun.\n',
    'numeric' : 'Votre mot de passe est entièrement numérique.\n',
    'short' : "Votre mot de passe est trop court. Il doit contenir au moins 8 caractères.\n",
    'match' : "Les mots de passe ne correspondent pas.\n"
};

var errors = document.getElementsByClassName("errorlist");

if(errors){
    for(err in myObjectErrors){
        if(errors[0].textContent.includes(err)){
            errors[0].textContent = "";
            errors[0].textContent += myObjectErrors[err] + '\n';
        }
    }
}