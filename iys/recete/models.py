from django.db import models
from hasta.models import Hasta
from core.models import Ilac, Mayi, BirimTipi,UygulamaYolu,SureTipi,Hospital



class Recete(models.Model):
    hasta = models.ForeignKey(Hasta, on_delete=models.SET_NULL, null=True, blank=True)
    ilac = models.ForeignKey(Ilac, on_delete=models.SET_NULL, null=True, blank=True)
    mayi = models.ForeignKey(Mayi, on_delete=models.SET_NULL, null=True, blank=True)
    istenenMiktar = models.IntegerField(null=True, blank=True, verbose_name='İstenen Miktar')
    birimTipi = models.ForeignKey(BirimTipi, on_delete=models.SET_NULL, null=True, blank=True)
    sure = models.IntegerField(verbose_name='Süre', null=True, blank=True)
    sureTipi = models.ForeignKey(SureTipi, on_delete=models.SET_NULL, null=True, blank=True)
    receteTarihi = models.DateField()
    hastane = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.hasta.name + ' ' + self.hasta.surname + ' ' + self.ilac.adi + ' ' + self.receteTarihi

    class Meta:
        verbose_name = 'Reçete'


class ReceteUygulama(models.Model):
    uygulamaYolu = models.ForeignKey(UygulamaYolu, on_delete=models.SET_NULL, null=True)
    uygulamaSaati = models.TimeField(verbose_name='Uygulama Saati')
    recete = models.ForeignKey(Recete, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.uygulamaYolu.adi + ' ' + self.uygulamaSaati

    class Meta:
        verbose_name='Reçete Uygulama'



