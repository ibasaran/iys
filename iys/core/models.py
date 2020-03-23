from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Hospital(models.Model):
    name = models.CharField(max_length=250, verbose_name='Hastane Adı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Hastane'


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

class ServisBilgileri(models.Model):
    servisAdi = models.CharField(max_length=250, verbose_name='Servis Adı')
    durumTipi = models.ForeignKey(DurumTipi,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.servisAdi

    class Meta:
        verbose_name='ServisBilgileri'

class HospitalUser(models.Model):
    authorizedUser = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.SET_NULL,null=True)
    servis = models.ForeignKey(ServisBilgileri,on_delete=models.SET_NULL,null=True)

    class Meta:
        verbose_name = 'Hastane Kullanıcı'

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
        verbose_name='Dolum Yeri'


class DolumYeri(models.Model):
    dolumTipi = models.ForeignKey(DolumTipi,on_delete=models.SET_NULL,null=True)
    miktari = models.IntegerField( verbose_name='Miktarı')
    birimTipi = models.ForeignKey(BirimTipi,on_delete=models.SET_NULL,null=True)
    durumTipi = models.ForeignKey(DurumTipi,on_delete=models.SET_NULL,null=True)


    def __str__(self):
        return self.dolumTipi.name + ' ' + str(self.miktari) + ' ' + self.birimTipi.name

    class Meta:
        verbose_name='Dolum Yeri'

class Mayi(models.Model):
    name = models.CharField(max_length=250, verbose_name='Mayi Adı')
    miktari = models.IntegerField( verbose_name='Miktarı')
    birimTipi = models.ForeignKey(BirimTipi,on_delete=models.SET_NULL,null=True)
    durumTipi = models.ForeignKey(DurumTipi,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.name + ' ' + str(self.miktari) + ' ' + self.birimTipi.name

    class Meta:
        verbose_name='Mayi'
        ordering = ['-id']

class Ilac(models.Model):
    etkenMadde = models.CharField(max_length=250, verbose_name='Etken Madde')
    #adi = models.CharField(max_length=250, verbose_name='İlaç Adı')
    piyasaAdi = models.CharField(max_length=250, verbose_name='Piyasa Adı')
    esdegerIlac = models.CharField(max_length=250, verbose_name='Eşdeğer İlaç')
    mg = models.IntegerField( verbose_name='Mg')
    ml = models.IntegerField( verbose_name='Ml')
    #dolumYeri = models.ForeignKey(DolumYeri,on_delete=models.SET_NULL,null=True)
    birimTipi = models.ForeignKey(BirimTipi,on_delete=models.SET_NULL,null=True)
    durumTipi = models.ForeignKey(DurumTipi,on_delete=models.SET_NULL,null=True)
    saklamaKosulu = models.TextField(max_length=500, verbose_name='Saklama Koşulu')
    uyari = models.TextField(max_length=500, verbose_name='Uyari')


    def __str__(self):
        return self.piyasaAdi + ' ' + str(self.etkenMadde) + ' ' + self.piyasaAdi

    class Meta:
        verbose_name='İlaç'
        ordering = ['-id']


class UygulamaYolu(models.Model):
    adi = models.CharField(max_length=250, verbose_name='Uygulama Yolu Adı')
    durumTipi = models.ForeignKey(DurumTipi,on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return self.adi

    class Meta:
        verbose_name='Uygulama Yolu'


class Cinsiyet(models.Model):
    name = models.CharField(max_length=50,verbose_name='Cinsiyet Adı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Cinsiyet'


class KurumBilgisi(models.Model):
    name = models.CharField(max_length=250, verbose_name='Kurum Adı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Kurum Bilgisi'


class SureTipi(models.Model):
    name = models.CharField(max_length=250, verbose_name='Süre Tipi Adı')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Süre Tipi'


class UygulamaSaati(models.Model):
    saat = models.TimeField(verbose_name='Uygulama Saati')
    #recete = models.ManyToManyField(Recete, blank=True)

    def __str__(self):
        return str(self.saat)

    class Meta:
        verbose_name='Uygulama Saati'