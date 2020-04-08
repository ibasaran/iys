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
import math

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
        self.toplamKar=0
        self.kullanilanIlac=0
        self.percentage=0
        self.hastaSayisi=0
        self.eczaneMg = 0
        self.eczaneIlcSayisi = 0
        self.tedaviSayisi = 0

class HastaInfo(object):
    def __init__(self):
        self.ilacAdi=''
        self.hastaAdi = ''
        self.istenenMik = 0
        self.ilacMik = 0
        self.kalanMik = 0


def addHasta(hastaList, recete):
    hastaInfo = HastaInfo()
    hastaInfo.ilacAdi = recete.ilac.piyasaAdi
    hastaInfo.hastaAdi = recete.hasta.name + ' ' + recete.hasta.surname
    hastaInfo.istenenMik = recete.istenenMiktar
    hastaInfo.ilacMik = recete.ilac.mg
    if (recete.ilac.mg -  recete.istenenMiktar) < 0:
        hastaInfo.kalanMik = recete.ilac.mg * 2  - recete.istenenMiktar
    else:
        hastaInfo.kalanMik = recete.ilac.mg - recete.istenenMiktar
    hastaList.append(hastaInfo)

def addIlac(infoList, recete):
    ilac = IlacInfo()
    ilac.ilacId = recete.ilac.id
    ilac.ilacAdi = recete.ilac.piyasaAdi
    ilac.ilacMik = recete.ilac.mg
    
    
    varmi = False
    if (len(infoList) > 0):
        for i in infoList:
            if i.ilacId == ilac.ilacId:
                varmi = True
                ilac.tedaviSayisi = ilac.tedaviSayisi + 1
                ilac.eczaneMg = ilac.eczaneMg + recete.ilac.mg
                ilac.eczaneIlcSayisi = ilac.eczaneIlcSayisi + 1
                i.toplamIstenenMik = i.toplamIstenenMik + recete.istenenMiktar
                if (recete.ilac.mg -  recete.istenenMiktar) < 0:
                    i.toplamKalanMik = i.toplamKalanMik + (recete.ilac.mg * 2  -  recete.istenenMiktar)
                else:
                    i.toplamKalanMik = i.toplamKalanMik + (recete.ilac.mg -  recete.istenenMiktar)
                i.toplamKarEdilenIlacSayisi = math.ceil(i.toplamKalanMik / ilac.ilacMik)
                i.kullanilanIlac = math.ceil(i.toplamIstenenMik / ilac.ilacMik)
                i.percentage = (100 * i.toplamKarEdilenIlacSayisi) / (i.toplamKarEdilenIlacSayisi + i.kullanilanIlac)
                if (recete.ilac.fiyat):
                    i.toplamKar = Decimal(i.toplamKarEdilenIlacSayisi) * recete.ilac.fiyat
                    

            
    if (not  varmi):
        ilac.toplamIstenenMik = ilac.toplamIstenenMik + recete.istenenMiktar
        ilac.toplamKalanMik = ilac.toplamKalanMik + (recete.ilac.mg -  recete.istenenMiktar)
        ilac.toplamKarEdilenIlacSayisi = math.ceil(ilac.toplamKalanMik / ilac.ilacMik)
        ilac.kullanilanIlac = math.ceil(ilac.toplamIstenenMik / ilac.ilacMik)
        ilac.percentage = (100 * ilac.toplamKarEdilenIlacSayisi) / (ilac.toplamKarEdilenIlacSayisi + ilac.kullanilanIlac)
        ilac.tedaviSayisi = ilac.tedaviSayisi + 1
        ilac.eczaneMg = ilac.eczaneMg + recete.ilac.mg
        ilac.eczaneIlcSayisi = ilac.eczaneIlcSayisi + 1
        if (recete.ilac.fiyat):
            ilac.toplamKar = Decimal(ilac.toplamKarEdilenIlacSayisi) * recete.ilac.fiyat
            
        infoList.append(ilac)
    return infoList    

def durumReport(request):
    ilacInfo = []
    toplamReceteSayisi = 0
    toplamUygulananTedaviSayisi = 0
    toplamHastaSayisi = 0
    toplamKar = 0
    toplamArtirilanIlacAdeti = 0
    toplamKullanilanIlacAdeti = 0
    genelYuzde = 0
    toplamEczIlcSayisi = 0
    hastaList = []
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
        toplamHastaSayisi = Hasta.objects.count()
        for recete in receteler:
            toplamReceteSayisi = toplamReceteSayisi + 1
            for saat in recete.uygulamaSaati.all():
                addIlac(ilacInfo,recete)
                addHasta(hastaList,recete)
                toplamUygulananTedaviSayisi = toplamUygulananTedaviSayisi + 1


        for ilc in ilacInfo:
            toplamArtirilanIlacAdeti = toplamArtirilanIlacAdeti + ilc.toplamKarEdilenIlacSayisi
            toplamKullanilanIlacAdeti = toplamKullanilanIlacAdeti + ilc.kullanilanIlac
            toplamKar = toplamKar + ilc.toplamKar
            toplamEczIlcSayisi = toplamEczIlcSayisi + ilc.eczaneIlcSayisi

        genelYuzde = math.ceil((100 * toplamArtirilanIlacAdeti) / (toplamArtirilanIlacAdeti + toplamKullanilanIlacAdeti))

        if request.POST.get('detay',False):
            template = get_template('rapor/durum/durumReportDetail.html')
        else:
            template = get_template('rapor/durum/durumReport.html')
        html = template.render({'ilacInfo':ilacInfo, 
            'toplamHastaSayisi':toplamHastaSayisi, 
            'today': timezone.now(),
            'toplamReceteSayisi':toplamReceteSayisi,
            'toplamUygulananTedaviSayisi':toplamUygulananTedaviSayisi,
            'toplamArtirilanIlacAdeti':toplamArtirilanIlacAdeti,
            'hastaList':hastaList,
            'genelYuzde':genelYuzde,
            'toplamKullanilanIlacAdeti':toplamKullanilanIlacAdeti,
            'toplamKar':toplamKar,
            'toplamEczIlcSayisi':toplamEczIlcSayisi})
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(str(html).encode('utf-8')), response)
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)
    else:
        return render(request, 'rapor/durum/durumReport.html', {'ilacInfo':ilacInfo, 
            'toplamHastaSayisi':toplamHastaSayisi, 
            'today': timezone.now(),
            'toplamReceteSayisi':toplamReceteSayisi,
            'toplamUygulananTedaviSayisi':toplamUygulananTedaviSayisi})


        





        
