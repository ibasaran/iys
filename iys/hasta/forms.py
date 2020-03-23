from django.forms import ModelForm, Textarea, NumberInput, DateInput, Select, TextInput
from hasta.models import Hasta
from django import forms
from core.models import Cinsiyet, DurumTipi,ServisBilgileri,KurumBilgisi

class DateInput(forms.DateInput):
    input_type = 'text'

class HastaForm(ModelForm):
    kurumBilgisi = forms.ModelChoiceField(required=False,queryset=KurumBilgisi.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    servisBilgisi = forms.ModelChoiceField(required=False,queryset=ServisBilgileri.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    cinsiyet = forms.ModelChoiceField(required=False,queryset=Cinsiyet.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    durumTipi = forms.ModelChoiceField(required=False,queryset=DurumTipi.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    dogumTarihi = forms.DateField(widget=DateInput( format = '%d/%m/%Y',attrs={'class':'form-control', 'size':10,'pattern':"\d{1,2}/\d{1,2}/\d{4}",'oninput':"this.value = DDMMYYYY(this.value, event)", 'placeholder':'GÜN/AY/YIL'}), 
                               input_formats=('%d/%m/%Y',),
                               required=False)
    class Meta:
        model = Hasta
        fields = ['protokolNo', 'tcNo', 'name', 'surname', 'cinsiyet', 'dogumTarihi', 'yasi', 'durumTipi', 'boy','kilo','vucutYuzeyAlani','kurumBilgisi','servisBilgisi']
        widgets = {
            'protokolNo': TextInput(attrs={'class':'form-control','required':'required'}),
            'tcNo': TextInput(attrs={'class':'form-control','required':'required','onblur':'tckimlikkontorolu(this);', 'maxlength':'11'}),
            'name':TextInput(attrs={'class':'form-control','required':'required'}),
            'surname': TextInput(attrs={'class':'form-control','required':'required'}),
            #'dogumTarihi': DateInput(format=('%d/%m/%Y'),attrs={'class':' date-picker form-control','onchange':'calculateAge(this.value)'}),
            'yasi': NumberInput(attrs={'class':'form-control'}),
            'boy': NumberInput(attrs={'class':'form-control'}),
            'kilo': NumberInput(attrs={'class':'form-control'}),
            'vucutYuzeyAlani': TextInput(attrs={'class':'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        servisBilgisi = cleaned_data.get('servisBilgisi')

        if servisBilgisi is None:
            print('SERVIS BİLGİSİ BOS OLAMAZ')
            raise forms.ValidationError("Servis Bilgisi Boş Olamaz")