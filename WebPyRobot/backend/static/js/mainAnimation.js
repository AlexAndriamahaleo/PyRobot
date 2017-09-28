
var stringReceive = a;

var tabReceive = [];

var suprStr = 	function (stringReceive){
					var str = "";
					var miniTab = [];
					for (var i = 1; i < stringReceive.length-1; i++) {
						if(stringReceive[i] == '[' ||
						   stringReceive[i] == ' ' ||
						   stringReceive[i] == '\"'){}
						else if (stringReceive[i] == ',') {
							if(stringReceive[i + 2] != '[' ){
								miniTab.push(str);
								str = "";
							}
						}
						else if (stringReceive[i] == ']') {
							miniTab.push(str);
							str = "";
							tabReceive.push(miniTab);
							miniTab = [];
						}
						else
							str = str + stringReceive[i];

					}
				};
// var tabReceive = [["0","moveDown","0","1"],
// 				  ["0","shoot","10","10"],
// 				  ["0","moveDown","0","0"],
// 				  ["0","moveRigth","0","0"],
// 				  ["0","moveDown","0","0"],
// 				  ["0","moveDown","0","0"],
// 				  ["0","moveDown","0","0"],
// 				  ["0","moveDown","0","0"],
// 				  ["0","shoot","31","31"],
// 				  ["0","endTurn","31","31"],
// 				  ["1","moveUp","0","0"],
// 				  ["1","shoot","0","0"],
// 				  ["1","moveUp","0","0"],
// 				  ["1","moveUp","0","0"]];




var winWidth = (window.innerWidth);
var winHieght = (window.innerHeight);

var contraint =36/(Math.min(winHieght,winWidth)/36);

if(Math.floor((Math.random() * 2) + 1) == 2){
	var map = new Map("terre",contraint);
}
else
	var map = new Map("premiere",contraint);

var player1 = new Player("tank1.png", 0, 0, STATE.DOWN,contraint);
map.addPlayer(player1);

var player2 = new Player("tank2.png", 31, 31, STATE.UP,contraint);
map.addPlayer(player2);


var animation = new Array();
var tir = new Array();

var moveDown = function(player,x,y){
	player.move(STATE.UP,map);
};

var moveUp = function(player,x,y){
	player.move(STATE.DOWN,map);
};

var moveLeft = function(player,x,y){
	player.move(STATE.LEFT,map);
};

var moveRigth = function(player,x,y){
	player.move(STATE.RIGHT,map)
};

var deadPlayer = function(player){
	player.dead();
	if (player == player1)
		document.getElementById("win").innerHTML = "Le joueur 2 a gagné.";
	else 
		document.getElementById("win").innerHTML = "Le joueur 1 a gagné.";
};	

var shoot = function(player,x,y){
	var ctx = canvas.getContext('2d');
	var bullet;
	player.shoot(player.x,player.y,x,y);
	if(x == player1.x && y == player1.y){
		bullet = new Bullet ("tir.png",player.x,player.y,player1.direction, player1.x, player1.y,contraint);
	}
	else if(x == player2.x && y == player2.y){
		bullet = new Bullet ("tir.png",player.x,player.y,player2.direction, player2.x, player2.y,contraint);
	}
	else
		bullet = new Bullet ("tir.png",player.x,player.y,-2,x,y,contraint);
	map.addBullet(bullet);
	tir.push(bullet);
};

var initAnimation = function(){
	for (var i = 0; i < this.tabReceive.length; i++) {
		if(tabReceive[i][0]  == "0"){
			tabReceive[i][0] = player1;
		}
		else
			tabReceive[i][0] = player2;

		if(tabReceive[i][1] == "moveDown") {
			animation[i] = function(i){
				moveDown(tabReceive[i][0],tabReceive[i][2],tabReceive[i][3]);
			};
		}
		else if(tabReceive[i][1] == "moveUp")
			animation[i] = function(i){
				moveUp(tabReceive[i][0],tabReceive[i][2],tabReceive[i][3]);
			};

		else if(tabReceive[i][1] == "moveLeft")
			animation[i] = function(i){
				moveLeft(tabReceive[i][0],tabReceive[i][2],tabReceive[i][3]);
			};

		else if(tabReceive[i][1] == "moveRight") {
			animation[i] = function(i){
				moveRigth(tabReceive[i][0],tabReceive[i][2],tabReceive[i][3]);
			};
		}
		else if(tabReceive[i][1] == "shoot" ){
			animation[i] = function (i){
				shoot(tabReceive[i][0],tabReceive[i][2],tabReceive[i][3]);
			};
		}
		else if(tabReceive[i][1] == "endTurn" ){
			animation[i] = function (i){

			};
		}
		else if(tabReceive[i][1] == "dead")
			animation[i] = function (i){ 
				deadPlayer(tabReceive[i][0]);
			
		}

	}
};

window.onload = function() {

	var canvas = document.getElementById('canvas');
	var ctx = canvas.getContext('2d');

	canvas.width  = map.getLargeur() * 32 /contraint;
	canvas.height = map.getHauteur() * 32 /contraint;

	var j = 0;
	var i = 0;
	var k = 0;

	suprStr(stringReceive);
	initAnimation();

	setInterval(function() {
		map.dessinerMap(ctx);
	}, 60);

	var asbird;
	var xbird;
	var ybird;

	setInterval(function() {
		    if(j < animation.length){
		    	animation[j](j);
		   		++j;
		   	}
		   asbird =Math.floor((Math.random() * 20) + 1);
		   if(asbird == 1){
		   	var xbird = Math.floor((Math.random() * 32) + 1);
		   	map.addBird(new Bird("bird.png",xbird,0,0,xbird,32,contraint));
		   }
		   else if(asbird == 2){
		   	var xbird = Math.floor((Math.random() * 32) + 1);
		   	map.addBird(new Bird("bird.png",xbird,32,2,xbird,0,contraint));
		   }
		   else if(asbird == 3){
		   	var ybird = Math.floor((Math.random() * 32) + 1);
		   	map.addBird(new Bird("bird.png",0,ybird,1,32,ybird,contraint));
		   }
		   else if(asbird == 4){
		   	var ybird = Math.floor((Math.random() * 32) + 1);
		   	map.addBird(new Bird("bird.png",32,ybird,3,32,ybird,contraint));
		   }
	}, 400);
};
