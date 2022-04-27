from django.contrib import admin
from .models import Lottery, Ticket, Report

admin.site.register(Lottery)
admin.site.register(Ticket)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text')