from django.urls import path
from . import views
from .views import chi_siamo_view

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('componenti/', views.componenti_view, name='componenti'),
    path('ordini/', views.ordini_view, name='ordini'),
    path('recensione/', views.recensione_view, name='recensione'),
    path('recensioni/', views.recensioni_view, name='recensioni'),
    path('crea_ordine/', views.crea_ordine_view, name='crea_ordine'),
    path('aziende/', views.aziende_view, name='aziende'),
    path('chi-siamo/', chi_siamo_view, name='chi_siamo'),

    # nuove
    path('scelta-registrazione/', views.scelta_registrazione_view, name='scelta_registrazione'),
    path('register/privato/', views.register_privato_view, name='register_privato'),
    path('register/azienda/', views.register_azienda_view, name='register_azienda'),
    path('profilo/', views.profilo_view, name='profilo'),
    path('logout/', views.logout_view, name='logout'),
    path('giveaway/', views.giveaway_view, name='giveaway'),
]
