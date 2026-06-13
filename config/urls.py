from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('accounts/signup/', RedirectView.as_view(url='/register/', permanent=False)),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),
    path('employers/', include('employers.urls')),
]

handler400 = 'accounts.views.bad_request_view'
handler403 = 'accounts.views.permission_denied_view'
handler404 = 'accounts.views.page_not_found_view'
handler500 = 'accounts.views.server_error_view'

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
