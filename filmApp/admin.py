from django.contrib import admin

from filmApp.models import Aktyor, Kino, Tarif, Izoh

admin.site.register(Aktyor)
admin.site.register(Kino)
# admin.site.register(Tarif)
admin.site.register(Izoh)


@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'narx', 'davomiylik']

