from django.forms import ModelForm, inlineformset_factory,NumberInput, DateInput,TextInput
from django import forms
from .models import Recete, ReceteUygulama
from core.models import Ilac,Mayi,BirimTipi,SureTipi,UygulamaSaati,UygulamaYolu,DolumTipi
from hasta.models import Hasta
from dal import autocomplete


#
class ReceteForm(ModelForm):
    hasta = forms.ModelChoiceField(required=False,queryset=Hasta.objects.all(), widget=autocomplete.ModelSelect2(url='recete:hasta-autocomplete',attrs={'class':'form-control'}), empty_label='Seçiniz')
    ilac = forms.ModelChoiceField(required=False,queryset=Ilac.objects.all(), widget=autocomplete.ModelSelect2(url='recete:ilac-autocomplete',attrs={'class':'form-control'}), empty_label='Seçiniz')
    mayi = forms.ModelChoiceField(required=False,queryset=Mayi.objects.all(), widget=autocomplete.ModelSelect2(url='recete:mayi-autocomplete',attrs={'class':'form-control'}), empty_label='Seçiniz')
    birimTipi = forms.ModelChoiceField(required=False,queryset=BirimTipi.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    dolumTipi = forms.ModelChoiceField(required=False,queryset=DolumTipi.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    sureTipi = forms.ModelChoiceField(required=False,queryset=SureTipi.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    uygulamaSaati = forms.ModelMultipleChoiceField(required=True,queryset=UygulamaSaati.objects.all().order_by('saat'),widget=forms.CheckboxSelectMultiple(attrs={"data-columns":"2"}))
    uygulamaYolu = forms.ModelChoiceField(required=False,queryset=UygulamaYolu.objects.all(), widget=forms.Select(attrs={'class':'form-control'}), empty_label='Seçiniz')
    receteTarihi = forms.DateField(widget=forms.DateInput(format = '%d/%m/%Y',attrs={'class':'form-control'}), 
                               input_formats=('%d/%m/%Y',), 
                               required=False)
    def __init__(self, *args, **kwargs):
        super(ReceteForm, self).__init__(*args, **kwargs)
        self.fields['uygulamaSaati'].error_messages = {'required': 'Uygulama Saati Seçilmelidir.'}
    def clean(self):
        cleaned_data = super().clean()
        id = cleaned_data.get('id')
        mayi = cleaned_data.get('mayi')
        uygulamaSaati = cleaned_data.get('uygulamaSaati')
        uygulamaYolu = cleaned_data.get('uygulamaYolu')
        ilac = cleaned_data.get('ilac')
        hasta = cleaned_data.get('hasta')
        istenenMiktar = cleaned_data.get('istenenMiktar')
        dolumTipi = cleaned_data.get('dolumTipi')
        receteTarihi = cleaned_data.get('receteTarihi')

        if mayi is None:
            raise forms.ValidationError("Mayi Boş Olamaz")

        if uygulamaYolu is None:
            raise forms.ValidationError("Uygulama Yolu Seçilmelidir.")

        if ilac is None:
            raise forms.ValidationError("İlaç Seçilmelidir.")

        if hasta is None:
            raise forms.ValidationError("Hasta Seçilmelidir.")

        if istenenMiktar is None:
            raise forms.ValidationError("İstenen Miktar Belirtilmelidir.")

        if dolumTipi is None:
            raise forms.ValidationError("Dolum Yeri Belirtilmelidir.")

        

    def clean_recipients(self):
        mayi = self.cleaned_data['mayi']
        if mayi is None:
             raise forms.ValidationError("Mayi Boş Olamaz")
    class Meta:
        model = Recete
        exclude = ()
        widgets = {
            'istenenMiktar':NumberInput(attrs={'class':'form-control'}),
            'sure':NumberInput(attrs={'class':'form-control'}),
            #'receteTarihi': DateInput(attrs={'class':'date-picker  form-control', 'id':'myDatepicker2'},format = '%d/%m/%Y'),
            'hemsireNotu': TextInput(attrs={'class':'form-control'}),
        }


class ReceteUygulamaForm(ModelForm):
    class Meta:
        model = ReceteUygulama
        exclude = ()


ReceteFormSet = inlineformset_factory(Recete, ReceteUygulama, form=ReceteUygulamaForm, extra=1)