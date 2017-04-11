from django.conf.urls import url

from . import views

urlpatterns = [
    # homepage
    url(r'^my_cars/delete_car/(?P<car_id>\d+)/$', views.delete_car, name='delete_car'),  # to delete one of my cars
    url(r'^my_cars/new_car/$', views.new_car, name='new_car'),  # to view list of my cars
    url(r'^my_cars/$', views.view_my_cars, name='view_my_cars'),  # to view list of my cars
    #    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    #    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    #    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    #    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]
