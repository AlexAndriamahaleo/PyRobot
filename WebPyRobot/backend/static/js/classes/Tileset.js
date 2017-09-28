

function Tileset(url,contraint) {
	// Chargement de l'image dans l'attribut image
	this.image = new Image();
	this.image.referenceDuTileset = this;
	this.image.onload = function() {
		if(!this.complete) 
			throw new Error("Erreur de chargement du tileset nommé \"" + url + "\".");
		
		// Largeur du tileset en tiles
		this.referenceDuTileset.largeur = this.width / 32;
	}
	this.contraint = contraint;
	this.image.src = "../static/tilesets/" + url;
}

// Méthode de dessin du tile numéro "number" dans le contexte 2D "context" aux coordonnées xDestination et yDestination
Tileset.prototype.drawTile = function(number, context, xDestination, yDestination) {
	var xSourceEnTiles = number % this.largeur;
	if(xSourceEnTiles == 0) xSourceEnTiles = this.largeur;
	var ySourceEnTiles = Math.ceil(number / this.largeur);
	
	var xSource = (xSourceEnTiles - 1) * 32.4;
	var ySource = (ySourceEnTiles - 1) * 33;
	
	context.drawImage(this.image, xSource, ySource, 32, 32, xDestination, yDestination, 32/this.contraint, 32/this.contraint);
}
