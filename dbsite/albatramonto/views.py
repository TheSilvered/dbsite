from django.shortcuts import render
from .models import OreLuce

def albatramonto_home(request):
    dati = OreLuce.objects.raw("SELECT * FROM albatramonto_oreluce")
    return render(request, 'albatramonto_home.html', {"dati": dati})
