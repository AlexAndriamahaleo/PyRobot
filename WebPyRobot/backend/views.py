import json
import random

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import logout as system_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from channels import Group
from pure_pagination.mixins import PaginationMixin
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .constants import NotificationMessage
from .forms import SignUpForm, ChangeDataForm, CodeForm
from .funct.funct import getItemByType,getBoolInventory
from .game.Game import Game
from .models import Weapon, Armor, Caterpillar, NavSystem, TypeItem, Inventory, DefaultIa
from .models import UserProfile, Tank, Ia, BattleHistory, Notification




def index(request):
    if request.user.is_authenticated:
        context = {'money' : UserProfile.objects.get(user=request.user).money,
                   'username' : request.user,
                   'pageIn' : 'accueil' ,
                   'agression': UserProfile.objects.get(user=request.user).agression,
                   'tank': Tank.objects.get(owner=UserProfile.objects.get(user=request.user))}
        return render(request, "backend/accueil.html", context)
    else:
        form = SignUpForm()
        context = { 'form' : form }
        return render(request, "backend/index.html",context)


@never_cache
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('backend:index'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            from django.contrib.auth import login
            login(request, user)
            urlnext = request.POST.get('next', reverse('backend:index'))
            return redirect(urlnext)
        else:
            form = SignUpForm()
            context = {
                'form': form,
                'next': request.GET.get('next'),
                'error': 'Votre Pseudo et/ou votre mot de passe ne corresponde pas, veuillez réessayer. Merci'
            }
            return render(request, 'backend/index.html', context)
    return render(request, 'backend/index.html',  {'next': request.GET.get('next')})


@never_cache
def logout(request):
    system_logout(request)
    return redirect(reverse('backend:index'))


class SignUp (FormView):
    template_name = 'backend/index.html'
    form_class = SignUpForm

    def get_success_url(self):

        self.success_url = reverse('backend:registrationComplete')

        return super().get_success_url()

    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = User.objects.create_user(username, email, password)

            #create User
            UserProfile(user=user, money=0).save()

            #create ia file default
            userProfile = UserProfile.objects.get(user=user)
            i = Ia.objects.create(owner=userProfile, name=username+"\'s Ia", text=DefaultIa.objects.get(pk=1).text)

            #default Inventory
            Inventory.objects.create(owner=userProfile, item=1, typeItem=TypeItem(pk=1))
            Inventory.objects.create(owner=userProfile, item=1, typeItem=TypeItem(pk=2))
            Inventory.objects.create(owner=userProfile, item=1, typeItem=TypeItem(pk=3))
            Inventory.objects.create(owner=userProfile, item=1, typeItem=TypeItem(pk=4))

            #init tank
            w = getItemByType(1,TypeItem(pk=1))
            a = getItemByType(1,TypeItem(pk=2))
            c = getItemByType(1,TypeItem(pk=3))
            n = getItemByType(1,TypeItem(pk=4))
            Tank.objects.create(owner=userProfile, ia=i,weapon=w,armor=a,caterpillar=c,navSystem=n)


            from django.contrib.auth import authenticate
            user = authenticate(username=username, password=password)

            from django.contrib.auth import login
            login(self.request, user)

            return super(SignUp, self).form_valid(form)

        return super(SignUp, self).form_invalid(form)


def thanks(request):
    return index(request)


@login_required
def fight(request):
    print ("Start ....")
    user1 = UserProfile.objects.get(user=request.user)
    users = UserProfile.objects.exclude(pk=user1.pk)
    user2 = random.choice(list(users))

    notify = NotificationMessage()
    notify.msg_content = "%s vient de démarrer un combat contre toi" % user1.user.username
    print (notify.dumps())
    Group(user2.user.username + '-notifications').send(
        {'text': notify.dumps()})

    Notification.objects.create(user=user1.user, content="Vous démarrer un combat face à %s" % user2.user.username,
                                is_read=True)
    Notification.objects.create(user=user2.user,
                                content="%s vient de démarrer un combat contre toi" % user1.user.username)
    tank1 = Tank.objects.get(owner=user1)
    tank2 = Tank.objects.get(owner=user2)
    ia1 = Ia.objects.get(owner=user1)
    ia2 = Ia.objects.get(owner=user2)
    game = Game(tank1, tank2, ia1, ia2)
    res = game.run(0)

    if game.is_victorious():
        user1.money = user1.money + 500
        user1.exp = 0 #user1.exp + 5
        user1.srch = 0 #user1.srch + 10
        user1.save()
        user2.money = user2.money + 100
        user2.exp = 0 #user2.exp + 1
        user2.save()
    else:
        user2.money = user2.money + 500
        user2.exp = 0 #user2.exp + 5
        user2.srch = 0 # user2.srch + 10
        user2.save()
        user1.money = user1.money + 100
        user1.exp = 0 #user1.exp + 1
        user1.save()


    context = {
        'result': res,
        'pageIn': 'accueil',
        'component': user2.user.username
    }
    return render(request, "backend/fight.html", context)


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        print("ICI")
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            context = {'money': UserProfile.objects.get(user=request.user).money,
                       'username': request.user,
                       'pageIn': 'accueil',
                       'returnChange': "Les Informations ont bien été enregistré"}
            return render(request, "backend/accueil.html", context)
        else:
            context = {'money': UserProfile.objects.get(user=request.user).money,
                       'username': request.user,
                       'pageIn': 'accueil',
                       'returnChange': "Erreur"}
            return render(request, "backend/accueil.html", context)

@login_required
def editor(request):
    userprofile = UserProfile.objects.get(user=request.user)
    ia = Ia.objects.get(owner=userprofile)
    if request.method == 'POST':
        code_form = CodeForm(request.POST)
        if code_form.is_valid():
            useria = code_form.cleaned_data['ia']
            ia.text = useria
            ia.save()

    context = {
        'money': UserProfile.objects.get(user=request.user).money,
        'username': request.user,
        'pageIn': 'editor',
        'code': ia.text,
        'name': request.user
    }
    return render(request, 'backend/editeur.html', context)

@login_required
def createscript(request):

    #create ia file default
    #userProfile = UserProfile.objects.get(user=user)
    #i = Ia.objects.create(owner=userProfile, name=username + "\'s Ia", text=DefaultIa.objects.get(pk=1).text)

    #from .forms import CodeForm
    #userprofile = UserProfile.objects.get(user=request.user)

    # create ia file default
    userProfile = UserProfile.objects.get(user=request.user)

    ia = Ia.objects.create(owner=userProfile, name=request.user+ "\'s Ia", text=DefaultIa.objects.get(pk=1).text)
    ia.save()

    #ia = Ia.objects.get(owner=userProfile)

    #ia.text = DefaultIa.objects.all()
    #ia.save()

    context = {
        'money': UserProfile.objects.get(user=request.user).money,
        'username': request.user,
        'pageIn': 'editor',
        'code': ia.text,
        'name': request.user
    }

    return render(request, 'backend/editeur.html', context)

@login_required
def editorDetail(request, pk):
    return HttpResponse('page de l editor pour ' + pk)


@login_required
def market(request):
    currentUser = UserProfile.objects.get(user=request.user)

    context = {'money' : currentUser.money,
               'username' : request.user,
               'pageIn': 'market',
               'weapons': Weapon.objects.all(),
               'armors': Armor.objects.all(),
               'caterpillars': Caterpillar.objects.all(),
               'navSys': NavSystem.objects.all(),
               }
    return render(request, 'backend/boutique.html',context)

@login_required
def inventory(request):
    inventory = UserProfile.objects.get(user=request.user).__getInventory__()
    weapon = inventory [0]
    armor = inventory [1]
    caterpillar = inventory [2]
    navSys = inventory [3]
    context = {'money' : UserProfile.objects.get(user=request.user).money,
               'username' : request.user,
               'pageIn': 'inventory',
               'weaponInv': weapon,
               'armorInv': armor,
               'caterInv': caterpillar,
               'navInv': navSys,
               'tank': Tank.objects.get(owner=UserProfile.objects.get(user=request.user))
               }
    return render(request, 'backend/inventaire.html',context)

@login_required
def parameter(request):

    form = ChangeDataForm()
    form.fields['email'].initial = request.user.email
    form.fields['username'].initial= request.user.username
    context = {'money' : UserProfile.objects.get(user=request.user).money,
               'username' : request.user,
               'form': form}
    return render(request, 'backend/parameter.html',context)

@login_required
def help(request):
    context = {'money' : UserProfile.objects.get(user=request.user).money,
               'username' : request.user,
               'pageIn': 'help'}
    return render(request, 'backend/aide.html',context)

@login_required
def agression(request):
    userProfile = UserProfile.objects.get(user=request.user)
    agressionValue = userProfile.agression
    userProfile.agression = not agressionValue
    userProfile.save()
    return redirect(reverse('backend:index'))

@login_required
def changeStuff(request):
    userProfile = UserProfile.objects.get(user=request.user)
    tank = Tank.objects.get(owner=userProfile)
    itemIn = request.POST.get("item")
    typeIn = request.POST.get("typeItem")
    if int(typeIn) == 1:
        w = getItemByType(itemIn, TypeItem(pk=1))
        tank.weapon = w
        tank.save()
    elif int(typeIn) == 2:
        a = getItemByType(itemIn, TypeItem(pk=2))
        tank.armor = a
        tank.save()
    elif int(typeIn) == 3:
        c = getItemByType(itemIn, TypeItem(pk=3))
        tank.caterpillar = c
        tank.save()
    elif int(typeIn) == 4:
        n = getItemByType(itemIn, TypeItem(pk=4))
        tank.navSystem = n
        tank.save()
    return redirect(reverse('backend:inventory'))

@login_required
def buyStuff (request):
    user = UserProfile.objects.get(user=request.user)
    itemIn = int(request.POST.get("item"))
    typeIn = int(request.POST.get("typeItem"))
    price = int(request.POST.get("price"))

    boolTab = getBoolInventory(user)

    if boolTab[typeIn-1][itemIn-1]:
        context = {'money': UserProfile.objects.get(user=request.user).money,
                   'username': request.user,
                   'pageIn': 'market',
                   'weapons': Weapon.objects.all(),
                   'armors': Armor.objects.all(),
                   'caterpillars': Caterpillar.objects.all(),
                   'navSys': NavSystem.objects.all(),
                   "return": "Item déjà acheter "
                   }
        return render(request, 'backend/boutique.html', context)
    elif price > user.money :
        context = {'money': UserProfile.objects.get(user=request.user).money,
                   'username': request.user,
                   'pageIn': 'market',
                   'weapons': Weapon.objects.all(),
                   'armors': Armor.objects.all(),
                   'caterpillars': Caterpillar.objects.all(),
                   'navSys': NavSystem.objects.all(),
                   "return": "Pas assez d'argent"
                   }
        return render(request, 'backend/boutique.html', context)
    else :
        user.money = user.money - price
        user.save()
        Inventory.objects.create(owner=user,item=itemIn,typeItem=TypeItem(pk=typeIn))
        context = {'money': UserProfile.objects.get(user=request.user).money,
                   'username': request.user,
                   'pageIn': 'market',
                   'weapons': Weapon.objects.all(),
                   'armors': Armor.objects.all(),
                   'caterpillars': Caterpillar.objects.all(),
                   'navSys': NavSystem.objects.all(),
                   "return": "Achat effectué"
                   }
        return render(request, 'backend/boutique.html', context)

@login_required
def documentation (request):
    context = {
        'pageIn': 'documentation',
    }
    return render (request,"backend/documentation.html", context)

@login_required
def tutoriel (request):
    context = {
        'pageIn': 'tutoriels',
    }
    return render(request,"backend/tutorial.html", context)

@login_required
def recherche(request):
    context = {
        'pageIn': 'recherche',
    }
    return render(request,"backend/research.html", context)

@login_required
def developpement (request):
    context = {
        'pageIn': 'developpement',
    }
    return render(request,"backend/developpement.html", context)


class HistoriesView(LoginRequiredMixin, PaginationMixin, ListView):
    template_name = "backend/histories.html"
    model = BattleHistory
    paginate_by = 10

    def get_queryset(self):
        queryset = BattleHistory.objects.filter(Q(user=self.request.user) | Q(opponent=self.request.user))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HistoriesView, self).get_context_data(**kwargs)
        context['pageIn'] = 'battle_histories'
        return context


class AIScriptView(LoginRequiredMixin, ListView):
    template_name = "backend/editeur.html"
    model = Ia

    def get_context_data(self, **kwargs):
        context = super(AIScriptView, self).get_context_data(**kwargs)
        context['scripts'] = self.request.user.userprofile.ia_set.all()
        context['pageIn'] = 'editor'

        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)