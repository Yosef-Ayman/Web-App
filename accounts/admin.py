from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_employer', 'is_staff')
    list_filter = ('is_employer', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Jobify Profile', {
            'fields': ('gender', 'job_title', 'location', 'profile_photo', 'cv_file', 'is_employer'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Jobify Profile', {'fields': ('is_employer',)}),
    )
