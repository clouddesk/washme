from django.conf.urls import url

from . import views

urlpatterns = [
    # homepage
    url(r'^$', views.main, name='main'),  # to view main page
]