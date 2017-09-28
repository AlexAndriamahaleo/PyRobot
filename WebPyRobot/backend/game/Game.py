class Robot(object):
    def __init__(self, tank, id):
        self.__tank = tank
        self.__life = 100
        self.__pm = self.__tank.caterpillar.moveValue
        self.__pa = self.__tank.navSystem.actionValue
        self.__cpa = self.__pa
        self.__cpm = self.__pm

    def getTank(self):
        return self.__tank
    def getTankId(self):
        return self.__tank.id
    def getLife(self):
        return self.__life
    def getPM(self):
        return self.__cpm
    def getPointAction(self):
        return self.__cpa
    def setLife(self, life):
        self.__life = life
    def setPM(self, pm):
        self.__cpm = pm
    def setPA(self, pa):
        self.__cpa = pa
    def gettankpa(self):
        return self.__pa
    def gettankpm(self):
        return self.__pm
    def getWeaponDamage(self):
        return self.__tank.weapon.attackValue
    def getRange(self):
        return self.__tank.weapon.range
    def getWPa(self):
        return self.__tank.weapon.attackCost

class Game(object):
    def __init__(self, r1, r2, ia1, ia2):
        self.__size = 32
        self.__map = []
        self.__current = 0
        self.__robots = [Robot(r1, 0), Robot(r2, 1)]
        self.__robotsia = [ia1, ia2]
        self.__result = []
        for i in range (self.__size*self.__size):
            self.__map.append(-1)
        self.__map[0] = 0
        self.__map[self.__size*self.__size - 1] = 1

    def getTankId(self):
        return self.__current

    def getEnemyTankId(self):
        if self.__current == 0:
            return 1
        else:
            return 0

    def getCellPosX(self, numCell):
        return numCell - (self.__size * (numCell // self.__size))

    def getCellPosY(self, numCell):
        return numCell // self.__size

    def getCellDistance(self, numCellA, numCellB):
        return (abs(self.getCellPosX(numCellB) - self.getCellPosX(numCellA)) + abs(self.getCellPosY(numCellB) - self.getCellPosY(numCellA)) )

    def getCellFromXY(self, x, y):
        return y*self.__size + x

    def getPosition(self, TankID):
        for i in range(self.__size*self.__size):
            if self.__map[i] == TankID:
                return i
        return -1

    def getLife(self, TankID):
        return self.__robots[TankID].getLife()

    def getPM(self, TankID):
        return self.__robots[TankID].getPM()

    def getPA(self, TankID):
        return self.__robots[TankID].getPointAction()

    def getRange(self, TankID):
        return self.__robots[TankID].getRange()

    def moveTank(self, NumCell):
        if NumCell > self.__size*self.__size - 1:
            return -1
        pm = self.getPM(self.__current)
        pos = self.getPosition(self.__current)
        xp = self.getCellPosX(NumCell)
        yp = self.getCellPosY(NumCell)
        x = self.getCellPosX(pos)
        y = self.getCellPosY(pos)
        cpt = 0;
        while pm > 0 and pos != NumCell:
            if x > xp:
                # gauche
                if pm > 0 and self.__map[self.getCellFromXY(x - 1, y)] == -1:
                    self.__result.append([self.__current, "moveLeft", 0, 0])
                    self.__map[pos] = -1
                    self.__map[self.getCellFromXY(x - 1, y)] = self.__current
                    pm -= 1
                    x -= 1
                    pos = self.getPosition(self.__current)

            if x < xp :
                #droite
                if pm > 0 and self.__map[self.getCellFromXY(x + 1, y)] == -1:
                    self.__result.append([self.__current, "moveRight", 0, 0])
                    self.__map[pos] = -1
                    self.__map[self.getCellFromXY(x + 1, y)] = self.__current
                    pm -=1
                    x += 1
                    pos = self.getPosition(self.__current)

            if y > yp :
                #Bas
                if pm > 0 and self.__map[self.getCellFromXY(x, y-1)] == -1:
                    self.__result.append([self.__current, "moveDown", 0, 0])
                    self.__map[pos] = -1
                    self.__map[self.getCellFromXY(x , y-1)] = self.__current
                    pm -=1
                    y -= 1
                    pos = self.getPosition(self.__current)

            if y < yp :
                #Haut
                if pm > 0 and self.__map[self.getCellFromXY(x, y + 1)] == -1:
                    self.__result.append([self.__current, "moveUp", 0, 0])
                    self.__map[pos] = -1
                    self.__map[self.getCellFromXY(x, y+1)] = self.__current
                    pm -=1
                    y += 1
                    pos = self.getPosition(self.__current)

            cpt += 1
            if cpt >= self.__robots[self.__current].getPM(): return


        self.__robots[self.__current].setPM(pm)

    def shoot(self):
        pos = self.getPosition(self.getEnemyTankId())
        x = self.getCellPosX(pos)
        y = self.getCellPosY(pos)

        posp = self.getPosition(self.__current)
        xp = self.getCellPosX(posp)
        yp = self.getCellPosY(posp)

        dist = self.getCellDistance(self.getCellFromXY(x,y),self.getCellFromXY(xp,yp))

        pa = self.__robots[self.__current].getPointAction()
        paWe = self.__robots[self.__current].getWPa()
        dWe = self.__robots[self.__current].getWeaponDamage()
        range = self.__robots[self.__current].getRange()
        if pa - paWe >= 0:
            if(dist > range):
                    self.__result.append([self.__current, "shoot", 16, 16])
            else:
                self.__result.append([self.__current, "shoot",x, y])
                self.__robots[self.getEnemyTankId()].setLife(self.__robots[self.getEnemyTankId()].getLife()-dWe)
            self.__robots[self.__current].setPA(pa-paWe)

    def run(self, i):
        # for i in range(0, 64):
        if i >= 100: return self.__result
        if self.__robots[0].getLife() <= 0:
            self.__result.append([0, "dead", 0, 0])
            return self.__result
        if self.__robots[1].getLife() <= 0:
            self.__result.append([1, "dead", 0, 0])
            return self.__result

        def exit():
            pass
        self.__current = 0
        exec (self.__robotsia[0].text)
        self.__result.append([0, "endTurn", 0, 0])
        self.__result.append([0, "endTurn", 0, 0])
        self.__current = 1
        exec (self.__robotsia[1].text)
        self.__result.append([1, "endTurn", 0, 0])
        self.__result.append([0, "endTurn", 0, 0])

        self.__robots[0].setPM(self.__robots[0].gettankpm())
        self.__robots[0].setPA(self.__robots[0].gettankpa())
        self.__robots[1].setPM(self.__robots[1].gettankpm())
        self.__robots[1].setPA(self.__robots[1].gettankpa())

#         text = """
# # Default ia
#
# # Get the enemy position in the game
# enemy = self.getEnemyTankId()
# enemypos = self.getPosition(enemy)
#
# # Move foward to the enemy
# self.moveTank(enemypos)
#
# # Shoot the enemy Gracefuly
# self.shoot()
# """
#         exec (text)
#         print (text)

        return self.run(i + 1)

        # return self.__result

