from django.forms import ModelForm, inlineformset_factory,NumberInput, DateInput
from django import forms
from .models import Recete, ReceteUygulama
from core.models import Ilac,Mayi,BirimTipi,SureTipi,UygulamaSaati,UygulamaYolu
from hasta.models import Hasta
from dal import autocomplete

#
class ReceteForm(ModelForm):
    hasta = forms.ModelChoiceField(required=False,queryset=Hasta.objects.all(), widget=autocomplete.ModelSelect2(url='recete:hasta-autocomplete',attrs={'class':'form-control'}), empty_label='Seçiniz')
    ilac = forms.ModelChoiceField(required=False,queryset=Ilac.objects.all(), widget=autocomplete.ModelSelect2(url='recete:ilac-autocomplete',attrs={'class':'form-control'}), empty_label='Seçiniz')
    mayi = forms.ModelChoiceField(required=False,queryset=Mayi.objects.all(), widget=autocomplete.ModelSelect2(url='recete:mayi-autocomplete',attrs={'class':'form-control'}), empty_label='Seçiniz')
    birimTipi = forms.ModelChoiceField(required=False,queryset=BirimTipi.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    sureTipi = forms.ModelChoiceField(required=False,queryset=SureTipi.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    uygulamaSaati = forms.ModelMultipleChoiceField(queryset=UygulamaSaati.objects.all(),widget=forms.CheckboxSelectMultiple)
    uygulamaYolu = forms.ModelChoiceField(required=False,queryset=UygulamaYolu.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')

    class Meta:
        model = Recete
        exclude = ()
        widgets = {
            'istenenMiktar':NumberInput(attrs={'class':'form-control'}),
            'sure':NumberInput(attrs={'class':'form-control'}),
            'receteTarihi': DateInput(attrs={'class':'date-picker  form-control', 'id':'myDatepicker2'})
        }


class ReceteUygulamaForm(ModelForm):
    class Meta:
        model = ReceteUygulama
        exclude = ()


ReceteFormSet = inlineformset_factory(Recete, ReceteUygulama, form=ReceteUygulamaForm, extra=1)