from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register("departman", DepartmanViewSet, basename="Departman")
router.register("predmet", PredmetViewSet, basename="Predmet")
router.register("ispit", IspitniRokViewSet, basename="Ispit")
router.register("prijava", PrijavaViewSet, basename="Prijava")


urlpatterns = [
    path("", include(router.urls)),
    path("uzmi_nove_ispitne_rokove/", uzmi_nove_ispitne_rokove, name='uzmi_nove_ispitne_rokove'),
    path("uzmi_id_poslednjeg_roka/", uzmi_id_poslednjeg_roka, name='uzmi_id_poslednjeg_roka')
]
