# -*- coding: utf-8 -*-

from django.shortcuts import render
from .forms import HastaReportForm
from hasta.models import Hasta
from recete.models import Recete
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from django.utils import timezone
import datetime

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