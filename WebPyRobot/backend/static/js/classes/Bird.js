
function Bird(url, x1, y1, direction, x2, y2,contraint) {

    this.x = x1; // (en cases)
    this.y = y1; // (en cases)

    this.x2 = x2;
    this.y2 = y2;

    this.x1 = x1;
    this.y1 = y1;

    this.direction = direction;
    this.stateAnimation = 1;
    
    // Chargement de l'image dans l'attribut image
    this.image = new Image();
    this.image.refPlayer = this;
    this.image.onload = function() {
        if(!this.complete) 
            throw "Erreur de chargement du sprite nommé \"" + url + "\".";
        
        // Taille du personnage
        this.refPlayer.width = this.width / 6;
        this.refPlayer.height = this.height / 4;
    }
    this.image.src = "../static/sprites/" + url;
    this.contraint = contraint;
}

Bird.prototype.drawBird = function(context) {
    var frame = 0; // Numéro de l'image à prendre pour l'animation
    var shiftX = 0, shiftY = 0; // Décalage à appliquer à la position du personnage
    if(Math.abs(this.x1 + (this.x*32/this.contraint) - (this.x2*32/this.contraint )) <= this.contraint && Math.abs(this.y1+(this.y*32/this.contraint) - (this.y2*32/this.contraint)) <= this.contraint) {//&& Math.abs(this.y -this.y2*32*this.contraint) <= 0.1 ) {
        // Si le déplacement a atteint ou dépassé le temps nécéssaire pour s'effectuer, on le termine
        this.stateAnimation = -1;
        return false;
    }
    if(this.stateAnimation >= 0) {

        frame = this.stateAnimation; 
        if(frame > 6) {
            frame %= 6;
        }

        shiftX = ((this.x2 - this.x) * (this.stateAnimation / 5)) ;
        shiftY = ((this.y2 - this.y) * (this.stateAnimation / 5));


        // On incrémente d'une frame
        this.stateAnimation++;
        
        this.x1 = 0 + shiftX;
        this.y1 = 0 + shiftY ;
    } 

    context.drawImage(
        this.image, 
            this.width * frame, this.direction * this.height, // Point d'origine du rectangle source à prendre dans notre image
            this.width, this.height, // Taille du rectangle source (c'est la taille du personnage)
            (this.x * 32/this.contraint) - (this.width /7/this.contraint ) + shiftX, (this.y * 32/this.contraint) - this.height/7/this.contraint + shiftY,
            this.width/this.contraint*2, this.height/this.contraint*2 
    );

    return true;

}