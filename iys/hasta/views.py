from django.shortcuts import render
from hasta.forms import HastaForm
from hasta.models import Hasta


def hastaList(request):
    return render(request, 'hasta/list.html', {'hastalar':Hasta.objects.all()})


def hastaEdit(request):

    if (request.POST):
        hastaForm = HastaForm(request.POST)
        if hastaForm.is_valid():
            hastaForm.save()

    else:
        hastaForm = HastaForm()

    return render(request, 'hasta/edit.html', {'hastaForm':hastaForm})
