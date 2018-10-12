from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('events/<int:events_id>', views.events_detail, name='events_detail'),
    path('events/', views.events_index, name='events_index'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
]