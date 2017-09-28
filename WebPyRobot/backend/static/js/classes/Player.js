var STATE = {
    "UP"   : 0,
    "RIGHT" : 1,
    "DOWN"    : 2,
    "LEFT" : 3,
    "DIAGONALEUPRIGHT": 4,
    "DIAGONALEDOWNRIGHT" : 5,
    "DIAGONALEDOWNLEFT" : 6,
    "DIAGONALEUPLEFT"   : 7,
    "DEAD"              : 8,
}

var TIME_MOVING = 3;
var NB_IMAGE = 9;

function Player(url, x, y, direction,contraint) {
    this.x = x; // (en cases)
    this.y = y; // (en cases)
    this.direction = direction;
    this.stateAnimation = -1;
    
    // Chargement de l'image dans l'attribut image
    this.image = new Image();
    this.image.refPlayer = this;
    this.image.onload = function() {
        if(!this.complete) 
            throw "Erreur de chargement du sprite nommé \"" + url + "\".";
        
        // Taille du personnage
        this.refPlayer.width = this.width / NB_IMAGE;
        this.refPlayer.height = this.height / 8;
    }
    this.image.src = "../static/sprites/" + url;
    this.contraint = contraint;
}

Player.prototype.drawPlayer = function(context) {
    var frame = 0; // Numéro de l'image à prendre pour l'animation
    var shiftX = 0, shiftY = 0; // Décalage à appliquer à la position du personnage
    if(this.stateAnimation >= TIME_MOVING) {
        // Si le déplacement a atteint ou dépassé le temps nécéssaire pour s'effectuer, on le termine
        this.stateAnimation = -1;
    } else if(this.stateAnimation >= 0) {

        frame = this.stateAnimation %NB_IMAGE;
        if(frame > NB_IMAGE) {
            frame %= NB_IMAGE;
        }
        
        // Nombre de pixels restant à parcourir entre les deux cases
        var pixelsAParcourir = 32/this.contraint - (32/this.contraint * (this.stateAnimation / TIME_MOVING));
        
        // À partir de ce nombre, on définit le décalage en x et y.
        if(this.direction == STATE.UP) {
            shiftY = pixelsAParcourir;
        } else if(this.direction == STATE.DOWN) {
            shiftY = -pixelsAParcourir;
        } else if(this.direction == STATE.LEFT) {
            shiftX = pixelsAParcourir;
        } else if(this.direction == STATE.RIGHT) {
            shiftX = -pixelsAParcourir;
        }else if(this.direction == STATE.DIAGONALEUPLEFT){
            shiftY = pixelsAParcourir;
            shiftX = pixelsAParcourir;
        }else if(this.direction == STATE.DIAGONALEUPRIGHT){
            shiftY = pixelsAParcourir;
            shiftX = -pixelsAParcourir;
        }else if(this.direction == STATE.DIAGONALEDOWNLEFT){
            shiftY = -pixelsAParcourir;
            shiftX = pixelsAParcourir;
        }else if(this.direction == STATE.DIAGONALEDOWNRIGHT){
            shiftY = -pixelsAParcourir;
            shiftX = -pixelsAParcourir;
        }
        
        this.stateAnimation++;
    }
    
    if(this.direction != STATE.DEAD){
        context.drawImage(
            this.image, 
            this.width * frame, this.direction * this.height, // Point d'origine du rectangle source à prendre dans notre image
            this.width, this.height, // Taille du rectangle source (c'est la taille du personnage)
            (this.x * 32/this.contraint) - (this.width /7/this.contraint ) + shiftX, (this.y * 32/this.contraint) - this.height/7/this.contraint + shiftY,
            this.width/1.4/this.contraint, this.height/1.4/this.contraint 
        );
        if(this.direction > 3 && this.stateAnimation == -1) {
            this.direction = this.direction %4;
            this.stateAnimation = 15;
        }
    }
}

Player.prototype.getNextCoordonnee = function(direction) {
    var coord = {'x' : this.x, 'y' : this.y};
    switch(direction) {
        case STATE.DOWN : 
            coord.y++;
            break;
        case STATE.LEFT : 
            coord.x--;
            break;
        case STATE.RIGHT : 
            coord.x++;
            break;
        case STATE.UP : 
            coord.y--;
            break;
    }
    return coord;
}

Player.prototype.move = function(direction, map) {
    if(this.stateAnimation >= 0) {
        return false;
    }
    this.direction = direction;
        
    var nextSquare = this.getNextCoordonnee(direction);
    if(nextSquare.x < 0 || nextSquare.y < 0 || nextSquare.x >= map.getLargeur() || nextSquare.y >= map.getHauteur()) {
        return false;
    }
    
    this.stateAnimation = 1;
        
    this.x = nextSquare.x;
    this.y = nextSquare.y;
    

    return true;
}


Player.prototype.shoot= function(x, y, x1, y1) {

    var direction = this.direction; 
    if(y == y1){
        if(x < x1)
            this.direction = STATE.RIGHT;
        else 
            this.direction = STATE.LEFT;
    }
    else if(x == x1){

        if(y < y1)
            this.direction = STATE.DOWN;
        else 
            this.direction = STATE.UP;
    }

    else if(x > x1){
        if(y < y1)
            this.direction = STATE.DIAGONALEDOWNLEFT;
        else 
            this.direction = STATE.DIAGONALEUPLEFT;
    }
    else 
        if(y < y1)
            this.direction = STATE.DIAGONALEDOWNRIGHT;
        else 
            this.direction = STATE.DIAGONALEUPRIGHT;

    this.stateAnimation = 1;
}


Player.prototype.dead = function(){
    this.direction = STATE.DEAD;
}