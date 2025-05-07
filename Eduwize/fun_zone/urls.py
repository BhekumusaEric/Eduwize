from django.urls import path
from . import views

app_name = 'fun_zone'

urlpatterns = [
    path('hackathons/', views.hackathon_list, name='hackathon_list'),
]