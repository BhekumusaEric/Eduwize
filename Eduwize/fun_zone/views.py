from django.shortcuts import render
from .models import Hackathon

def hackathon_list(request):
    hackathons = Hackathon.objects.all()
    return render(request, 'fun_zone/hackathon_list.html', {'hackathons': hackathons})