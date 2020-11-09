from django.db import models

# Create your models here.
class Novost(models.Model):
    # id(se podrazumeva), tip, naslov, opis, link, datum, hash
    tip = models.CharField(max_length=50)
    naslov = models.CharField(max_length=8192)
    opis = models.CharField(max_length=8192)
    link = models.CharField(max_length=255)
    hash_value = models.CharField(max_length=64, default="", blank=True)
    datum = models.DateTimeField() 

    def __str__(self):
        return f"ID: {self.id} *** {self.tip} *** {self.naslov}"


class Student(models.Model):
    email = models.EmailField(max_length=50)
    lozinka = models.CharField(max_length=255)
    fcm_token = models.CharField(blank=False, max_length=255) 
    pretplate = models.TextField(default="", null=False)
    smerovi = models.TextField(default="", null=False)
    departmani = models.TextField(default="", null=False)
