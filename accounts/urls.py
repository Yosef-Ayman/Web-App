from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('profile/', views.profile_view, name='profile'),
    path('onboarding/basic/', views.BasicOnboardingView.as_view(), name='onboarding_basic'),
    path('onboarding/job-seeker/', views.JobSeekerOnboardingView.as_view(), name='onboarding_job_seeker'),
    path('onboarding/employer/', views.EmployerOnboardingView.as_view(), name='onboarding_employer'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('check-username/', views.check_username_view, name='check_username'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('help/', views.help_view, name='help'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html', email_template_name='auth/password_reset_email.html', success_url=reverse_lazy('password_reset_done')), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),
]
