from django.shortcuts import render
from main import models
# Create your views here.
def index(request):
    return render(request, 'index.html')