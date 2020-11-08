from django.db import models
from django.core.validators import FileExtensionValidator

class Departman(models.Model):
    naziv = models.CharField(max_length=64)

    def __str__(self):
        return f"Departman za {self.naziv}"

class Smer(models.Model):
    naziv = models.CharField(max_length=64)
    departman = models.ForeignKey(Departman, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Smer {self.naziv}"

# Predmet ima samo auto generisani id
class Predmet(models.Model):
    def __str__(self):
        try:
            if len(self.smerpredmet_set.all()) > 0:
                return "Predmet: " + " / ".join([s.naziv_predmeta for s in self.smerpredmet_set.all()]) 
            else:
                return "Novi predmet"
        except:
            return "Nema jos ime"

class SmerPredmet(models.Model):
    smer = models.ForeignKey(Smer, on_delete=models.CASCADE, default=None)
    predmet = models.ForeignKey(Predmet, on_delete=models.CASCADE, default=None)
    # Posto jedan isti predmet na razlicitim smerovima ima razliciti naziv, Predmet je definisan svojim id-ijem
    # a njegovo ime se pamti u tabeli SmerPredmet
    naziv_predmeta = models.CharField(max_length=255)
    godina_studija = models.IntegerField(default=1)

    class Meta:
        unique_together = (("smer", "predmet"))

    def __str__(self):
        try:
            return f"Smer: {self.smer.naziv} <=> Predmet: {self.predmet.__str__()}"
        except Exception as e:
            print(e)
            return "idk"

class IspitniRok(models.Model):
    def putanjaSlike(self, filename):
        return f"{self.predmet.id}/{self.godina}/{self.ispitni_rok}/{filename}"

    predmet = models.ForeignKey(Predmet, on_delete=models.CASCADE, default=None)
    godina = models.IntegerField()
    ispitni_rok = models.CharField(max_length=64)
    slika = models.ImageField(max_length=255, blank=False, null=False, upload_to=putanjaSlike)
    proveren = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.predmet.__str__()} {self.ispitni_rok} {self.godina}"

    
class Prijava(models.Model):

    ispitni_rok = models.ForeignKey(IspitniRok, on_delete=models.CASCADE)
    razlog_prijave = models.CharField(max_length=64)
    dodatak = models.CharField(max_length=512, blank=True)