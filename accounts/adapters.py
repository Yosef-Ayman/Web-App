from django.urls import reverse

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .services import get_authenticated_home_url


class AccountAdapter(DefaultAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        user.first_name = data.get('first_name') or ''
        user.last_name = data.get('last_name') or ''
        user.email = data.get('email', '')
        user.username = user.email
        return user

    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_authenticated:
            return get_authenticated_home_url(user)
        return reverse('index')

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        user = request.user
        if user.is_authenticated:
            return get_authenticated_home_url(user)
        return reverse('index')