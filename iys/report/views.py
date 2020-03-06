from django.shortcuts import render

# Create your views here.



def openReportForm(request):
    return render(request, 'rapor/hastaReport.html', {})