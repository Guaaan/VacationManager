from django.contrib import admin
from .models import VacationRequest

@admin.register(VacationRequest)
class VacationRequestAdmin(admin.ModelAdmin):
    list_display = ('user','start_date','end_date','days_requested','status','created_at')
    list_filter = ('status',)
