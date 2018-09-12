from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import api_views
from . import views

app_name = 'backend'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup2/$', views.SignUp.as_view(), name='signUp2'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^registrationComplete/autoLogin/$', views.thanks, name='registrationComplete'),
    # url(r'^password_change$', views.password_change, name='password_change'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^battle/$', views.fight, name='fight'),
    url(r'^battle/(?P<player_pk>[0-9]+)/$', views.fight, name='fight'),
    url(r'^testcpu/$', views.versus, name='testcpu'),
    url(r'^versus/(?P<previous>[0-1])/$', views.versus, name='versus'),
    url(r'^versus/(?P<previous>[0-1])/(?P<player_pk>[0-9]+)/$', views.versus, name='versus'),
    url(r'^versus/(?P<previous>[0-1])/(?P<player_pk>[0-9]+)/(?P<script_pk>[0-9]+)/$', views.versus, name='versus'),
    url(r'^replay/$', views.replay, name='replay'),
    url(r'^editor/$', views.AIScriptView.as_view(), name='editor'),
    url(r'^editor/(?P<pk>[0-9]+)/$', views.editorDetail, name='editorDetail'),
    # url(r'^inventory/$', views.inventory, name='inventory'),
    # url(r'^market/$', views.market, name='market'),
    # url(r'^parameter/$', views.parameter, name='parameter'),
    # url(r'^agression/$', views.agression, name='agression'),
    # url(r'^changeStuff/$', views.changeStuff, name='changeStuff'),
    # url(r'^buyStuff/$', views.buyStuff, name='buyStuff'),
    url(r'^help/$', views.help, name='help'),
    url(r'^documentation/$', views.documentation, name='documentation'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^tutoriels/$', views.tutoriel, name='tutoriels'),
    # url(r'^recherche/$', views.recherche, name='recherche'),
    # url(r'^developpement/$', views.developpement, name='developpement'),
    url(r'^battle-histories/$', views.HistoriesView.as_view(), name="battle_histories"),
    url(r'^finish-battle/$', views.finish_battle, name='finish_battle'),
    url(r'^championnat/$', views.CreateChampionship.as_view(), name='championship'),
    url(r'^change_championship/$', views.change_championship, name='change_championship'),
    url(r'^profile/$', views.get_user_profile, name='profile_perso'),
    url(r'^training/$', views.select_player_for_training, name='select_player_for_training'),
    url(r'^championship/$', views.select_player_for_championship, name='select_player_for_championship'),
    url(r'^delete_script/$', views.delete_script, name='delete_script'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
