from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
import requests

# Create your models here.

def showCityChoices():
    return (
        ('Mumbai', 'Mumbai'),
        ('Delhi', 'Delhi'),
        ('Bangalore', 'Bangalore'),
        ('Chennai', 'Chennai'),
        ('Kolkata', 'Kolkata'),
    )
class Record(models.Model):
    user_name = models.CharField(max_length = 200, null = True, verbose_name = 'user name')
    email = models.EmailField(null = True)
    city = models.CharField(max_length = 200, null = True, choices = showCityChoices())
    createdAt = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return 'Record for ' + self.user_name

@receiver(post_save, sender=Record)
def sendRecordEmail(sender, instance, created, **kwargs):
    if created:
        # Get latest entry in database and send request using a particular city name
        record = Record.objects.latest('id')
        response = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+record.city+'&appid='+settings.OPEN_WEATHER_API_KEY).json()
        weather_emoji_link = 'http://openweathermap.org/img/wn/'+response['weather'][0]['icon']+'@2x.png'
        
        # Email process, Body in a template called mail_template.html
        email = EmailMessage(
            f"Hi {record.user_name}, interested in our services",
            render_to_string('task/mail_template.html', 
                {
                    'record': record,
                    'weather_emoji_link':weather_emoji_link,
                    'temp' : response['main']['temp'],
                    'pressure' : response['main']['pressure'],
                    'humidity' : response['main']['humidity'],
                }
            ),
            settings.EMAIL_HOST_USER,
            [record.email]
        )
        # To allow emoji using img tag
        email.content_subtype = "html"
        email.fail_silently = False
        email.send()
