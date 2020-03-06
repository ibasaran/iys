from django.forms import ModelForm, inlineformset_factory,NumberInput, DateInput,TextInput
from django import forms
from hasta.models import Hasta
from dal import autocomplete
import datetime 


class HastaReportForm(forms.Form):
    hasta = forms.ModelChoiceField(required=False,queryset=Hasta.objects.all(), widget=autocomplete.ModelSelect2(url='recete:hasta-autocomplete',attrs={'class':'form-control'}), empty_label='Seçiniz')
    baslangicTarihi = forms.DateField(initial=datetime.date.today)
    bitisTarihi = forms.DateField(initial=datetime.date.today)