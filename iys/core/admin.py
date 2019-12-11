from django.contrib import admin
from core.models import Hospital, HospitalUser, BirimTipi,DurumTipi, TozBilgileri,DolumTipi,DolumYeri,Mayi,Ilac,UygulamaYolu,ServisBilgileri,Cinsiyet,KurumBilgisi,SureTipi

admin.site.register(Hospital)
admin.site.register(HospitalUser)
admin.site.register(BirimTipi)
admin.site.register(DurumTipi)
admin.site.register(TozBilgileri)
admin.site.register(DolumTipi)
admin.site.register(DolumYeri)
admin.site.register(Mayi)
admin.site.register(Ilac)
admin.site.register(UygulamaYolu)
admin.site.register(ServisBilgileri)
admin.site.register(Cinsiyet)
admin.site.register(KurumBilgisi)
admin.site.register(SureTipi)