from django.shortcuts import render
from django.template import loader
t = loader.get_template('mainapp/index.html')
c = cars
t.render(cars)
