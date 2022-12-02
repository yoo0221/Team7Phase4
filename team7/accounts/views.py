from django.shortcuts import render, redirect

# Create your views here.
def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def create_user(request):
    id = request.POST['username']
    password = request.POST['username']
    first_name = request.POST['username']
    last_name = request.POST['username']
    sex = request.POST['sex']
    return redirect('index')