from django.shortcuts import render
from mainapp.get_cars import get_olx, get_autoria, get_rst

count_cars = 100


def index(request):
    olx = get_olx(count_cars)
    autoria = get_autoria(count_cars)
    rst = get_rst(count_cars)
    return render(request, 'mainapp/index.html', {
        'olx': olx,
        'autoria': autoria,
        'rst': rst,
    })
