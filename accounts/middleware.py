from django.shortcuts import redirect
from django.urls import Resolver404, resolve

from .services import get_onboarding_redirect_url


class OnboardingRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.should_redirect(request):
            onboarding_url = get_onboarding_redirect_url(request.user)
            if onboarding_url and request.path != onboarding_url:
                return redirect(onboarding_url)
        return self.get_response(request)

    def should_redirect(self, request):
        user = getattr(request, 'user', None)
        if user is None or not user.is_authenticated:
            return False

        path = request.path_info
        if path.startswith(('/admin/', '/static/', '/media/', '/accounts/')):
            return False

        try:
            match = resolve(path)
        except Resolver404:
            return False
        url_name = match.url_name
        if url_name == 'logout':
            return False
        if url_name in {'onboarding_basic', 'onboarding_job_seeker', 'onboarding_employer'}:
            return False
        if url_name in {'bad_request', 'permission_denied', 'page_not_found', 'server_error'}:
            return False
        if url_name in {'login', 'register', 'check_username', 'logout',
                        'password_reset', 'password_reset_done',
                        'password_reset_confirm', 'password_reset_complete'}:
            return False
        return get_onboarding_redirect_url(user) is not None
