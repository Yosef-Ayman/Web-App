import re
from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from jobs.models import Application, Job

from .forms import BasicProfileForm, EmployerOnboardingForm, JobSeekerOnboardingForm
from .models import CustomUser
from .services import get_authenticated_home_url, get_onboarding_redirect_url


def job_seeker_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_employer:
            messages.error(request, 'Employer accounts cannot access job seeker pages.')
            return redirect('employers_index')
        return view_func(request, *args, **kwargs)

    return wrapper


def index_view(request):
    if request.user.is_authenticated:
        onboarding_url = get_onboarding_redirect_url(request.user)
        if onboarding_url:
            return redirect(onboarding_url)
        if request.user.is_employer:
            return redirect('employers_index')

    jobs = (
        Job.objects.filter(is_active=True)
        .select_related('employer', 'category')[:9]
    )

    context = {'jobs': jobs}

    if request.user.is_authenticated and not request.user.is_employer:
        applications = (
            Application.objects.filter(applicant=request.user)
            .select_related('job', 'job__employer')
            .order_by('-created_at')[:5]
        )
        context['applications'] = applications
        context['total_applications'] = Application.objects.filter(applicant=request.user).count()
        context['hired_count'] = Application.objects.filter(applicant=request.user, status='hired').count()
        context['in_review_count'] = Application.objects.filter(applicant=request.user, status='in_review').count()

    return render(request, 'index.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect(get_authenticated_home_url(request.user))

    if request.method == 'POST':
        first_name = re.sub(r'\s+', '', request.POST.get('first_name', '')).strip()
        last_name = re.sub(r'\s+', '', request.POST.get('last_name', '')).strip()
        email = request.POST.get('email', '').strip().lower()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        gender = request.POST.get('gender', '')
        is_employer = request.POST.get('is_employer') == '1'

        if not all([first_name, last_name, email, password1, password2]):
            messages.error(request, 'All required fields must be filled.')
            return render(request, 'auth/register.html')
        email_re = re.compile(r'^[^\s@]+@[^\s@]+\.[^\s@]{2,}$')
        if not email_re.match(email):
            messages.error(request, 'Enter a valid email address (e.g. you@example.com).')
            return render(request, 'auth/register.html')
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'auth/register.html')
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'auth/register.html')
        if CustomUser.objects.filter(email__iexact=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'auth/register.html')

        username = email
        role = 'employer' if is_employer else 'seeker'
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            gender=gender if gender in ('M', 'F') else '',
            is_employer=is_employer,
            role=role,
        )


        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Account created successfully.')
        return redirect(get_authenticated_home_url(user))

    return render(request, 'auth/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_authenticated_home_url(request.user))

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None and '@' in username:
            try:
                existing = CustomUser.objects.get(email__iexact=username)
                user = authenticate(request, username=existing.username, password=password)
            except CustomUser.DoesNotExist:
                user = None

        if user is not None:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            onboarding_url = get_onboarding_redirect_url(user)
            if onboarding_url:
                return redirect(onboarding_url)
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect(get_authenticated_home_url(user))

        messages.error(request, 'Invalid email or password.')

    return render(request, 'auth/login.html', {'form': type('Form', (), {'non_field_errors': [], 'username': type('F', (), {'errors': []})(), 'password': type('F', (), {'errors': []})()})()})


def check_username_view(request):
    username = request.GET.get('username', '').strip()
    available = not CustomUser.objects.filter(username__iexact=username).exists()
    return JsonResponse({'available': available})


def logout_view(request):
    logout(request)
    return redirect('index')


class BasicOnboardingView(View):
    template_name = 'onboarding/basic.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        next_url = get_onboarding_redirect_url(request.user)
        if not next_url:
            return redirect(get_authenticated_home_url(request.user))
        if next_url != request.path:
            return redirect(next_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': BasicProfileForm(instance=request.user)})

    def post(self, request):
        form = BasicProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account details are updated.')
            return redirect(get_authenticated_home_url(request.user))
        return render(request, self.template_name, {'form': form})


class JobSeekerOnboardingView(View):
    template_name = 'onboarding/job_seeker.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_employer:
            return redirect(get_authenticated_home_url(request.user))
        next_url = get_onboarding_redirect_url(request.user)
        if not next_url:
            return redirect(get_authenticated_home_url(request.user))
        if next_url != request.path:
            return redirect(next_url)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': JobSeekerOnboardingForm(instance=request.user)})

    def post(self, request):
        form = JobSeekerOnboardingForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.onboarding_complete = True
            user.save()
            messages.success(request, 'Your job seeker profile is ready.')
            return redirect(get_authenticated_home_url(user))
        return render(request, self.template_name, {'form': form})


class EmployerOnboardingView(View):
    template_name = 'onboarding/employer.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_employer:
            return redirect(get_authenticated_home_url(request.user))
        next_url = get_onboarding_redirect_url(request.user)
        if not next_url:
            return redirect(get_authenticated_home_url(request.user))
        if next_url != request.path:
            return redirect(next_url)
        return super().dispatch(request, *args, **kwargs)

    def get_profile(self):
        from employers.models import EmployerProfile
        try:
            return self.request.user.employer_profile
        except EmployerProfile.DoesNotExist:
            return None

    def get(self, request):
        profile = self.get_profile()
        return render(request, self.template_name, {'form': EmployerOnboardingForm(instance=profile), 'profile': profile})

    def post(self, request):
        profile = self.get_profile()
        form = EmployerOnboardingForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile_instance = form.save(commit=False)
            if profile_instance.user_id is None:
                profile_instance.user = request.user
            profile_instance.save()
            request.user.onboarding_complete = True
            request.user.save(update_fields=['onboarding_complete'])
            messages.success(request, 'Your employer profile is ready.')
            return redirect(get_authenticated_home_url(request.user))
        return render(request, self.template_name, {'form': form, 'profile': profile})


@job_seeker_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        if 'cv_upload' in request.FILES:
            user.cv_file = request.FILES['cv_upload']
            user.save(update_fields=['cv_file'])
            messages.success(request, 'CV updated successfully.')
            return redirect('profile')

        user.first_name = request.POST.get('first_name', user.first_name).strip()
        user.last_name = request.POST.get('last_name', user.last_name).strip()
        user.job_title = request.POST.get('job_title', user.job_title).strip()
        user.location = request.POST.get('location', user.location).strip()
        username = request.POST.get('username', user.username).strip()
        if username and not CustomUser.objects.filter(username=username).exclude(pk=user.pk).exists():
            user.username = username
        if 'profile_photo' in request.FILES:
            user.profile_photo = request.FILES['profile_photo']
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    applications = (
        Application.objects.filter(applicant=user)
        .select_related('job', 'job__employer', 'job__category')
    )
    summary = applications.aggregate(
        applied=Count('id'),
        in_review=Count('id', filter=Q(status='in_review')),
        hired=Count('id', filter=Q(status='hired')),
        rejected=Count('id', filter=Q(status='rejected')),
    )
    latest = applications.first()

    return render(request, 'profile.html', {
        'user': user,
        'applications': applications,
        'summary': summary,
        'latest': latest,
        'total': applications.count(),
    })


def about_view(request):
    return render(request, 'about.html')


def contact_view(request):
    return render(request, 'contact.html')


def help_view(request):
    return render(request, 'help.html')


def privacy_view(request):
    return render(request, 'privacy.html')


def terms_view(request):
    return render(request, 'terms.html')


def bad_request_view(request, exception=None):
    return render(request, 'errors/400.html', status=400)


def permission_denied_view(request, exception=None):
    return render(request, 'errors/403.html', status=403)


def page_not_found_view(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def server_error_view(request):
    return render(request, 'errors/500.html', status=500)