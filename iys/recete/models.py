from django.db import models
from hasta.models import Hasta
from core.models import Ilac, Mayi, BirimTipi,UygulamaYolu,SureTipi,Hospital,UygulamaSaati,DolumTipi
from django.core.exceptions import ValidationError


class Recete(models.Model):
    hasta = models.ForeignKey(Hasta, on_delete=models.SET_NULL, null=True, blank=True)
    ilac = models.ForeignKey(Ilac, on_delete=models.SET_NULL, null=True, blank=True)
    mayi = models.ForeignKey(Mayi, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sulandırma Mayisi")
    istenenMiktar = models.IntegerField(null=True, blank=True, verbose_name='İstenen İlaç Miktarı')
    birimTipi = models.ForeignKey(BirimTipi, on_delete=models.SET_NULL, null=True, blank=True)
    #sure = models.IntegerField(verbose_name='Süre', null=True, blank=True)
    #sureTipi = models.ForeignKey(SureTipi, on_delete=models.SET_NULL, null=True, blank=True)
    receteTarihi = models.DateField()
    hastane = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    uygulamaSaati = models.ManyToManyField(UygulamaSaati)
    uygulamaYolu = models.ForeignKey(UygulamaYolu, on_delete=models.SET_NULL, null=True)
    hemsireNotu = models.CharField(max_length=250, verbose_name='Hemşire Notu',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dolumTipi = models.ForeignKey(DolumTipi,on_delete=models.SET_NULL, null=True, blank=True)


    # def clean(self):
    #     if self.mayi is None:
    #         print('Mayi Seçilmemiş')
    #         raise ValidationError('Mayi Seçiniz')
    
    def __str__(self):
        return str(self.hasta.name) or '' + ' ' + str(self.hasta.surname) or '' + ' ' + str(self.ilac.piyasaAdi) or ''

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


