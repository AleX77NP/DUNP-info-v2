from django.shortcuts import render
from .popuni_bazu import popuni_bazu
from django.http import HttpResponse
import json
from django.views.decorators.http import require_http_methods
from .models import Novost, Student
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from .send_notifications import send_notification_test, send_notification_filter

def azuriraj_bazu(request):
    try:
        sta_je_dodato_u_bazu = popuni_bazu()
        return HttpResponse("Uspesno azurirana baza podataka! Novosti koje su dodate u bazu: " + json.dumps(sta_je_dodato_u_bazu, indent=4))
    except Exception as e:
        return HttpResponse(f"Greska prilikom azuriranja baze: {e}")

# npr. http://localhost:8000/api/novosti/?latest_id=0&tip=obavestenja&tip=vesti&tip=obavestenja_smera-Racunarska_tehnika&tip=raspored_ispita-Softversko_inzenjerstvo&tip=raspored_ispita-Matematika&tip=termini_konsultacija-DEPARTMAN_ZA_FILOLOSKE_NAUKE
@require_http_methods(["GET"])
def uzmi_novosti(request):
    latest_id = request.GET["latest_id"]
    tipovi = request.GET.getlist("tip")
    temp = Novost.objects.filter(id__gt = latest_id)
    result = []

    for zahtev in tipovi:
        zahtev = zahtev.replace("_", " ")
        delovi = zahtev.split("-")
        if len(delovi) == 1:
            # print(f"Daj mi sve sto pripada tipu {delovi[0]}")
            result.extend(temp.filter(tip=delovi[0]))
        elif len(delovi) == 2:
            # print(f"Daj mi {delovi[0]} za departman/smer {delovi[1]}")
            result.extend(temp.filter(tip=delovi[0], naslov__contains=delovi[1]))
    # Izbaci duplikate iz liste
    result = list(dict.fromkeys(result)) 
    # Sortiraj listu u opadajucem redosledu po id-u u bazi, tj. po pk-u (primary key)
    result = sorted(result, key=lambda k: k.datum, reverse=True)

    response = serializers.serialize("json", result)
    return HttpResponse(response)


# kada korisnik instalira aplikaciju i unese moodle podatke, odabrane departmane, pretplate i vesti, cuva se i fcm token iz firebase-a
@csrf_exempt
@require_http_methods(["POST","PUT"])
def prijava_studenta(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        lozinka = make_password(data.get('lozinka'))
        fcm_token = data.get('fcm_token')
        pretplate = data.get('pretplate')
        smerovi_departmani = data.get('smerovi')
        departmani = data.get('departmani')

        novi = {
            "lozinka": lozinka,
            "fcm_token": fcm_token,
            "pretplate": pretplate,
            "smerovi": smerovi,
            "departmani": departmani
        }
        student, created = Student.objects.update_or_create(email=email,defaults=novi)
        return HttpResponse("Uspeh pri prijavi.")

    except Exception as e:
        print(e)
        return HttpResponse("Neuspeh pri prijavi.")
    

@csrf_exempt
@require_http_methods(["PUT"]) #metoda za izmenu pretplata na serveru, poziva se kada korisnik na frontendu promeni pretplate
def izmena_pretplata(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        pretplate = data.get('pretplate')
        smerovi = data.get('smerovi')
        departmani = data.get('departmani')
        if len(Student.objects.filter(email=email)) == 0:
            return HttpResponse("Student ne postoji u bazi.")
        else:
            Student.objects.filter(email=email).update(pretplate=pretplate, smerovi=smerovi, departmani=departmani)
            return HttpResponse("Uspeh pri izmeni pretplata.")

    except Exception as e:
        print(e)
        return HttpResponse("Neuspeh pri promeni pretplata." + e)


@csrf_exempt
@require_http_methods(["POST"]) #metoda za probu notifikacije
def posalji_notifikaciju(request):
    try:
        data = json.loads(request.body)
        title = data.get('title')
        message = data.get('message')

        send_notification(title,message)
        return HttpResponse("Poslana notifikacija")
    except:
        return HttpResponse("Neuspeh")


