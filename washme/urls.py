from django.conf import settings

from django.conf.urls.static import static

from django.conf.urls import include, url

from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^company/', include('company.urls', namespace='company')),
    url(r'^car/', include('car.urls', namespace='car')),
    url(r'', include('main.urls', namespace='main')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
