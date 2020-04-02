from django.shortcuts import render,get_object_or_404
from hasta.forms import HastaForm
from hasta.models import Hasta
from core.models import Hospital, HospitalUser
from django.contrib.auth.models import User


def hastaList(request):

    if (request.user.username == 'erkan' or request.user.username == 'aysel'):
        return render(request, 'hasta/list.html', {'hastalar':Hasta.objects.all()})

    hastaneId = request.session['hastaneId']
    user = request.user
    hastane = Hospital.objects.get(pk=hastaneId)

    hastaneKullanici = HospitalUser.objects.get(authorizedUser=user, hospital=hastane)

    if (hastaneKullanici):
        hastalar = Hasta.objects.filter(servisBilgisi=hastaneKullanici.servis, durumTipi='1')
        return render(request, 'hasta/list.html', {'hastalar':hastalar})
    else:
        return render(request, 'hasta/list.html', {'hastalar':{}})


def hastaAdd(request):
    message = None
    info = None
    hastaForm = HastaForm()
    if (request.POST):
        hastaForm = HastaForm(request.POST)
        if hastaForm.is_valid():
            tc = request.POST['tcNo']
            hasta = Hasta.objects.filter(tcNo=tc)
            if(hasta):
                message = "Bu TC numarası ile daha önce hasta kaydı oluşturulmuş"
            else:
                hastaForm.save()
                info = 'Başarı ile kaydedildi.'
        else:
            print('FORM Valid degil')
    #hastaForm = HastaForm()

    return render(request, 'hasta/add.html', {'form':hastaForm, 'info':info, 'message':message})

def hastaEdit(request, id):
    message = None
    info = None
    if (request.POST):
        hastaModel = get_object_or_404(Hasta,pk=id)
        hastaForm = HastaForm(request.POST or None, instance=hastaModel)
        if hastaForm.is_valid():
            hastaForm.save()
            info = 'Başarı ile güncellendi.'
            
        else:
            message = "Hatalı kayıt! Tekrar deneyiniz."
        hastaForm = HastaForm()
    else:
        hasta = Hasta.objects.get(pk=id)
        hastaForm = HastaForm(instance=hasta)

    return render(request, 'hasta/edit.html', {'id':id,'form':hastaForm, 'info':info, 'message':message})
