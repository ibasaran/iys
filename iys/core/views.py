from django.shortcuts import render, redirect
from core.forms import LoginForm
from django.contrib.auth import authenticate, logout as dj_logout, login as dj_login
from django.http import HttpResponseRedirect, JsonResponse


def login_page(request):

    print("POSTTT")
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            username = loginForm.cleaned_data['username']
            password = loginForm.cleaned_data['password']
            hospitalId = loginForm.cleaned_data['hospital']
            print("Kullanıcı Adı:%s Şifre: %s Hastane ID: %s" % (username, password,hospitalId))
            the_user = authenticate(username=username, password=password)
            if the_user:
                dj_login(request,the_user)
                return HttpResponseRedirect('/dashboard')
        else:
            print("LOGIN FORM VALID DEGİLL")
    else:
        loginForm = LoginForm()

    return render(request, 'auth/login.html',{'loginForm':loginForm})
