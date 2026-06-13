from django.contrib import admin

from .models import EmployerProfile


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'industry', 'location', 'created_at')
    search_fields = ('company_name', 'user__email', 'user__username')
    raw_id_fields = ('user',)
