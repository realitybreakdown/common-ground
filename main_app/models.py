from django.db import models
from django.urls import reverse
from datetime import date 
from django.contrib.auth.models import User
from django import forms


# Create your models here.

class Event(models.Model):
    who = models.CharField(max_length=100)
    what = models.TextField(max_length=600)
    where = models.CharField(max_length=250)
    date = models.DateField('Event date')

    def __str__(self):
        return self.who

    # def get_absolute_url(self):
    #     return reverse('events_detail', kwargs={'events_id': self.id})

    class Meta:
        ordering = ['-date']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
