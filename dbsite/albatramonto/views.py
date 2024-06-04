from django.shortcuts import render
from .models import OreLuce

def albatramonto_home(request):
    if request.GET and "datainizio" in request.GET:
        dati = OreLuce.objects.raw(f'SELECT * FROM albatramonto_oreluce WHERE data >= "{request.GET["datainizio"]}"')
    else:
        dati = OreLuce.objects.raw('SELECT * FROM albatramonto_oreluce')
    return render(request, 'albatramonto_home.html', {"dati": dati})
