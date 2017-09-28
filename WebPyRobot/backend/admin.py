from django.contrib import admin
from .models import UserProfile, Tank, Armor, Caterpillar, Ia, NavSystem, Weapon, TypeItem, Inventory, DefaultIa

# Register your models here.


admin.site.register(UserProfile)
admin.site.register(Armor)
admin.site.register(Caterpillar)
admin.site.register(Ia)
admin.site.register(NavSystem)
admin.site.register(Weapon)
admin.site.register(Tank)
admin.site.register(TypeItem)
admin.site.register(Inventory)
admin.site.register(DefaultIa)