from django.urls import path
from . import views

urlpatterns = [
    path('azuriraj_bazu/', views.azuriraj_bazu, name='azuriraj_bazu'),
    path('', views.uzmi_novosti, name='uzmi_novosti'),
    path('prijava_studenta/', views.prijava_studenta, name="prijava_studenta"),
    path('izmena_pretplata/', views.izmena_pretplata, name="izmena_pretplata"),
    path('posalji_notifikaciju/', views.posalji_notifikaciju, name="posalji_notifikaciju")
]