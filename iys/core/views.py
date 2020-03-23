from django.shortcuts import render, redirect,get_object_or_404
from core.forms import LoginForm
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login
from django.http import HttpResponseRedirect, JsonResponse
from hasta.models import Hasta
from recete.models import Recete
import datetime
from core.models import Hospital,HospitalUser
from django.contrib.auth.models import User

def login_page(request):

    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            hospitalId = loginForm.cleaned_data['hospital'].id
            the_user = authenticate(username=username, password=password)
            if the_user:
                dj_login(request,the_user)
                request.session.pop('hastaneId',hospitalId)
                request.session['hastaneId'] = hospitalId
                return HttpResponseRedirect('/dashboard')
        else:
            print("LOGIN FORM VALID DEGİLL")
    else:
        loginForm = LoginForm()

    return render(request, 'auth/login.html',{'loginForm':loginForm})


def dashboard(request):
    
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    bugunReceteSayisi = Recete.objects.filter(receteTarihi__range=(today_min, today_max)).count()
    return render(request, 'dashboard.html', {"hastaSayisi":Hasta.objects.count(), 
    "receteSayisi":Recete.objects.count(), "bugunReceteSayisi":bugunReceteSayisi
    , "hastane":get_object_or_404(Hospital, pk=request.session['hastaneId'])})


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect('/')


