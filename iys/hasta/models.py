from django.db import models
from core.models import DurumTipi,KurumBilgisi,ServisBilgileri,Cinsiyet


class Hasta(models.Model):
    protokolNo = models.CharField(max_length=500, verbose_name='Protokol Numarası')
    tcNo = models.CharField(max_length=11,verbose_name='T.C. Kimlik Numarası',blank=True,null=True)
    name = models.CharField(max_length=300, verbose_name='Adı',blank=True,null=True)
    surname = models.CharField(max_length=300, verbose_name='Soyadı',blank=True,null=True)
    cinsiyet = models.ForeignKey(Cinsiyet,on_delete=models.SET_NULL,blank=True,null=True)
    dogumTarihi = models.DateField(blank=True,null=True, verbose_name='Doğum Tarihi')
    yasi = models.IntegerField(verbose_name='Yaşı',blank=True,null=True)
    durumTipi = models.ForeignKey(DurumTipi,on_delete=models.SET_NULL,blank=True,null=True)
    boy = models.IntegerField(verbose_name='Boy',blank=True,null=True)
    kilo = models.IntegerField(verbose_name='Kilo',blank=True,null=True)
    vucutYuzeyAlani = models.IntegerField(verbose_name='Vucut Yüzey Alanı',blank=True,null=True)
    kurumBilgisi = models.ForeignKey(KurumBilgisi, on_delete=models.SET_NULL,blank=True,null=True)
    servisBilgisi = models.ForeignKey(ServisBilgileri, on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return  'Hasta Adı ' +  str(self.name) + ' ' + str(self.surname)

    class Meta:
        verbose_name = 'Hasta Bilgileri'
        ordering = ['-id']



