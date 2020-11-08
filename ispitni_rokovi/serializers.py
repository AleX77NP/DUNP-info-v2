from .models import *
from rest_framework import serializers

class SmerPredmetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmerPredmet
        fields = "__all__"


class SmerSerializer(serializers.ModelSerializer):
    smerpredmet_set = SmerPredmetSerializer(many=True)
    
    class Meta:
        model = Smer
        fields = ("id", "naziv", "departman", "smerpredmet_set")


class DepartmanSerializer(serializers.ModelSerializer):
    smer_set = SmerSerializer(many=True)
    class Meta:
        model = Departman
        fields = ("id", "naziv", "smer_set")


class IspitniRokSerializer(serializers.ModelSerializer):
    class Meta:
        model = IspitniRok
        fields = "__all__"


class PredmetSerializer(serializers.ModelSerializer):
    ispitnirok_set = IspitniRokSerializer(many=True)
    class Meta:
        model = Predmet
        fields = ("id", "ispitnirok_set")

class PrijavaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prijava
        fields = "__all__"

