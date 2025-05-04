from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('news/', include('news.urls')),
]
