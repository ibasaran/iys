from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Hospital(models.Model):
    name = models.CharField(max_length=250, verbose_name='Hastane Adı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Hastane'
        


class HospitalUser(models.Model):
    authorizedUser = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.SET_NULL,null=True)

    class Meta:
        verbose_name = 'Hastane Kullanıcı'


class BirimTipi(models.Model):
    name = models.CharField(max_length=250, verbose_name='Birim Adı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Birim Tipi'



class DurumTipi(models.Model):
    name = models.CharField(max_length=250, verbose_name='Durum Adı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Durum Tipi'

class TozBilgileri(models.Model):
    name = models.CharField(max_length=250, verbose_name='Toz Adı')
    solusyon = models.CharField(max_length=250, verbose_name='Sulandırma Solüsyonu')
    birimTipi = models.ForeignKey(BirimTipi,on_delete=models.SET_NULL,null=True)
    durumTipi = models.ForeignKey(DurumTipi,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Toz Bilgisi'


class DolumTipi(models.Model):
    name = models.CharField(max_length=250, verbose_name='Dolum Tipi Adı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Dolum Tipi'


class DolumYeri(models.Model):
    dolumTipi = models.ForeignKey(DolumTipi,on_delete=models.SET_NULL,null=True)
    miktari = models.IntegerField(max_length=25, verbose_name='Miktarı')
    birimTipi = models.ForeignKey(BirimTipi,on_delete=models.SET_NULL,null=True)
    durumTipi = models.ForeignKey(DurumTipi,on_delete=models.SET_NULL,null=True)


    def __str__(self):
        return self.dolumTipi.name + ' ' + str(self.miktari) + ' ' + self.birimTipi.name

    class Meta:
        verbose_name='Dolum Yeri'
