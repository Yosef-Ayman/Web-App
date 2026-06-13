from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.views import job_seeker_required

from .models import Application, Job, JobCategory


def jobs_list_view(request):
    if request.user.is_authenticated and request.user.is_employer:
        return redirect('employers_index')

    queryset = Job.objects.filter(is_active=True).select_related('employer', 'category')

    query = request.GET.get('q', '').strip()
    selected_type = request.GET.get('job_type', '').strip()
    selected_category = request.GET.get('category', '').strip()
    selected_location = request.GET.get('location', '').strip()

    if query:
        queryset = queryset.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(employer__company_name__icontains=query)
            | Q(location__icontains=query)
        )
    if selected_type:
        queryset = queryset.filter(job_type=selected_type)
    if selected_category:
        queryset = queryset.filter(category__name=selected_category)
    if selected_location:
        queryset = queryset.filter(location=selected_location)

    jobs = list(queryset)
    categories = list(
        JobCategory.objects.filter(jobs__is_active=True)
        .distinct()
        .order_by('name')
        .values_list('name', flat=True)
    )
    locations = list(
        Job.objects.filter(is_active=True)
        .exclude(location='')
        .values_list('location', flat=True)
        .distinct()
        .order_by('location')
    )

    applied_job_ids = set()
    if request.user.is_authenticated and not request.user.is_employer:
        applied_job_ids = set(
            Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)
        )

    return render(request, 'jobs.html', {
        'jobs': jobs,
        'total': len(jobs),
        'query': query,
        'selected_type': selected_type,
        'selected_category': selected_category,
        'selected_location': selected_location,
        'categories': categories,
        'locations': locations,
        'applied_job_ids': applied_job_ids,
    })


def job_detail_view(request, pk):
    if request.user.is_authenticated and request.user.is_employer:
        return redirect('employers_index')

    job = get_object_or_404(
        Job.objects.select_related('employer', 'category'),
        pk=pk,
        is_active=True,
    )
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(applicant=request.user, job=job).exists()

    return render(request, 'apply.html', {
        'job': job,
        'skills_list': job.skills_list(),
        'already_applied': already_applied,
    })


@job_seeker_required
def apply_job_view(request, pk):
    job = get_object_or_404(
        Job.objects.select_related('employer', 'category'),
        pk=pk,
        is_active=True,
    )

    if Application.objects.filter(applicant=request.user, job=job).exists():
        return render(request, 'apply.html', {
            'job': job,
            'skills_list': job.skills_list(),
            'already_applied': True,
        })

    if request.method == 'POST':
        cv_file = request.FILES.get('cv_file')
        if cv_file:
            request.user.cv_file = cv_file
            request.user.save(update_fields=['cv_file'])

        Application.objects.create(
            applicant=request.user,
            job=job,
            cv_file=request.user.cv_file,
        )
        messages.success(request, 'Application submitted successfully.')
        return redirect('profile')

    return render(request, 'apply.html', {
        'job': job,
        'skills_list': job.skills_list(),
        'already_applied': False,
    })

