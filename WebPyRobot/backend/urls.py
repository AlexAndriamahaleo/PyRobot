from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import api_views
from . import views

app_name = 'backend'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.SignUp.as_view(), name='signUp'),
    url(r'^registrationComplete/autoLogin/$', views.thanks, name='registrationComplete'),
    url(r'^password_change$', views.password_change, name='password_change'),
    url(r'^battle/$', views.fight, name='fight'),
    url(r'^battle/(?P<player_pk>[0-9]+)/$', views.fight, name='fight'),
    url(r'^testcpu/$', views.testcpu, name='testcpu'),
    url(r'^versus/$', views.testcpu, name='versus'),
    url(r'^versus/(?P<player_pk>[0-9]+)/$', views.testcpu, name='versus'),
    url(r'^versus/(?P<player_pk>[0-9]+)/(?P<script_pk>[0-9]+)/$', views.testcpu, name='versus'),
    url(r'^replay/$', views.replay, name='replay'),
    url(r'^editor/$', views.AIScriptView.as_view(), name='editor'),
    url(r'^editor/(?P<pk>[0-9]+)/$', views.editorDetail, name='editorDetail'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^market/$', views.market, name='market'),
    url(r'^parameter/$', views.parameter, name='parameter'),
    url(r'^help/$', views.help, name='help'),
    url(r'^agression/$', views.agression, name='agression'),
    url(r'^changeStuff/$', views.changeStuff, name='changeStuff'),
    url(r'^buyStuff/$', views.buyStuff, name='buyStuff'),
    url(r'^documentation/$', views.documentation, name='documentation'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^tutoriels/$', views.tutoriel, name='tutoriels'),

    url(r'^recherche/$', views.recherche, name='recherche'),
    url(r'^developpement/$', views.developpement, name='developpement'),

    url(r'^battle-histories/$', views.HistoriesView.as_view(), name="battle_histories"),
    url(r'^finish-battle/$', views.finish_battle, name='finish_battle'),
    url(r'^championnat/$', views.CreateChampionship.as_view(), name='championship'),
    url(r'^change_championship/$', views.change_championship, name='change_championship')

]
