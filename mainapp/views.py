from django.shortcuts import render
from mainapp.get_cars import get_cars


def index(request):
    # olx = get_olx(count_cars)
    # autoria = get_autoria(count_cars)
    # rst = get_rst(count_cars)
    params = {
        'count_cars': 100,
        'price2': 1200,
        'year1': 1995,
    }
    return render(request, 'mainapp/index.html', {
        'cars': get_cars(params),
    })
