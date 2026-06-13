from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    role = models.CharField(max_length=10, choices=[('seeker', 'Job Seeker'), ('employer', 'Employer')], blank=False, default='seeker')
    job_title = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=150, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    cv_file = models.FileField(upload_to='cvs/', blank=True, null=True)
    is_employer = models.BooleanField(default=False)
    onboarding_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name() or self.email or self.username
