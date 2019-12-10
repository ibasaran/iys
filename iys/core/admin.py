from django.contrib import admin
from core.models import Hospital, HospitalUser, BirimTipi,DurumTipi, TozBilgileri,DolumTipi,DolumYeri

admin.site.register(Hospital)
admin.site.register(HospitalUser)
admin.site.register(BirimTipi)
admin.site.register(DurumTipi)
admin.site.register(TozBilgileri)
admin.site.register(DolumTipi)
admin.site.register(DolumYeri)