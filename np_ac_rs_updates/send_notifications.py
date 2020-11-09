from django.conf import settings
from fcm_django.models import FCMDevice
from .models import Student

def send_notification_filter(title, message, tip): #ovde jos da se filtrira po departmanima i smerovima
    try:

        emailovi = Student.objects.filter(pretplate__icontains=tip).values_list('email', flat=True) #uzmi studente koji medju pretplatama imaju tip vesti koja stize, i njima posalji 
        lista = list(emailovi)

        devices = FCMDevice.objects.filter(name__in=lista)
        devices.send_message(title=title, body=message, sound=True)
    except:
        pass


def send_notification_test(title, message):
    devices = FCMDevice.objects.all()
    devices.send_message(title=title, body=message, sound=True)

