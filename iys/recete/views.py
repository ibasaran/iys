from django.urls import reverse
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .models import Recete, ReceteUygulama
from .forms import ReceteFormSet


class ReceteList(ListView):
    model = Recete


class ReceteCreate(CreateView):
    model = Recete
    fields = ['istenenMiktar', 'birimTipi', 'receteTarihi']


class ReceteUygulamaCreate(CreateView):
    template_name='recete/edit.html'
    model = Recete
    fields = ['istenenMiktar', 'birimTipi', 'receteTarihi']
    #success_url = '/'

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
        with transaction.atomic():
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
    fields = ['istenenMiktar', 'birimTipi', 'receteTarihi']
    #success_url = '/'
    template_name='recete/edit.html'

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
    success_url = '/'
