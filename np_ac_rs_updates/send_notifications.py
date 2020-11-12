from django.conf import settings
from fcm_django.models import FCMDevice
from .models import Student

def send_notification_filter(title, message, tip): 
    try:
        print(tip)
        print(title)
        emailovi = Student.objects.filter(pretplate__icontains=tip).values_list('email', flat=True) #uzmi studente koji medju pretplatama imaju tip vesti koja stize, i njima posalji 
        studenti = Student.objects.filter(pretplate__icontains=tip)

        lista = list(emailovi)

        #filtrira slanje, ako u smerovima studenta ili departmanima ima taj smer/departman za koji je dosla novost, salje mu se

        if tip == "vesti" or tip == "obavestenja" or tip == "instagram":
            devices = FCMDevice.objects.filter(name__in=lista)
            devices.send_message(title=title, body=message, sound=True)

        else:
            for student in studenti:
                smerovi = student.smerovi.split('_')
                departmani = student.departmani.split('_')

                if any(smer in title for smer in smerovi) or any(dep in title for dep in departmani):
                    device = FCMDevice.objects.filter(name=student.email)
                    device.send_message(title=title, body=message, sound=True)
                
            

    except Exception as ex:
        print(ex)


def send_notification_test(title, message):
    devices = FCMDevice.objects.all()
    devices.send_message(title=title, body=message, sound=True)

