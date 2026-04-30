from django.shortcuts import render, redirect
from .forms import FarmerRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request,'home.html')


def register(request):

    if request.method == 'POST':

        form = FarmerRegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:
        form = FarmerRegistrationForm()

    return render(request,'register.html',{'form':form})


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        else:

            return render(request,"login.html",{"error":"Invalid username or password"})

    return render(request,"login.html")

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('/login/') 