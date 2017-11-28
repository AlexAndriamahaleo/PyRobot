from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(blank=True)
    agression = models.BooleanField(default=False)

    #Exp - R&D
    exp = models.PositiveIntegerField(default=0)
    srch = models.PositiveIntegerField(default=0)
    dev = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=0)
    next_level_exp = models.PositiveIntegerField(default=int(1/settings.EXP_CONSTANT))
    true_level = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user.username

    def __getInventory__(self):
        wep = Inventory.objects.filter(owner=self,typeItem=TypeItem(pk=1))
        wOut = []
        for w in wep:
            wOut.append(getItemByType(w.item,TypeItem(pk=1)))
        arm = Inventory.objects.filter(owner=self, typeItem=TypeItem(pk=2))
        aOut =[]
        for a in arm:
            aOut.append(getItemByType(a.item,TypeItem(pk=2)))
        cater = Inventory.objects.filter(owner=self, typeItem=TypeItem(pk=3))
        cOut = []
        for c in cater:
            cOut.append(getItemByType(c.item, TypeItem(pk=3)))
        sys = Inventory.objects.filter(owner=self, typeItem=TypeItem(pk=4))
        sOut = []
        for s in sys:
            sOut.append(getItemByType(s.item, TypeItem(pk=4)))
        return [wOut, aOut, cOut, sOut]

    def get_active_ai_script(self):
        ai_scripts = self.ia_set.filter(active=True)
        if ai_scripts:
            return list(ai_scripts)[0]
        return None

    def change_active_ai(self, new_ai):
        old_ai = self.get_active_ai_script()
        if old_ai:
            old_ai.active = False
            old_ai.save()
        new_ai.active = True
        new_ai.save()
        tank = self.tank_set.all()[0]
        tank.ia = new_ai
        tank.save()

    @property
    def get_ai_name(self):
        ai = self.get_active_ai_script()
        if ai:
            return ai.name
        return "No Active Script"

    def get_running_battle(self):
        """
        Get the current battle
        :return:
        """
        battle = self.user.battlehistories.filter(is_finished=False)
        if battle:
            return battle[0]
        return None

    def calc_next_level_exp(self):
        self.next_level_exp = int((self.level + 1)**2/settings.EXP_CONSTANT)
        # instance.save()

# pre_save.connect(calc_next_level_exp, sender=UserProfile)



class Ia(models.Model):
    owner = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=50, default='')
    text = models.TextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def getIaByOwner(user):
        return Ia.objects.get(owner=user)

def create_ia_name(sender, instance, raw, created, **kwargs):
    if instance.name == '':
        instance.name = "AI Script %s" % instance.pk
        instance.save()

post_save.connect(create_ia_name, sender=Ia)


class Weapon(models.Model):

    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    attackValue = models.PositiveIntegerField()
    range = models.PositiveIntegerField()
    attackCost = models.PositiveIntegerField()
    pathIcon = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    def isInInventory(self,user):
        inv = Inventory.objects.filter(owner=user,typeItem=TypeItem(pk=1), item=self.pk)
        if inv.count() > 0 :
            return True
        else:
            return False

class Armor(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    armorValue = models.PositiveIntegerField()
    pathIcon = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    def isInInventory(self,user):
        inv = Inventory.objects.filter(owner=user,typeItem=TypeItem(pk=2), item=self.pk)
        if inv.count() > 0 :
            return True
        else:
            return False

class Caterpillar(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    moveValue = models.PositiveIntegerField()
    pathIcon = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    def isInInventory(self,user):
        inv = Inventory.objects.filter(owner=user,typeItem=TypeItem(pk=3), item=self.pk)
        if inv.count() > 0 :
            return True
        else:
            return False


class NavSystem(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    actionValue = models.PositiveIntegerField()
    pathIcon = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def isInInventory(self,user):
        inv = Inventory.objects.filter(owner=user,typeItem=TypeItem(pk=4), item=self.pk)
        if inv.count() > 0 :
            return True
        else:
            return False


class Tank(models.Model):
    owner = models.ForeignKey(UserProfile)
    ia = models.ForeignKey(Ia)
    weapon = models.ForeignKey(Weapon)
    armor = models.ForeignKey(Armor)
    caterpillar = models.ForeignKey(Caterpillar)
    navSystem = models.ForeignKey(NavSystem)

    def __str__(self):
        return self.owner.__str__()


class TypeItem (models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Inventory (models.Model):
    owner = models.ForeignKey(UserProfile)
    item = models.PositiveIntegerField()
    typeItem = models.ForeignKey(TypeItem)

    def __str__(self):
        return self.owner.__str__() + ",.... " + getItemByType(self.item, self.typeItem).__str__()


class DefaultIa (models.Model):
    text = models.TextField()

def getItemByType(itemIn,type):
    if type ==  TypeItem(pk=1) :
        return Weapon.objects.get(pk=itemIn)
    elif type == TypeItem(pk=2):
        return Armor.objects.get(pk=itemIn)
    elif type == TypeItem(pk=3):
        return Caterpillar.objects.get(pk=itemIn)
    elif type == TypeItem(pk=4) :
        return NavSystem.objects.get(pk=itemIn)


class BattleHistory(models.Model):
    user = models.ForeignKey(User, related_name="battlehistories")
    opponent = models.ForeignKey(User, related_name="opponents")
    is_victorious = models.BooleanField(default=False)
    used_script = models.ForeignKey(Ia, related_name='+', null=True, default=None)
    opp_used_script = models.ForeignKey(Ia, related_name='+', null=True, default=None)
    # Status of a battle. We need to show clients that battle is realtime not a replay :))
    is_finished = models.BooleanField(default=False, db_index=True)
    # Animation step index.
    step = models.PositiveIntegerField(default=0)
    max_step = models.PositiveIntegerField(default=0)
    # Result array. We should us JsonField but it's only available in PostgreSQL now
    result_stats = models.TextField(default='')
    player_x = models.PositiveIntegerField(default=0)
    player_y = models.PositiveIntegerField(default=0)
    opponent_x = models.PositiveIntegerField(default=0)
    opponent_y = models.PositiveIntegerField(default=0)
    map_name = models.CharField(max_length=10, default="terre")
    timestamp = models.DateTimeField(auto_now_add=True)
    difficult_level = models.CharField(max_length=10, default="normal")


class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications")
    content = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)