from django.contrib import admin
from .models import Novost, Student

class NovostAdmin(admin.ModelAdmin):
    list_display = ("id", "tip", "naslov", "datum", )
    list_filter = ("tip",)
    search_fields = ("id", "tip", "naslov", "datum", "opis", "link", )

class StudentAdmin(admin.ModelAdmin):
     list_display = ("email", "lozinka", "fcm_token", "pretplate", )

# Register your models here.
admin.site.register(Novost, NovostAdmin)
admin.site.register(Student, StudentAdmin)