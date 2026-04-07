from django.contrib import admin

from .models import ServiceHistory, VeterinaryAppointment

admin.site.register(VeterinaryAppointment)
admin.site.register(ServiceHistory)
