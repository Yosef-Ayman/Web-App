from django.urls import path

from . import views

urlpatterns = [
    path('', views.jobs_list_view, name='jobs'),
    path('apply/<int:pk>/', views.apply_job_view, name='apply_job'),
    path('<int:pk>/', views.job_detail_view, name='job_detail'),
]
