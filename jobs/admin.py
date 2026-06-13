from django.contrib import admin

from .models import Application, Job, JobCategory


@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'job_type', 'category', 'is_active', 'created_at')
    list_filter = ('job_type', 'category', 'is_active', 'location')
    search_fields = ('title', 'description', 'employer__company_name')
    raw_id_fields = ('employer',)


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('applicant__email', 'job__title')
    raw_id_fields = ('applicant', 'job')
