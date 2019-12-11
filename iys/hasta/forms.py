from django.forms import ModelForm, Textarea, NumberInput, DateInput, Select, TextInput
from hasta.models import Hasta
from django import forms
from core.models import Cinsiyet, DurumTipi,ServisBilgileri,KurumBilgisi


class HastaForm(ModelForm):
    kurumBilgisi = forms.ModelChoiceField(required=False,queryset=KurumBilgisi.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    servisBilgisi = forms.ModelChoiceField(required=False,queryset=ServisBilgileri.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    cinsiyet = forms.ModelChoiceField(required=False,queryset=Cinsiyet.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    durumTipi = forms.ModelChoiceField(required=False,queryset=DurumTipi.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')

    class Meta:
        model = Hasta
        fields = ['protokolNo', 'tcNo', 'name', 'surname', 'cinsiyet', 'dogumTarihi', 'yasi', 'durumTipi', 'boy','kilo','vucutYuzeyAlani','kurumBilgisi','servisBilgisi']
        widgets = {
            'protokolNo': TextInput(attrs={'class':'form-control'}),
            'tcNo': NumberInput(attrs={'class':'form-control'}),
            'name':TextInput(attrs={'class':'form-control'}),
            'surname': TextInput(attrs={'class':'form-control'}),
            'dogumTarihi': DateInput(attrs={'class':'form-control'}),
            'yasi': NumberInput(attrs={'class':'form-control'}),
            'boy': NumberInput(attrs={'class':'form-control'}),
            'kilo': NumberInput(attrs={'class':'form-control'}),
            'vucutYuzeyAlani': NumberInput(attrs={'class':'form-control'}),
        }