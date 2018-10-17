from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Event, EventForm, Comment
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import DateInput
from .forms import LoginForm, CommentForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User




# Create your views here.
@method_decorator(login_required, name='dispatch')
class EventCreate(CreateView):
    model = Event
    success_url = '/events/'
    # widgets = {'date': DateInput(format='%Y-%m-%d', attrs={'type': 'date'})}
    form_class = EventForm

@method_decorator(login_required, name='dispatch')
class EventUpdate(UpdateView):
  model = Event
  fields = ['who', 'what', 'where', 'date']

  def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/events/' + str(self.object.pk))

@method_decorator(login_required, name='dispatch')
class EventDelete(DeleteView):
  model = Event
  success_url = '/events'

@method_decorator(login_required, name='dispatch')
class CommentUpdate(UpdateView):
    model = Comment
    fields = ['content']
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(f"/events/{self.object.event_id}")

@method_decorator(login_required, name='dispatch')
class CommentDelete(DeleteView):
    model = Comment
    def post(self, request, *args, **kwargs):
        comment = self.get_object()
        event_id = comment.event_id
        comment.delete()
        return redirect(f"/events/{event_id}")
    
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def events_index(request):
    events = Event.objects.all()
    return render(request, 'events/index.html', {'events': events})

def events_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    is_attending = event.volunteers.filter(id=request.user.id).exists()
    comment_form = CommentForm()
    return render(request, 'events/detail.html', {
        'event': event, 'comment_form': comment_form, 'is_attending': is_attending,
    })
    
def profile(request, id):
    profile = User.objects.get(id=id)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def add_comment(request, event_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.user = request.user
        new_comment.event_id = event_id
        new_comment.save()
    return redirect('events_detail', event_id=event_id)

def login_view(request):
    if request.method == 'POST':
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

@login_required
def add_volunteer(request, event_id):
    event = Event.objects.get(id=event_id)
    event.volunteers.add(request.user)
    return redirect(f"/events/{event_id}")

