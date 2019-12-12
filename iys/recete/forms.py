from django.forms import ModelForm, inlineformset_factory

from recete.models import Recete, ReceteUygulama


class ReceteForm(ModelForm):
    class Meta:
        model = Recete
        exclude = ()


class ReceteUygulamaForm(ModelForm):
    class Meta:
        model = ReceteUygulama
        exclude = ()


ReceteFormSet = inlineformset_factory(Recete, ReceteUygulama, form=ReceteUygulamaForm, extra=1)