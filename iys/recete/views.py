from django.urls import reverse
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import render,get_object_or_404, redirect
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
from core.models import Hospital, HospitalUser
from django.utils import timezone
from django.db.models import Q
from datetime import timedelta
from django import forms
from django.forms.utils import ErrorList

class ReceteList(ListView):
    model = Recete
    template_name = 'recete/list.html'

    def get_queryset(self):
        user = self.request.user
        # 0 : today 1: yesterday 2:all
        try:
            showIndex = self.kwargs['type']
        except:
            showIndex = 2

        if user.username == 'erkan' or user.username == 'aysel' or user.username=='ismail'or user.username == 'admin':
            if showIndex == '0':
                return Recete.objects.all().order_by('-created_at')
            elif showIndex == '1':
                yesterday_min = datetime.datetime.combine(datetime.date.today() - timedelta(days = 1), datetime.time.min)
                yesterday_max = datetime.datetime.combine(datetime.date.today() - timedelta(days = 1), datetime.time.max)
                return Recete.objects.filter(receteTarihi__range=(yesterday_min,yesterday_max)).order_by('-created_at')
            else:
                today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
                return Recete.objects.filter(receteTarihi__range=(today_min,today_max)).order_by('-created_at')
        # elif user.username == 'admin':
        #     if showIndex == '0':
        #         return Recete.objects.all()
        #     elif showIndex == '1':
        #         yesterday_min = datetime.datetime.combine(datetime.date.today() - timedelta(days = 1), datetime.time.min)
        #         yesterday_max = datetime.datetime.combine(datetime.date.today() - timedelta(days = 1), datetime.time.max)
        #         return Recete.objects.filter(receteTarihi__range=(yesterday_min,yesterday_max))
        #     else:
        #         today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        #         today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        #         return Recete.objects.filter(receteTarihi__range=(today_min,today_max))
        else:
            hastaneId = self.request.session['hastaneId']
            hastane = Hospital.objects.get(pk=hastaneId)
            hastaneKullanici = HospitalUser.objects.get(authorizedUser=user, hospital=hastane)

            if showIndex == '0':
                return Recete.objects.filter(hasta__servisBilgisi=hastaneKullanici.servis,hasta__durumTipi__name='AKTİF').order_by('-created_at')
            elif showIndex == '1':
                yesterday_min = datetime.datetime.combine(datetime.date.today() - timedelta(days = 1), datetime.time.min)
                yesterday_max = datetime.datetime.combine(datetime.date.today() - timedelta(days = 1), datetime.time.max)
                return Recete.objects.filter(hasta__servisBilgisi=hastaneKullanici.servis, receteTarihi__range=(yesterday_min,yesterday_max),hasta__durumTipi__name='AKTİF').order_by('-created_at')
            else:
                today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
                return Recete.objects.filter(hasta__servisBilgisi=hastaneKullanici.servis, receteTarihi__range=(today_min,today_max),hasta__durumTipi__name='AKTİF').order_by('-created_at')


class ReceteCreate(CreateView):
    model = Recete
    fields = ['istenenMiktar', 'birimTipi', 'receteTarihi']


class ReceteUygulamaCreate(CreateView):
    template_name='recete/edit.html'
    model = Recete
    form_class = ReceteForm

    def get_initial(self):
        super(ReceteUygulamaCreate, self).get_initial()
        if (self.kwargs['hpk'] != '0'):
            if 'tekrar' in self.kwargs['hpk']:
                hpk = self.kwargs['hpk']
                hpk = hpk.replace('tekrar', '')
                recete = get_object_or_404(Recete, pk=hpk)
                if (recete):
                    return {
                        'hastane_id':self.request.session['hastaneId'],
                        'hasta': recete.hasta.id,
                        'ilac': recete.ilac,
                        'mayi': recete.mayi,
                        'istenenMiktar': recete.istenenMiktar,
                        'birimTipi': recete.birimTipi,
                        'dolumTipi': recete.dolumTipi,
                        'hemsireNotu': recete.hemsireNotu,
                        'uygulamaYolu': recete.uygulamaYolu,
                        'uygulamaSaati':recete.uygulamaSaati.all()
                    }
            else:
                recete = get_object_or_404(Recete, pk=self.kwargs['hpk'])
                if (recete):
                    return {
                        'hastane_id':self.request.session['hastaneId'],
                        'hasta': recete.hasta.id,
                        'receteTarihi' : recete.receteTarihi
                    }
        else: 
            return {
                'hastane_id':self.request.session['hastaneId'],
            }

    def get_success_url(self):
        return reverse('recete:recete-update', kwargs={'pk' : self.object.pk, 'isCreate':1})

    def get_context_data(self, **kwargs):
        data = super(ReceteUygulamaCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['receteuygulamas'] = ReceteFormSet(self.request.POST)
        else:
            data['receteuygulamas'] = ReceteFormSet()
            data['isUpdate'] = False
            data['pk'] = 0
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        receteuygulamas = context['receteuygulamas']
        receteTarihi = form.cleaned_data['receteTarihi']
        hasta = form.cleaned_data['hasta']
        ilac = form.cleaned_data['ilac']
        ayniRecete = Recete.objects.filter(receteTarihi=receteTarihi, hasta=hasta, ilac=ilac)

        if (ayniRecete):
            #raise forms.ValidationError("Bu hasta için %s tarihli %s isimli ilaç reçetesi zaten oluşturulmuş." % (receteTarihi,ilac.piyasaAdi))
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                    u"Bu hasta için %s tarihli %s isimli ilaç reçetesi zaten oluşturulmuş." % (receteTarihi,ilac.piyasaAdi)
            ])
            return self.form_invalid(form)

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
        return reverse('recete:recete-update', kwargs={'pk' : self.object.pk, 'isCreate':'0'})


    def get_context_data(self, **kwargs):
        data = super(ReceteUygulamaUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['receteuygulamas'] = ReceteFormSet(self.request.POST, instance=self.object)
        else:
            data['receteuygulamas'] = ReceteFormSet(instance=self.object)
            data['isUpdate'] = True
            data['isCreate'] = self.kwargs['isCreate']
            data['pk'] = str(self.object.pk)
            
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
        return reverse('recete:recete-list',kwargs={'type' : 2})


def receteDurdur(request,id):
    recete = get_object_or_404(Recete, pk=id)
    recete.durduruldu = True
    recete.durdurulmaTarihi = datetime.datetime.now() + datetime.timedelta(hours=3)
    recete.save()
    return redirect(reverse('recete:recete-list',kwargs={'type' : 2}))

class IlacInfo(object):

    def __init__(self):
        self.ilacAdi=''
        self.toplamMiktar=0
        self.ilacId=None

def addIlac(infoList, recete):
    ilac = IlacInfo()
    ilac.ilacId = recete.ilac.id
    ilac.ilacAdi = recete.ilac.piyasaAdi
    ilac.toplamMiktar = (recete.ilac.ml / recete.ilac.mg) * recete.istenenMiktar

    varmi = False
    if (len(infoList) > 0):
        for i in infoList:
            if i.ilacId == ilac.ilacId:
                varmi = True
                i.toplamMiktar = i.toplamMiktar + ilac.toplamMiktar
            
    if (not  varmi):
        infoList.append(ilac)
    return infoList

def hazirlamaList(request):
    context = {}
    ilacInfo = []
    now = datetime.datetime.now() + datetime.timedelta(hours=3)
    now = now.time()
    context['now'] = now
    hazirnacankTedaviler = []
    bekleyenTedaviler = []

    if(request.method == 'POST'):
        receteTarihi = request.POST.get('receteTarihi', '')
        hazirlamaListesi = Recete.objects.filter(hastane__id=request.session['hastaneId'],receteTarihi=datetime.datetime.strptime(str(receteTarihi), "%d/%m/%Y").date(),hasta__durumTipi__name='AKTİF',durduruldu=False)
        for recete in hazirlamaListesi:
            for saat in recete.uygulamaSaati.all():
                addIlac(ilacInfo,recete)
        context['hazirlamaListesi'] = hazirlamaListesi
        context['infoList'] = ilacInfo
    else:
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        hazirlamaListesi = Recete.objects.filter(hastane__id=request.session['hastaneId'],receteTarihi__range=(today_min, today_max),hasta__durumTipi__name='AKTİF',durduruldu=False)
        context['hazirlamaListesi'] = hazirlamaListesi
        for recete in hazirlamaListesi:
            for saat in recete.uygulamaSaati.all():
                if saat.saat > now:
                    addIlac(ilacInfo,recete)
        context['infoList'] = ilacInfo

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

        
        user = self.request.user
       
        if (user.username == 'erkan' or user.username == 'aysel'): 
            qs = Hasta.objects.all()
        else:
            hastaneId = self.request.session['hastaneId']
            hastane = Hospital.objects.get(pk=hastaneId)
            hastaneKullanici = HospitalUser.objects.get(authorizedUser=user, hospital=hastane)
            qs = Hasta.objects.filter(servisBilgisi=hastaneKullanici.servis)

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
    #uygulama = ReceteUygulama.objects.get(pk=sid)

    hasta_adi = recete.hasta.name + ' ' +recete.hasta.surname
    servis_adi = recete.hasta.servisBilgisi.servisAdi
    tc_no = recete.hasta.tcNo
    ilac_adi = recete.ilac.piyasaAdi
    hazirlama_yeri = recete.uygulamaYolu.adi
    mayi = recete.mayi.name
    istenenMik = recete.istenenMiktar
    hemsireNotu = recete.hemsireNotu
    cekilecekMl = ( recete.ilac.ml * istenenMik ) / recete.ilac.mg
    tamamlanacakMiktar = recete.mayi.miktari - cekilecekMl
    toplamHacim = recete.mayi.miktari
    istenenMikBirimTip = recete.birimTipi.name
    dolumYeri = recete.dolumTipi.name

    toplamMk = recete.ilac.mg
    KalanMk = toplamMk - istenenMik


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
    p.drawString(5, 110, 'Hazirma Yeri: ' + str(dolumYeri))
    p.drawString(5, 95, 'Sulan. Mayisi: ' + mayi)
    #p.drawString(5, 80, 'İstl Mik: ' + str(istenenMik) + ' ' + str(istenenMikBirimTip))
    p.drawString(5,65, 'Not')
    p.drawString(5, 40, '' if hemsireNotu is None else str(hemsireNotu))

    p.drawString(170, 110, 'Toplam Mik: ' + str(toplamMk) + ' Mg')
    p.drawString(170, 95, 'İstenen. Mik: ' + str(istenenMik) + ' ' + str(istenenMikBirimTip))
    p.drawString(170, 80, 'Kalan Mk:' + str(KalanMk) )
    #p.line(165,75,280,75)
    p.drawString(170, 65,'Çekilen Mik: ' + str(cekilecekMl) + ' ML' )

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


