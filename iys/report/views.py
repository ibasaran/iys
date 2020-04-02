# -*- coding: utf-8 -*-

from django.shortcuts import render
from .forms import HastaReportForm, DurumRaporu
from hasta.models import Hasta
from recete.models import Recete
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.utils import timezone
import datetime
from decimal import Decimal

# Create your views here.



def openReportForm(request):
    hastaRerportForm = HastaReportForm()
    return render(request, 'rapor/hastaReportForm.html', {'form':hastaRerportForm})



def openReport(request):
    hasta = None
    tedaviListesi = None
    if (request.POST):
        hastaRerportForm = HastaReportForm(request.POST)
        hastaId = request.POST['hasta']
        baslangicTarihi = request.POST['baslangicTarihi']
        print(baslangicTarihi)
        if (baslangicTarihi is None ):
            baslangicTarihi = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date()
        else:
            baslangicTarihi = str(baslangicTarihi)
            baslangicTarihi = datetime.datetime.strptime(baslangicTarihi, '%d/%m/%Y').date()
        bitisTarihi = request.POST['bitisTarihi']
        if (bitisTarihi is None):
            bitisTarihi = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        else:
            bitisTarihi = str(bitisTarihi)
            bitisTarihi = datetime.datetime.strptime(bitisTarihi, '%d/%m/%Y').date()
        hasta = Hasta.objects.get(pk=hastaId)
        

        #baslangicTarihi = datetime.datetime.combine(baslangicTarihi, datetime.time.min)
        #bitisTarihi = datetime.datetime.combine(bitisTarihi, datetime.time.max)

        tedaviListesi = Recete.objects.filter(hasta__id=hastaId, receteTarihi__range=(baslangicTarihi, bitisTarihi))
        print(tedaviListesi.query)
        template = get_template('rapor/hastaReport.html')
        html = template.render({'hasta':hasta, 'tedaviListesi':tedaviListesi, 'today': timezone.now()})
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(str(html).encode('utf-8')), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)
    else:
        return render(request, 'rapor/hastaReport.html', {'hasta':hasta, 'tedaviListesi':tedaviListesi})
    #return render(request, 'rapor/hastaReport.html', {'hasta':hasta, 'tedaviListesi':tedaviListesi})



def durumReportForm(request):
    durumForm = DurumRaporu()
    return render(request, 'rapor/durum/durumForm.html', {'form':durumForm})


class IlacInfo(object):
    
    def __init__(self):
        self.ilacAdi=''
        self.toplamMiktar=0
        self.ilacId=None
        self.ilacMik=0
        self.toplamIstenenMik=0
        self.toplamKalanMik=0
        self.toplamKarEdilenIlacSayisi=0


def addIlac(infoList, recete):
    ilac = IlacInfo()
    ilac.ilacId = recete.ilac.id
    ilac.ilacAdi = recete.ilac.piyasaAdi
    ilac.ilacMik = recete.ilac.mg
    ilac.toplamIstenenMik = ilac.toplamIstenenMik + recete.istenenMiktar
    ilac.toplamKalanMik = ilac.toplamKalanMik + (recete.ilac.mg -  recete.istenenMiktar)
    ilac.toplamKarEdilenIlacSayisi = ilac.toplamKalanMik / ilac.ilacMik
    if (recete.ilac.fiyat):
        ilac.toplamKar = Decimal(ilac.toplamKarEdilenIlacSayisi) * recete.ilac.fiyat

    varmi = False
    if (len(infoList) > 0):
        for i in infoList:
            if i.ilacId == ilac.ilacId:
                varmi = True
                i.toplamMiktar = i.toplamMiktar + ilac.toplamMiktar
            
    if (not  varmi):
        infoList.append(ilac)
    return infoList    

def durumReport(request):
    if (request.POST):
        baslangicTarihi = request.POST['baslangicTarihi']
        if (baslangicTarihi is None ):
            baslangicTarihi = datetime.datetime.strptime('2000-01-01', '%Y-%m-%d').date()
        else:
            baslangicTarihi = str(baslangicTarihi)
            baslangicTarihi = datetime.datetime.strptime(baslangicTarihi, '%d/%m/%Y').date()
        bitisTarihi = request.POST['bitisTarihi']
        if (bitisTarihi is None):
            bitisTarihi = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        else:
            bitisTarihi = str(bitisTarihi)
            bitisTarihi = datetime.datetime.strptime(bitisTarihi, '%d/%m/%Y').date()
        receteler = Recete.objects.filter(receteTarihi__range=(baslangicTarihi, bitisTarihi))
        toplamReceteSayisi = 0
        toplamUygulananTedaviSayisi = 0
        toplamHastaSayisi = 0
        toplamKar = 0
        ilacInfo = []

        for recete in receteler:
            for saat in recete.uygulamaSaati.all():
                addIlac(ilacInfo,recete)
                toplamUygulananTedaviSayisi = toplamUygulananTedaviSayisi + 1

        template = get_template('rapor/durum/durumReport.html')
        html = template.render({'ilacInfo':ilacInfo, 
            'toplamHastaSayisi':toplamHastaSayisi, 
            'today': timezone.now(),
            'toplamReceteSayisi':toplamReceteSayisi,
            'toplamUygulananTedaviSayisi':toplamUygulananTedaviSayisi})
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(str(html).encode('utf-8')), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

        





        
