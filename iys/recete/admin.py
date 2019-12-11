from django.contrib import admin
from recete.models import Recete, ReceteUygulama


class ReceteUygulamaInline(admin.StackedInline):
    model = ReceteUygulama
    extra = 1

class ReceteAdmin(admin.ModelAdmin):
    inlines = [ReceteUygulamaInline,]

admin.site.register(Recete,ReceteAdmin)
#admin.site.register(ReceteUygulama)

