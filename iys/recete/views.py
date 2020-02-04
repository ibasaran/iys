from django.urls import reverse
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import render,get_object_or_404
from .models import Recete, ReceteUygulama
from core.models import UygulamaSaati
from .forms import ReceteFormSet, ReceteForm
import datetime, string
from core.models import Hospital
from dal import autocomplete
from core.models import Mayi, Ilac
from hasta.models import Hasta
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize
import reportlab
from django.conf import settings

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
            #self.object = form.save()
            self.object.save()
            form.save_m2m()

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
    context = {}

    if(request.method == 'POST'):
        receteTarihi = request.POST.get('receteTarihi', '')
        hazirlamaListesi = Recete.objects.filter(hastane__id=request.session['hastaneId'],receteTarihi=datetime.datetime.strptime(str(receteTarihi), "%Y-%m-%d").date())
        context['hazirlamaListesi'] = hazirlamaListesi
    else:
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        hazirlamaListesi = Recete.objects.filter(hastane__id=request.session['hastaneId'],receteTarihi__range=(today_min, today_max))
        context['hazirlamaListesi'] = hazirlamaListesi
    # if(request.method == 'POST'):
    #     receteTarihi = request.POST.get('receteTarihi', '')
    #     print(receteTarihi)
    #     hazirlamaListesi = ReceteUygulama.objects.filter(recete__hastane__id=request.session['hastaneId'],recete__receteTarihi=datetime.datetime.strptime(str(receteTarihi), "%Y-%m-%d").date())
    #     print(hazirlamaListesi.query)
    #     context['hazirlamaListesi'] = hazirlamaListesi
    # else:
    #     today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    #     today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    #     hazirlamaListesi = ReceteUygulama.objects.filter(recete__hastane__id=request.session['hastaneId'],recete__receteTarihi__range=(today_min, today_max))
    #     context['hazirlamaListesi'] = hazirlamaListesi
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



def printRecete(request,id,sid):

    recete = Recete.objects.get(pk=id)
    uygulama = ReceteUygulama.objects.get(pk=sid)

    hasta_adi = recete.hasta.name
    servis_adi = recete.hasta.servisBilgisi.servisAdi
    tc_no = recete.hasta.tcNo
    ilac_adi = recete.ilac.adi
    hazirlama_yeri = recete.uygulamaYolu.adi
    mayi = recete.mayi.name
    istenenMik = recete.istenenMiktar
    hemsireNotu = recete.hemsireNotu
    cekilecekMl = (recete.ilac.ml / recete.ilac.mg) * istenenMik
    tamamlanacakMiktar = recete.mayi.miktari - cekilecekMl
    toplamHacim = recete.mayi.miktari
    istenenMikBirimTip = recete.birimTipi.name


    reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR))

    PAGE_WIDTH  = 300
    PAGE_HEIGHT = 225
    pdfmetrics.registerFont(TTFont('arial', 'arial.ttf'))
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.setFont("arial", 10)
    p.setPageSize((300, 200))
    
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    hastaneAdi = recete.hastane.name
    hastaneAdi_width = stringWidth(hastaneAdi, "arial", 10)
    pdf_text_object = p.beginText((PAGE_WIDTH - hastaneAdi_width) / 2, 183)
    pdf_text_object.textOut(hastaneAdi)
    p.drawText(pdf_text_object)
    p.line(0,177,300,177)


    p.drawString(5, 160, 'Hasta Adı: ' + str(hasta_adi))
    p.drawString(5, 145, 'Servis Adı: ' + str(servis_adi))
    p.drawString(180, 160, 'T.C. No: ' + str(tc_no))
    p.line(0,140,300,140)

    p.drawString(5, 125, 'İlaç Adı: ' + str(ilac_adi))
    p.drawString(5, 110, 'Hazirma Yeri: ' + str(hazirlama_yeri))
    p.drawString(5, 95, mayi)
    p.drawString(5, 80, 'İstl Mik: ' + str(istenenMik) + ' ' + str(istenenMikBirimTip))
    p.drawString(5, 40, 'Hemşire Notu: ' + '' if hemsireNotu is None else str(hemsireNotu))

    p.drawString(170, 110, 'İstl Mik: ' + str(istenenMik) + ' ' + str(istenenMikBirimTip))
    p.drawString(170, 95, 'Tamln. Mik: ' + str(tamamlanacakMiktar) + ' ML' )
    p.drawString(170, 80, 'Çekilen Mik: ' + str(cekilecekMl) + ' ML' )
    p.line(165,75,280,75)
    p.drawString(165, 60, 'Tpl Hacim: ' + str(toplamHacim) + ' ML')

    p.line(0,30,300,30)

    p.drawString(5, 15, 'Hazırlama Tarihi: ' + str(recete.receteTarihi.day) + '/' + str(recete.receteTarihi.month)+ '/' + str(recete.receteTarihi.year))
    p.drawString(150,15,'Hazırlayan: ' + request.user.username)


    #.drawString(50, 10, recete.hastane.name)

    

    #textsize(p)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='etiket.pdf',content_type='application/pdf')


def textsize(canvas):
    lyrics = '''\
    well she hit Net Solutions
    and she registered her own .com site now
    and filled it up with yahoo profile pics
    she snarfed in one night now
    and she made 50 million when Hugh Hefner
    bought up the rights now
    and she'll have fun fun fun
    til her Daddy takes the keyboard away'''

    lyrics = str.split(lyrics, "\n")
    from reportlab.lib.units import inch
    from reportlab.lib.colors import magenta, red
    canvas.setFont("Times-Roman", 20)
    canvas.setFillColor(red)
    canvas.drawCentredString(2.75*inch, 2.5*inch, "Font size examples")
    canvas.setFillColor(magenta)
    size = 7
    y = 2.3*inch
    x = 1.3*inch
    for line in lyrics:
        canvas.setFont("Helvetica", size)
        canvas.drawRightString(x,y,"%s points: " % size)
        canvas.drawString(x,y, line)
        y = y-size*1.2
        size = size+1.5