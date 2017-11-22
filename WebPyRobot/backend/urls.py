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
    url(r'^combat/$', views.fight, name='fight'),
    url(r'^editor/$', views.AIScriptView.as_view(), name='editor'),
    url(r'^editor/(?P<pk>[0-9]+)/$', views.editorDetail, name='editorDetail'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^market/$', views.market, name='market'),
    url(r'^parameter/$', views.parameter, name='parameter'),
    url(r'^help/$', views.help, name='help'),
    url(r'^agression/$', views.agression, name='agression'),
    url(r'^changeStuff/$', views.changeStuff, name='changeStuff'),
    url(r'^buyStuff/$', views.buyStuff, name='buyStuff'),
    #url(r'^documentation/$', views.documentation, name='documentation'),
    url(r'^documentation/$', views.documentation, name='documentation'),
    url(r'^tutoriels/$', views.tutoriel, name='tutoriels'),

    url(r'^recherche/$', views.recherche, name='recherche'),
    url(r'^developpement/$', views.developpement, name='developpement'),

    url(r'^dragonball-chars/$', api_views.angular_ajax_test, name="test_api"),

    url(r'^battle-histories/$', views.HistoriesView.as_view(), name="battle_histories")

]
