from django.shortcuts import render, redirect
from core.forms import LoginForm
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login
from django.http import HttpResponseRedirect, JsonResponse


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
    return render(request, 'dashboard.html', {})


def logout(request):
    dj_logout(request)
    return HttpResponseRedirect('/')


