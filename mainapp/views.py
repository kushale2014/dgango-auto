from django.shortcuts import render
from mainapp.get_olx import get_cars_olx

def index(request):
    cars = get_cars_olx()
    return render(request, 'mainapp/index.html', {'cars' : cars})
    # return render(request, 'index.html', {'all_cars':all_cars})

