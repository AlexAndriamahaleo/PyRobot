
var range = function(x,y,x1,y1){
    var xb = x1 - x;
    var yb = y1 - y;
    var xb2 = Math.pow(xb, 2);
    var yb2 = Math.pow(yb, 2);
    var yx2 = xb2 + yb2;
    return Math.sqrt(yx2);
}

function Bullet(url, x1, y1, targetDirection, x2, y2,contraint) {
    this.x = x1; // (en cases)
    this.y = y1; // (en cases)

    this.x2 = x2;
    this.y2 = y2;

    this.x1 = x1;
    this.y1 = y1;
    this.targetDir = targetDirection;
    this.direction = 1;
    // Chargement de l'image dans l'attribut image
    this.image = new Image();
    this.image.refPlayer = this;
    this.image.onload = function() {
        if(!this.complete) 
            throw "Erreur de chargement du sprite nommé \"" + url + "\".";
        // Taille du personnage
        this.refPlayer.width = this.width / 9.1;
        this.refPlayer.height = this.height / 6;
    }
    this.image.src = "../static/sprites/" + url;
    
    this.stateAnimation = 1;
    this.stateTouch = -1;
    this.contraint = contraint;
}

Bullet.prototype.drawBullet = function(context) {
    var frame = 0; // Numéro de l'image à prendre pour l'animation
    var shiftX = 0, shiftY = 0; // Décalage à appliquer à la position du personnage
    
     if (this.stateTouch > 0){
        frame = this.stateTouch;
        if(frame > 8) {
            frame %= 8;
        }
        ++this.stateTouch;

        context.drawImage(
            this.image, 
            this.width * frame, (this.targetDir +2) * this.height, // Point d'origine du rectangle source à prendre dans notre image
            this.width, this.height, // Taille du rectangle source (c'est la taille du personnage)
            // Point de destination (dépend de la taille du personnage)
            (this.x2 * 32/this.contraint) - (this.width /7/this.contraint ) , (this.y2/this.contraint * 32) - this.height/7/this.contraint,
            this.width/1.4/this.contraint, this.height/1.4/this.contraint // Taille du rectangle destination (c'est la taille du personnage)
        );

        if(this.stateTouch > 4)
            return false;


    } 

    else if(Math.abs(this.x1 + (this.x*32/this.contraint) - (this.x2*32/this.contraint )) <= 0.1 && Math.abs(this.y1+(this.y*32/this.contraint) - (this.y2*32/this.contraint)) <= 0.1 ) {
        // Si le déplacement a atteint ou dépassé le temps nécéssaire pour s'effectuer, on le termine
        this.stateAnimation = -1;
        this.direction = 2;
        this.stateTouch = 1;
    } else if(this.stateAnimation >= 0) {

        frame = this.stateAnimation; 

        if(frame > 9) {
            
            frame %= 9;
        }

        shiftX = ((this.x2/this.contraint - this.x/this.contraint) * (this.stateAnimation / 0.5));
        shiftY = ((this.y2/this.contraint - this.y/this.contraint) * (this.stateAnimation / 0.5));


        // On incrémente d'une frame
        this.stateAnimation++;
        context.drawImage(
            this.image, 
            this.width * frame, this.direction * this.height, // Point d'origine du rectangle source à prendre dans notre image
            this.width, this.height, // Taille du rectangle source (c'est la taille du personnage)
            // Point de destination (dépend de la taille du personnage)
            (this.x * 32/this.contraint) - (this.width /7/this.contraint) + shiftX, (this.y * 32/this.contraint) - this.height/7/this.contraint- this.width/2/1.5/this.contraint + shiftY,
            this.width/this.contraint, this.height/this.contraint // Taille du rectangle destination (c'est la taille du personnage)
        );
        
        this.x1 = 0 + shiftX;
        this.y1 = 0 + shiftY ;
        
    } 
    return true;
   
}