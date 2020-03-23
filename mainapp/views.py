from django.shortcuts import render
from mainapp.get_olx import get_cars_olx

def index(request):
    cars = get_cars_olx(100)
    cars0 = [cars[key] for key in range(0, len(cars), 2)]
    cars1 = [cars[key] for key in range(1, len(cars)+1, 2)]
    return render(request, 'mainapp/index.html', {'cars0' : cars0, 'cars1' : cars1})
    