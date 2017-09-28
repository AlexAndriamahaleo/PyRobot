from backend.models import Armor, Caterpillar, Ia, NavSystem, TypeItem, Weapon

def getItemByType(itemIn,type):
    if type ==  TypeItem(pk=1) :
        return Weapon.objects.get(pk=itemIn)
    elif type == TypeItem(pk=2):
        return Armor.objects.get(pk=itemIn)
    elif type == TypeItem(pk=3):
        return Caterpillar.objects.get(pk=itemIn)
    elif type == TypeItem(pk=4) :
        return NavSystem.objects.get(pk=itemIn)

def getBoolInventory(currentUser):
    weapons = Weapon.objects.all();
    wB = []
    for w in weapons:
        wB.append(w.isInInventory(currentUser))
    armors = Armor.objects.all();
    aB = []
    for a in armors:
        aB.append(a.isInInventory(currentUser))
    caterpillars = Caterpillar.objects.all();
    cB = []
    for c in caterpillars:
        cB.append(c.isInInventory(currentUser))
    navSys = NavSystem.objects.all();
    nB = []
    for n in navSys:
        nB.append(n.isInInventory(currentUser))
    return [wB, aB, cB, nB ]