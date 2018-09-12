from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from ckeditor.fields import RichTextField

from django import forms
from django.core.files.images import get_image_dimensions


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    money = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(blank=True, upload_to='img/user_avatar', default="img/user_avatar/default.png")
    # avatar = models.ImageField(upload_to='img/user_avatar')
    agression = models.BooleanField(default=False)

    # championship = models.ForeignKey(Championship)

    # Exp - R&D
    points = models.PositiveIntegerField(default=0) # future points ELO
    # exp
    coeff_K = models.PositiveIntegerField(default=40) # coefficient K
    # srch
    nb_games = models.PositiveIntegerField(default=0) # nb games played
    # dev

    level = models.PositiveIntegerField(default=0) # useless
    next_level_exp = models.PositiveIntegerField(default=0) # useless
    true_level = models.PositiveIntegerField(default=1) # useless

    def __str__(self):
        return self.user.username

    def __getInventory__(self):
        wep = Inventory.objects.filter(owner=self, typeItem=TypeItem(pk=1))
        wOut = []
        for w in wep:
            wOut.append(getItemByType(w.item, TypeItem(pk=1)))
        arm = Inventory.objects.filter(owner=self, typeItem=TypeItem(pk=2))
        aOut = []
        for a in arm:
            aOut.append(getItemByType(a.item, TypeItem(pk=2)))
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

    def get_temporary_ai_script(self):
        ai_scripts = self.ia_set.filter(edit=True)
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
        self.next_level_exp = int((self.level + 1) ** 2 / settings.EXP_CONSTANT)
        # instance.save()

    def get_tank(self):
        return self.tank_set.all()[0]

    '''
    def del_user(request, username):
        try:
            u = User.objects.get(username=username)
            u.delete()
            messages.sucess(request, "The user is deleted")

        except User.DoesNotExist:
            messages.error(request, "User doesnot exist")
            return render(request, 'front.html')

        except Exception as e:
            return render(request, 'front.html', {'err': e.message})

        return render(request, 'front.html')
    '''


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ()

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        try:
            w, h = get_image_dimensions(avatar)

            # validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                    '%s x %s pixels or smaller.' % (max_width, max_height))

            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                            'GIF or PNG image.')

            # validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar


class Ia(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    text = models.TextField()
    active = models.BooleanField(default=False)
    edit = models.BooleanField(default=False)

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

    def isInInventory(self, user):
        inv = Inventory.objects.filter(owner=user, typeItem=TypeItem(pk=1), item=self.pk)
        if inv.count() > 0:
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

    def isInInventory(self, user):
        inv = Inventory.objects.filter(owner=user, typeItem=TypeItem(pk=2), item=self.pk)
        if inv.count() > 0:
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

    def isInInventory(self, user):
        inv = Inventory.objects.filter(owner=user, typeItem=TypeItem(pk=3), item=self.pk)
        if inv.count() > 0:
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

    def isInInventory(self, user):
        inv = Inventory.objects.filter(owner=user, typeItem=TypeItem(pk=4), item=self.pk)
        if inv.count() > 0:
            return True
        else:
            return False


class Tank(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ia = models.ForeignKey(Ia, on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)
    armor = models.ForeignKey(Armor, on_delete=models.CASCADE)
    caterpillar = models.ForeignKey(Caterpillar, on_delete=models.CASCADE)
    navSystem = models.ForeignKey(NavSystem, on_delete=models.CASCADE)
    hp_value = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.owner.__str__()


class TypeItem(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item = models.PositiveIntegerField()
    typeItem = models.ForeignKey(TypeItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.owner.__str__() + ",.... " + getItemByType(self.item, self.typeItem).__str__()


class DefaultIa(models.Model):
    text = models.TextField()


def getItemByType(itemIn, type):
    if type == TypeItem(pk=1):
        return Weapon.objects.get(pk=itemIn)
    elif type == TypeItem(pk=2):
        return Armor.objects.get(pk=itemIn)
    elif type == TypeItem(pk=3):
        return Caterpillar.objects.get(pk=itemIn)
    elif type == TypeItem(pk=4):
        return NavSystem.objects.get(pk=itemIn)


class BattleHistory(models.Model):
    user = models.ForeignKey(User, related_name="battlehistories", on_delete=models.CASCADE)
    opponent = models.ForeignKey(User, related_name="opponents", on_delete=models.CASCADE)
    is_victorious = models.BooleanField(default=False)
    used_script = models.ForeignKey(Ia, related_name='+', null=True, default=None, on_delete=models.CASCADE)
    opp_used_script = models.ForeignKey(Ia, related_name='+', null=True, default=None, on_delete=models.CASCADE)
    # Status of a battle. We need to show clients that battle is realtime not a replay :))
    is_finished = models.BooleanField(default=False, db_index=True)
    # Animation step index.
    step = models.PositiveIntegerField(default=0)
    max_step = models.PositiveIntegerField(default=0)
    # Result array. We should us JsonField but it's only available in PostgreSQL now
    result_stats = models.TextField(default='')
    # Player positions
    player_x = models.PositiveIntegerField(default=0)
    player_y = models.PositiveIntegerField(default=0)
    # Opponent positions
    opponent_x = models.PositiveIntegerField(default=0)
    opponent_y = models.PositiveIntegerField(default=0)
    map_name = models.CharField(max_length=10, default="terre")
    timestamp = models.DateTimeField(auto_now_add=True)
    difficult_level = models.CharField(max_length=10, default="normal")
    mode = models.BooleanField(null=False, default=False)
    championship_name = models.CharField(max_length=60, default="PyRobot [Default]")

    def player_name(self):
        return self.user.username

    def opponent_name(self):
        return self.opponent.username


class Notification(models.Model):
    """
    A notification, like Facebook notification
    Define for later use
    """
    user = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class FAQ(models.Model):
    """
    FAQ
    """
    question = models.TextField(null=False)
    answer = RichTextField(null=False)
    symbol = models.CharField(default='import_contacts', null=True, help_text='Material Icons', max_length=50)

    def save(self, *args, **kwargs):
        self.question = self.question.strip().rstrip('?')
        super(FAQ, self).save(*args, **kwargs)


class Championship(models.Model):
    name = models.CharField(max_length=60, blank=False, unique=True)
    private_mode = models.BooleanField(default=False)
    secret_word = models.CharField(max_length=60, blank=True)
    players = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.name

    def remove_user(self, user):
        self.players.remove(user)

    def add_user(self, user):
        self.players.add(user)

    def move_user(self, user):
        self.add_user(user)
        self.remove_user(user)

    def get_players(self):
        return self.players
