from django.shortcuts import render
from .forms import HastaReportForm
from hasta.models import Hasta
from recete.models import Recete
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

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
        hasta = Hasta.objects.get(pk=hastaId)
        tedaviListesi = Recete.objects.filter(hasta__id=hastaId)
        html_string = render_to_string('rapor/hastaReport.html', {'hasta':hasta, 'tedaviListesi':tedaviListesi})
        html = HTML(string=html_string)
        result = html.write_pdf()

        # Creating http response
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = 'inline; filename=list_people.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'r')
            response.write(output.read())

    return response
    #return render(request, 'rapor/hastaReport.html', {'hasta':hasta, 'tedaviListesi':tedaviListesi})