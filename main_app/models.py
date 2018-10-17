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
    volunteers = models.ManyToManyField(User)


    def __str__(self):
        return self.what

    # def get_absolute_url(self):
    #     return reverse('events_detail', kwargs={'event_id': self.id})

    def get_absolute_url(self):
       return reverse('profile', kwargs={'id': 1})

    class Meta:
        ordering = ['-date']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['who', 'what', 'where', 'date']
        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'min': f"{date.today()}"}),
        }

class Comment(models.Model):
    content = models.TextField('Comment',max_length=600)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment: {self.content}"

