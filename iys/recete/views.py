from django.urls import reverse
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import render
from .models import Recete, ReceteUygulama
from .forms import ReceteFormSet, ReceteForm
import datetime

class ReceteList(ListView):
    model = Recete
    template_name = 'recete/list.html'


class ReceteCreate(CreateView):
    model = Recete
    fields = ['istenenMiktar', 'birimTipi', 'receteTarihi']


class ReceteUygulamaCreate(CreateView):
    template_name='recete/edit.html'
    model = Recete
    form_class = ReceteForm

    def get_initial(self):
        print('getting initial')
        print(self.request.session['hastaneId'])
        return {
            'hastane_id':self.request.session['hastaneId'],
        }

    def get_success_url(self):
        return reverse('recete:recete-update', kwargs={'pk' : self.object.pk})

    def get_context_data(self, **kwargs):
        data = super(ReceteUygulamaCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['receteuygulamas'] = ReceteFormSet(self.request.POST)
        else:
            data['receteuygulamas'] = ReceteFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        receteuygulamas = context['receteuygulamas']
        #self.object.hastane.id = self.request.session['hastaneId']
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.hastane_id = self.request.session['hastaneId']
            self.object = form.save()

            if receteuygulamas.is_valid():
                receteuygulamas.instance = self.object
                receteuygulamas.save()
        return super(ReceteUygulamaCreate, self).form_valid(form)


class ReceteUpdate(UpdateView):
    model = Recete
    success_url = '/'
    fields = ['istenenMiktar', 'birimTipi', 'receteTarihi']


class ReceteUygulamaUpdate(UpdateView):
    model = Recete
    #success_url = '/'
    template_name='recete/edit.html'
    form_class = ReceteForm

    def get_success_url(self):
        return reverse('recete:recete-update', kwargs={'pk' : self.object.pk})


    def get_context_data(self, **kwargs):
        data = super(ReceteUygulamaUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['receteuygulamas'] = ReceteFormSet(self.request.POST, instance=self.object)
        else:
            data['receteuygulamas'] = ReceteFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        receteuygulamas = context['receteuygulamas']
        with transaction.atomic():
            self.object = form.save()

            if receteuygulamas.is_valid():
                receteuygulamas.instance = self.object
                receteuygulamas.save()
        return super(ReceteUygulamaUpdate, self).form_valid(form)


class ReceteDelete(DeleteView):
    model = Recete
    #success_url = '/'

    def get_success_url(self):
        return reverse('recete:recete-list')




def hazirlamaList(request):

    context = {}
    if(request.method == 'POST'):
        receteTarihi = request.POST.get('receteTarihi', '')
        print(receteTarihi)
        hazirlamaListesi = ReceteUygulama.objects.filter(recete__hastane__id=request.session['hastaneId'],recete__receteTarihi=datetime.datetime.strptime(str(receteTarihi), "%Y-%m-%d").date())
        
        context['hazirlamaListesi'] = hazirlamaListesi

    
    return render(request, "recete/receteHazirlama.html", context)
