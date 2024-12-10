from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')
def auto(request):
    return render(request, 'auto.html')
def promotion(request):
    return render(request, 'promotion.html')
def contacts(request):
    return render(request, 'contacts.html')
def workconditions(request):
    return render(request, 'workconditions.html')
