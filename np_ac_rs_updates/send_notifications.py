from django.conf import settings
from fcm_django.models import FCMDevice
from .models import Student

def send_notification_filter(title, message, tip): 
    try:
        emailovi = Student.objects.filter(pretplate__icontains=tip).values_list('email', flat=True) #uzmi studente koji medju pretplatama imaju tip vesti koja stize, i njima posalji 
        studenti = Student.objects.filter(pretplate__icontains=tip)

        lista = list(emailovi)

        if tip == "vesti" or tip == "obavestenja":
            devices = FCMDevice.objects.filter(name__in=lista)
            devices.send_message(title=title, body=message, sound=True)
        else: #filtrira slanje, ako u smerovima studenta ili departmanima ima taj smer/departman za koji je dosla novost, salje mu se
            for student in studenti:
                smerovi = student.smerovi.split()
                departmani = student.departmani.split('-')
            
                print(smerovi)
                print(departmani)

                if any(smer in message for smer in smerovi) or any(dep in message for dep in departmani):
                    device = FCMDevice.objects.filter(name=student.email)
                    device.send_message(title=title, body=message, sound=True)
                
            

    except Exception as ex:
        print(ex)


def send_notification_test(title, message):
    devices = FCMDevice.objects.all()
    devices.send_message(title=title, body=message, sound=True)

