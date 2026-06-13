from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from jobs.models import Application, Job, JobCategory

from .models import EmployerProfile


def employer_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_employer:
            messages.error(request, 'Only employers can access this page.')
            return redirect('index')
        return view_func(request, *args, **kwargs)

    return wrapper


def _get_employer_profile(user):
    profile, _ = EmployerProfile.objects.get_or_create(
        user=user,
        defaults={'company_name': user.get_full_name() or user.email or 'My Company'},
    )
    return profile


def _parse_salary(value):
    value = (value or '').strip()
    return int(value) if value.isdigit() else None


def _jobs_page_context(profile, *, show_create_wizard=False, form_data=None, job=None):
    categories = JobCategory.objects.all().order_by('name')
    ctx = {
        'profile': profile,
        'categories': categories,
        'show_create_wizard': show_create_wizard,
        'form_data': form_data or {},
        'job': job,
    }
    ctx['jobs'] = Job.objects.filter(employer=profile).select_related('category')
    return ctx


@employer_required
def index_view(request):
    profile = _get_employer_profile(request.user)
    jobs = Job.objects.filter(employer=profile).select_related('category')
    total_applications = Application.objects.filter(job__employer=profile).count()
    return render(request, 'employers/index.html', {
        'profile': profile,
        'jobs': jobs[:5],
        'total_jobs': jobs.count(),
        'total_applications': total_applications,
    })


@employer_required
def profile_view(request):
    profile = _get_employer_profile(request.user)
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.last_name = request.POST.get('last_name', user.last_name).strip()
        profile.company_name = request.POST.get('company_name', profile.company_name).strip()
        profile.industry = request.POST.get('industry', profile.industry).strip()
        profile.location = request.POST.get('location', profile.location).strip()
        profile.description = request.POST.get('description', profile.description).strip()
        profile.website = request.POST.get('website', profile.website).strip()
        profile.position = request.POST.get('position', profile.position).strip()

        if 'avatar_image' in request.FILES:
            profile.avatar_image = request.FILES['avatar_image']
        if 'banner_image' in request.FILES:
            profile.banner_image = request.FILES['banner_image']

        user.save()
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('employers_profile')

    return render(request, 'employers/profile.html', {
        'profile': profile,
        'user': user,
    })


@employer_required
def jobs_list_view(request):
    profile = _get_employer_profile(request.user)
    show_create_wizard = request.GET.get('create') == '1'
    ctx = _jobs_page_context(profile, show_create_wizard=show_create_wizard)
    return render(request, 'employers/jobs.html', ctx)


@employer_required
def create_job_view(request):
    profile = _get_employer_profile(request.user)

    if request.method == 'GET':
        return redirect(f'{reverse("employers_jobs")}?create=1')

    title = request.POST.get('title', '').strip()
    location = request.POST.get('location', '').strip()
    job_type = request.POST.get('job_type', 'full').strip()
    category_name = request.POST.get('category', '').strip()
    description = request.POST.get('description', '').strip()
    skills = request.POST.get('skills', '').strip()
    form_data = {
        'title': title,
        'location': location,
        'job_type': job_type,
        'category': category_name,
        'description': description,
        'skills': skills,
        'salary_min': request.POST.get('salary_min', ''),
        'salary_max': request.POST.get('salary_max', ''),
    }

    if not all([title, location, description]):
        messages.error(request, 'Title, location, and description are required.')
        ctx = _jobs_page_context(
            profile,
            show_create_wizard=True,
            form_data=form_data,
        )
        return render(request, 'employers/jobs.html', ctx)

    category = None
    if category_name:
        category, _ = JobCategory.objects.get_or_create(name=category_name)

    Job.objects.create(
        employer=profile,
        title=title,
        location=location,
        job_type=job_type if job_type in dict(Job.JOB_TYPE_CHOICES) else 'full',
        category=category,
        description=description,
        skills=skills,
        salary_min=_parse_salary(form_data['salary_min']),
        salary_max=_parse_salary(form_data['salary_max']),
    )
    messages.success(request, 'Job posted successfully.')
    return redirect('employers_jobs')


@employer_required
def edit_job_view(request, pk):
    profile = _get_employer_profile(request.user)
    job = get_object_or_404(Job.objects.select_related('category'), pk=pk, employer=profile)

    categories = JobCategory.objects.all().order_by('name')

    if request.method == 'POST':
        job.title = request.POST.get('title', job.title).strip()
        job.location = request.POST.get('location', job.location).strip()
        job_type = request.POST.get('job_type', job.job_type).strip()
        if job_type in dict(Job.JOB_TYPE_CHOICES):
            job.job_type = job_type
        category_name = request.POST.get('category', '').strip()
        if category_name:
            job.category, _ = JobCategory.objects.get_or_create(name=category_name)
        elif request.POST.get('category') == '':
            job.category = None
        job.description = request.POST.get('description', job.description).strip()
        job.skills = request.POST.get('skills', job.skills).strip()
        job.salary_min = _parse_salary(request.POST.get('salary_min', ''))
        job.salary_max = _parse_salary(request.POST.get('salary_max', ''))
        job.is_active = request.POST.get('is_active') == 'on'
        job.save()
        messages.success(request, 'Job updated successfully.')
        return redirect('employers_jobs')

    return render(request, 'employers/job_form.html', {
        'profile': profile,
        'categories': categories,
        'job': job,
    })


@employer_required
def delete_job_view(request, pk):
    profile = _get_employer_profile(request.user)
    job = get_object_or_404(Job, pk=pk, employer=profile)

    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('employers_jobs')

    return render(request, 'employers/job_confirm_delete.html', {
        'profile': profile,
        'job': job,
    })


@employer_required
def job_applicants_view(request, pk):
    profile = _get_employer_profile(request.user)
    job = get_object_or_404(Job, pk=pk, employer=profile)
    applications = (
        Application.objects.filter(job=job)
        .select_related('applicant')
        .order_by('-created_at')
    )

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status', '').strip()
        if app_id and new_status in dict(Application.STATUS_CHOICES):
            application = get_object_or_404(Application, pk=app_id, job=job)
            application.status = new_status
            application.save(update_fields=['status', 'updated_at'])
            messages.success(request, 'Application status updated.')
            return redirect('employers_job_applicants', pk=pk)

    return render(request, 'employers/applicants.html', {
        'profile': profile,
        'job': job,
        'applications': applications,
        'status_choices': Application.STATUS_CHOICES,
    })
