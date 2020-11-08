from django.conf import settings
from fcm_django.models import FCMDevice

def send_notification(title, message):
    my_name = "iPhone AleXandar77"
    try:
        device = FCMDevice.objects.filter(name=my_name)
        device.send_message(title=title,body=message,sound=True)
    except:
        pass


