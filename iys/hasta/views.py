from django.shortcuts import render,get_object_or_404
from hasta.forms import HastaForm
from hasta.models import Hasta


def hastaList(request):
    return render(request, 'hasta/list.html', {'hastalar':Hasta.objects.all()})


def hastaAdd(request):
    message = None
    info = None
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
    hastaForm = HastaForm()

    return render(request, 'hasta/add.html', {'hastaForm':hastaForm, 'info':info, 'message':message})

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

    return render(request, 'hasta/edit.html', {'id':id,'hastaForm':hastaForm, 'info':info, 'message':message})
