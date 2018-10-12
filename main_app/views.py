from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Event, EventForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import DateInput
from .forms import LoginForm




# Create your views here.

class EventCreate(CreateView):
    model = Event
    success_url = '/events/'
    # widgets = {'date': DateInput(format='%Y-%m-%d', attrs={'type': 'date'})}
    form_class = EventForm

class EventUpdate(UpdateView):
  model = Event
  fields = ['who', 'what', 'where', 'date']

  def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/events/' + str(self.object.pk))


class EventDelete(DeleteView):
  model = Event
  success_url = '/events'


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def events_index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', {'events': events})

def events_detail(request, events_id):
    event = Event.objects.get(id=events_id)
    return render(request, 'events/detail.html', {'event': event})

def login_view(request):
    if request.method == 'POST':
        # if post, then authenticate (user submitted username and password)
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
                    return HttpResponseRedirect('/')
            else:
                print("The username and/or password is incorrect.")
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
   logout(request)
   return HttpResponseRedirect('/')

def signup_view(request):
   if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
           user = form.save()
           login(request, user)
           return redirect('about')
   else:
       form = UserCreationForm()
       return render(request, 'signup.html', {'form': form})

