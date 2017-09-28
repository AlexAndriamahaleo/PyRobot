from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(blank=True)
    agression = models.BooleanField(default=False)

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

class Ia(models.Model):
    owner = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=50, default='')
    text = models.TextField()

    def __str__(self):
        return self.name
    def getIaByOwner(user):
        return Ia.objects.get(owner=user)


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
