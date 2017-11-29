from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from .models import UserProfile, Tank, Armor, Caterpillar, Ia, NavSystem, Weapon, TypeItem, Inventory, DefaultIa, FAQ, BattleHistory

# Register your models here.
class FAQAdminForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'symbol']

class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm

admin.site.register(FAQ, FAQAdmin)

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
# admin.site.register(FAQ)
admin.site.register(BattleHistory)