from django.contrib import admin

from .models import CarWash, Box

from leaflet.admin import LeafletGeoAdmin


class CarWashAdmin(LeafletGeoAdmin):
    list_display = ('name', 'location')

admin.site.register(CarWash, CarWashAdmin)
admin.site.register(Box)