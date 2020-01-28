from django.urls import reverse
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import render,get_object_or_404
from .models import Recete, ReceteUygulama
from .forms import ReceteFormSet, ReceteForm
import datetime
from core.models import Hospital
from dal import autocomplete
from core.models import Mayi, Ilac
from hasta.models import Hasta
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

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
            self.object.hastane = get_object_or_404(Hospital, pk=self.request.session['hastaneId'])
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
            self.object.hastane = get_object_or_404(Hospital, pk=self.request.session['hastaneId'])
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
    print(request.session['hastaneId'])
    context = {}
    if(request.method == 'POST'):
        receteTarihi = request.POST.get('receteTarihi', '')
        print(receteTarihi)
        hazirlamaListesi = ReceteUygulama.objects.filter(recete__hastane__id=request.session['hastaneId'],recete__receteTarihi=datetime.datetime.strptime(str(receteTarihi), "%Y-%m-%d").date())
        print(hazirlamaListesi.query)
        context['hazirlamaListesi'] = hazirlamaListesi
    else:
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        hazirlamaListesi = ReceteUygulama.objects.filter(recete__hastane__id=request.session['hastaneId'],recete__receteTarihi__range=(today_min, today_max))
        context['hazirlamaListesi'] = hazirlamaListesi
    return render(request, "recete/receteHazirlama.html", context)



class MayiAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Mayi.objects.none()

        qs = Mayi.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class HastaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Mayi.objects.none()

        qs = Hasta.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class IlacAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        #if not self.request.user.is_authenticated():
        #    return Mayi.objects.none()

        qs = Ilac.objects.all()

        if self.q:
            qs = qs.filter(adi__istartswith=self.q)

        return qs



def printRecete(request,id):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Buraya bilgiler gelecek.")

    p.setPageSize((300, 200))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='etiket.pdf')
