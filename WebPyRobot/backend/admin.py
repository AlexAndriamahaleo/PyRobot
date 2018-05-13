from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from .models import UserProfile, Tank, Armor, Caterpillar, Ia, NavSystem, Weapon, TypeItem, Inventory, DefaultIa, FAQ, BattleHistory, Championship

# Register your models here.
class FAQAdminForm(forms.ModelForm):
    answer = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'symbol']


class FAQAdmin(admin.ModelAdmin):
    form = FAQAdminForm
    list_display = ['question']


class BattleHistoryAdmin(admin.ModelAdmin):
    list_display = ['get_player_name', 'get_opp_name', 'timestamp']

    def get_player_name(self, obj):
        return obj.player_name()

    def get_opp_name(self, obj):
        return obj.opponent_name()

    get_player_name.short_description = 'Player'
    get_player_name.admin_order_field = 'user__username'

    get_opp_name.short_description = "Opponent"
    get_opp_name.admin_order_field = "opponent__username"


class ChampionshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'private_mode', 'secret_word', 'players']

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
admin.site.register(BattleHistory, BattleHistoryAdmin)
admin.site.register(Championship)