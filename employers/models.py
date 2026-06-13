from django.conf import settings
from django.db import models


class EmployerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employer_profile',
    )
    company_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=150, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    position = models.CharField(max_length=150, blank=True)
    avatar_image = models.ImageField(upload_to='employers/avatars/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='employers/banners/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company_name']

    def __str__(self):
        return self.company_name
