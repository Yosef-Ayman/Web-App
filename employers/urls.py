from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='employers_index'),
    path('profile/', views.profile_view, name='employers_profile'),
    path('jobs/', views.jobs_list_view, name='employers_jobs'),
    path('job/create/', views.create_job_view, name='employers_create_job'),
    path('jobs/<int:pk>/edit/', views.edit_job_view, name='employers_edit_job'),
    path('jobs/<int:pk>/delete/', views.delete_job_view, name='employers_delete_job'),
    path('jobs/<int:pk>/applicants/', views.job_applicants_view, name='employers_job_applicants'),
]
