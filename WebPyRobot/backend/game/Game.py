import json
from math import *
from random import *

from django.conf import settings

from ..models import BattleHistory, Notification


class Robot(object):

    def __init__(self, tank, id):
        self.__tank = tank
        self.__life = tank.hp_value
        self.__pm = self.__tank.caterpillar.moveValue
        self.__pa = self.__tank.navSystem.actionValue
        self.__cpa = self.__pa
        self.__cpm = self.__pm
        self.__arm = self.__tank.armor.armorValue

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

    def gettankarm(self):
        return self.__arm

    def getWeaponDamage(self):
        return self.__tank.weapon.attackValue

    def getRange(self):
        return self.__tank.weapon.range

    def getWPa(self):
        return self.__tank.weapon.attackCost


class Game(object):
    def __init__(self, r1, r2, ia1, ia2, champ):
        self.__size = settings.BATTLE_MAP_SIZE
        self.__map = []
        self.__current = 0
        self.__robots = [Robot(r1, 0), Robot(r2, 1)]
        self.__robotsia = [ia1, ia2]
        self.__result = []
        for i in range(self.__size*self.__size):
            self.__map.append(-1)
        self.__map[0] = 0
        self.__map[self.__size*self.__size - 1] = 1
        self.__champ = champ

    def getSize(self):
        return self.__size

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
        return (abs(self.getCellPosX(numCellB) - self.getCellPosX(numCellA)) +
                abs(self.getCellPosY(numCellB) - self.getCellPosY(numCellA)))

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

    def moveTank(self, NumCell, PA=2):
        if NumCell > self.__size*self.__size - 1:
            return -1

        pm = self.getPM(self.__current) # useless
        pa_init = self.getPA(self.__current) # PA <= 4
        # print("%s PA: %s > %s" % (self.__current, pa_init, PA))
        if PA < pa_init:
            pa = PA
        else:
            pa = pa_init

        # if self.__current == 0:
            # print("MOVE PA (before while): %s" % pa)

        pos = self.getPosition(self.__current)
        xp = self.getCellPosX(NumCell)
        yp = self.getCellPosY(NumCell)
        x = self.getCellPosX(pos)
        y = self.getCellPosY(pos)
        cpt = 0
        while pa > 0 and pos != NumCell:
            if x > xp:
                # gauche
                if pa > 0 and self.__map[self.getCellFromXY(x - 1, y)] == -1:
                    self.__result.append([self.__current, "moveLeft", 0, 0, 0])
                    self.__map[pos] = -1
                    self.__map[self.getCellFromXY(x - 1, y)] = self.__current
                    pa -= 1
                    x -= 1
                    pos = self.getPosition(self.__current)

            if x < xp :
                #droite
                if pa > 0 and self.__map[self.getCellFromXY(x + 1, y)] == -1:
                    self.__result.append([self.__current, "moveRight", 0, 0, 0])
                    self.__map[pos] = -1
                    self.__map[self.getCellFromXY(x + 1, y)] = self.__current
                    pa -=1
                    x += 1
                    pos = self.getPosition(self.__current)

            if y > yp :
                #Bas
                if pa > 0 and self.__map[self.getCellFromXY(x, y-1)] == -1:
                    self.__result.append([self.__current, "moveDown", 0, 0, 0])
                    self.__map[pos] = -1
                    self.__map[self.getCellFromXY(x , y-1)] = self.__current
                    pa -=1
                    y -= 1
                    pos = self.getPosition(self.__current)

            if y < yp :
                #Haut
                if pa > 0 and self.__map[self.getCellFromXY(x, y + 1)] == -1:
                    self.__result.append([self.__current, "moveUp", 0, 0, 0])
                    self.__map[pos] = -1
                    self.__map[self.getCellFromXY(x, y+1)] = self.__current
                    pa -=1
                    y += 1
                    pos = self.getPosition(self.__current)

            cpt += 1
            # if cpt >= self.__robots[self.__current].getPM(): return
            if PA < pa_init:
                if cpt >= PA: return
            else:
                if cpt >= pa_init: return


        self.__robots[self.__current].setPM(pm) # useless
        if PA < pa_init:
            self.__robots[self.__current].setPA(pa_init-PA)
        else:
            self.__robots[self.__current].setPA(pa)

    def shoot(self):
        pos = self.getPosition(self.getEnemyTankId())
        x = self.getCellPosX(pos)
        y = self.getCellPosY(pos)

        posp = self.getPosition(self.__current)
        xp = self.getCellPosX(posp)
        yp = self.getCellPosY(posp)

        dist = self.getCellDistance(self.getCellFromXY(x, y), self.getCellFromXY(xp, yp))

        pa = self.__robots[self.__current].getPointAction() # PA <= 4

        # if self.__current == 0:
            # print("SHOOT PA: %s" % pa)

        paWe = self.__robots[self.__current].getWPa() # WPA = 1

        dWe = self.__robots[self.__current].getWeaponDamage() # WATK = 15

        arm = self.__robots[self.__current].gettankarm() # useless

        # reduce_dmg = int(arm*dWe/100)

        # real_dmg = dWe - reduce_dmg

        rest_pv = self.__robots[self.getEnemyTankId()].getLife()-dWe

        range = self.__robots[self.__current].getRange()
        mid_point = int(self.__size/2)
        if pa - paWe >= 0:
            if dist > range:
                self.__result.append([self.__current, "shoot", mid_point, mid_point, 0])
            else:
                self.__result.append([self.__current, "shoot", x, y, rest_pv])
                self.__robots[self.getEnemyTankId()].setLife(rest_pv)
            self.__robots[self.__current].setPA(pa-paWe)

    def is_victorious(self):
        """
        Check if the player who starts the battle is the winner or not
        :return:
        """
        for i in self.__result:
            if i[1] == "dead":
                if i[0] == 1:
                    return True
        return False

    def set_history(self, map_name, is_training):
        """
        Save history of a battle
        :return: ID of BattleHistory object
        """
        robot1 = self.__robots[0]
        robot2 = self.__robots[1]
        tank1 = robot1.getTank()
        tank2 = robot2.getTank()
        player = tank1.owner.user
        opponent = tank2.owner.user
        bh = BattleHistory.objects.create(
            user=player,
            used_script=tank1.owner.get_active_ai_script(),
            opp_used_script=tank2.owner.get_active_ai_script(),
            opponent=opponent,
            is_victorious=self.is_victorious(),
            result_stats=json.dumps(self.__result),
            max_step=len(self.__result),
            map_name=map_name,
            mode=is_training,
            championship_name=self.__champ
        )
        return bh.pk

    def set_history_itself(self, map_name, is_training, script_op):
        """
        Save history of a battle
        :return: ID of BattleHistory object
        """
        robot1 = self.__robots[0]
        robot2 = self.__robots[1]
        tank1 = robot1.getTank()
        tank2 = robot2.getTank()
        player = tank1.owner.user
        opponent = tank2.owner.user
        bh = BattleHistory.objects.create(
                user=player,
                used_script=tank1.owner.get_active_ai_script(),
                opp_used_script=script_op,
                opponent=opponent,
                is_victorious=self.is_victorious(),
                result_stats=json.dumps(self.__result),
                max_step=len(self.__result),
                map_name=map_name,
                mode=is_training,
                championship_name=self.__champ
            )
        return bh.pk

    def notify_endgame(self):
        robot1 = self.__robots[0]
        robot2 = self.__robots[1]
        tank1 = robot1.getTank()
        tank2 = robot2.getTank()
        user1 = tank1.owner.user
        user2 = tank2.owner.user
        Notification.objects.create(user=user1.user, content="Le combat contre %s vient de se terminer" % user2.user.username,
                                    is_read=True)
        Notification.objects.create(user=user2.user,
                                    content="Le combat contre %s vient de se terminer" % user1.user.username)

    def run(self, i):
        if i >= 100:
            return self.__result

        self.__current = 0
        exec(self.__robotsia[0].text)
        self.__result.append([0, "endTurn", 0, 0, 0])
        self.__result.append([0, "endTurn", 0, 0, 0])

        if self.__robots[1].getLife() <= 0:
            self.__result.append([1, "dead", 0, 0, 0])
            return self.__result

        self.__current = 1
        exec(self.__robotsia[1].text)
        self.__result.append([1, "endTurn", 0, 0, 0])
        self.__result.append([0, "endTurn", 0, 0, 0])

        self.__robots[0].setPM(self.__robots[0].gettankpm())
        self.__robots[0].setPA(self.__robots[0].gettankpa())
        self.__robots[1].setPM(self.__robots[1].gettankpm())
        self.__robots[1].setPA(self.__robots[1].gettankpa())

        if self.__robots[0].getLife() <= 0:
            self.__result.append([0, "dead", 0, 0, 0])
            return self.__result

        return self.run(i + 1)
