
function Map(name,contraint) {
	// Création de l'objet XmlHttpRequest
	var xhr = getXMLHttpRequest();
		
	// Chargement du fichier
	xhr.open("GET", '../static/maps/' + name + '.json', false);
	xhr.send(null);
	if(xhr.readyState != 4 || (xhr.status != 200 && xhr.status != 0)) // Code == 0 en local
		throw new Error("Impossible de charger la carte nommé \"" + name + "\" (code HTTP : " + xhr.status + ").");
	var mapJsonData = xhr.responseText;
	
	// Analyse des données
	var mapData = JSON.parse(mapJsonData);
	this.tileset = new Tileset(mapData.tileset,contraint);
	this.ground = mapData.ground;
	this.contraint = contraint;
	// Liste des player présents sur le terrain.
	this.player = new Array();
	this.bird = new Array();
	this.bullet = new Array();
}

// Pour récupérer la taille (en tiles) de la carte
Map.prototype.getHauteur = function() {
	return this.ground.length;
}
Map.prototype.getLargeur = function() {
	return this.ground[0].length;
}

// Pour ajouter un personnage
Map.prototype.addPlayer = function(character) {
	this.player.push(character);
}

Map.prototype.addBird= function(bird) {
	this.bird.push(bird);
}

Map.prototype.addBullet = function (bullet) {
	this.bullet.push(bullet);
}

Map.prototype.dessinerMap = function(context) {

	for(var i = 0, l = this.ground.length ; i < l ; i++) {
		var line = this.ground[i];
		var y = i * 32/this.contraint;
		for(var j = 0, k = line.length ; j < k ; j++) {
			this.tileset.drawTile(line[j], context, j * 32/this.contraint, y);
		}
	}
	// Dessin des player
	for(var i = 0, l = this.player.length ; i < l ; i++) {
		this.player[i].drawPlayer(context);
	}

	for (var i = 0; i < this.bird.length; i++) {
		if(!this.bird[i].drawBird(context)){
			this.bird.splice(i,1);
		}
	}
	for (var i = 0; i < this.bullet.length; i++) {
		if(!this.bullet[i].drawBullet(context)){
			this.bullet.splice(i,1);
		}
	}		
}