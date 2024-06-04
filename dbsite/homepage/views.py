from django.shortcuts import render

def main_home(request):
    return render(request, "homepage_home.html")
