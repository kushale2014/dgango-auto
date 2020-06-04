from django.shortcuts import render
from mainapp.get_cars import get_cars

PARAMS = {
    'search': ['rst', 'olx', 'autoria'],
    'count_cars': '100',
    'price1': '0',
    'price2': '1200',
    'year1': '1995',
    'year2': '0',
    'photos': '1',
}


def index(request):
    if (request.method == "POST"):
        params = {}
        for key in PARAMS:
            if request.POST.get(key):
                params[key] = request.POST.get(key)
        for key in PARAMS['search']:
            if request.POST.get(key):
                params[key] = request.POST.get(key)
    else:
        params = PARAMS
        for key in PARAMS['search']:
            params[key] = '1'
    print(params)
    return render(request, 'mainapp/index.html', {
        'cars': get_cars(params),
        'params': params,
    })
    # return render(request, 'mainapp/index2.html', {
    #     'params': params,
    # })
