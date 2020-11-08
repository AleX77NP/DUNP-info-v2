from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from rest_framework import mixins
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse
from .models import IspitniRok

# custom viewset koji omogucava samo GET, POST i HEAD metode,
# znaci kroisnik moze samo da dobija i postavlja nesto
class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass


class DepartmanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Departman.objects.all()
    serializer_class = DepartmanSerializer

class IspitniRokViewSet(CreateListRetrieveViewSet):
    queryset = IspitniRok.objects.all()
    serializer_class = IspitniRokSerializer

class PredmetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Predmet.objects.all()
    serializer_class = PredmetSerializer

class PrijavaViewSet(CreateListRetrieveViewSet):
    queryset = Prijava.objects.all()
    serializer_class = PrijavaSerializer

# vraca se ispitne rokove pocevsi od onog koji ima latest_id_roka za predmete koji se proslede
# npr. http://localhost:8000/api/faks/uzmi_nove_ispitne_rokove/?latest_id_roka=0&id_predmeta=1&id_predmeta=3
@require_http_methods(["GET"])
def uzmi_nove_ispitne_rokove(request):
    latest_id_roka = request.GET["latest_id_roka"]
    predmeti = request.GET.getlist("id_predmeta")
    result = IspitniRok.objects.filter(id__gt=latest_id_roka, predmet__in=predmeti, proveren=True)

    response = serializers.serialize("json", result)
    return HttpResponse(response)

@require_http_methods(["GET"])
def uzmi_id_poslednjeg_roka(request):
    result = IspitniRok.objects.last().pk
    return HttpResponse(result)
