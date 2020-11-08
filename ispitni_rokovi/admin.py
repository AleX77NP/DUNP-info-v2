from django.contrib import admin
from .models import *

class DepartmanAdmin(admin.ModelAdmin):
    list_display = ("naziv", "id")
    search_fields = ("naziv", "id")


class SmerAdmin(admin.ModelAdmin):
    list_display = ("id", "naziv", "departman")
    list_filter = ("departman",)
    search_fields = ("id", "naziv", "departman")


class PredmetAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id')
    search_fields = ('id', 'smerpredmet__naziv_predmeta')


class SmerPredmetAdmin(admin.ModelAdmin):
    list_display = ("id", "smer", "naziv_predmeta", "godina_studija")
    search_fields = ('id', 'smer__naziv', "naziv_predmeta", "godina_studija")
    list_filter = ('smer', "godina_studija" )


class IspitniRokAdmin(admin.ModelAdmin):
    list_display = ("predmet", "id", "godina", "ispitni_rok", "slika", "proveren")
    list_filter = ('proveren', 'godina', "ispitni_rok" )
    search_fields = ('id', 'predmet__id', "godina", "ispitni_rok", "slika")
    list_editable = ("proveren", )


class PrijavaAdmin(admin.ModelAdmin):
    list_display = ("id", "ispitni_rok", "razlog_prijave", "dodatak")
    search_fields = ("id", "razlog_prijave", "dodatak")


admin.site.register(Departman, DepartmanAdmin)
admin.site.register(Smer, SmerAdmin)
admin.site.register(Predmet, PredmetAdmin)
admin.site.register(SmerPredmet, SmerPredmetAdmin)
admin.site.register(IspitniRok, IspitniRokAdmin)
admin.site.register(Prijava, PrijavaAdmin)
