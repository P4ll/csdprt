from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from landings.views import index

urlpatterns = [
    path('', index, name='index'),
    path('captcha/', include('captcha.urls')),
    path('admin/', admin.site.urls),
    path('persons/', include('persons.urls')),
    path('accounts/', include('accounts.urls')),
    path('landings/', include('landings.urls')),
    path('blog/', include('blog.urls')),
]

if settings.DEVELOPMENT_MODE:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
