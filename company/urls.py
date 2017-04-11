from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # homepage
    url(r'^photo_delete/(?P<car_wash_id>\d+)/$', views.photo_delete, name='photo_delete'),  # to delete one of my photos
    url(r'^view_car_wash/(?P<car_wash_id>\d+)/$', views.view_car_wash, name='view_car_wash'),
    url(r'^view_car_washes/$', views.view_car_washes, name='view_car_washes'),  # to view list of car washes
    url(r'^new_car_wash/$', views.new_car_wash, name='new_car_wash'),  # to add new carwash
    url(r'^new_box/(?P<company_id>\d+)/$', views.new_box, name='new_box'),  # to add new box
    url(r'^edit_box/(?P<box_id>\d+)/$', views.edit_box, name='edit_box'),  # to edit box status
    url(r'^photo_list/(?P<car_wash_id>\d+)/$', views.photo_list, name='photo_list'),
    url(r'^company_data/$', views.company_dataset, name='company_dataset') # geojson format of carwashes
]