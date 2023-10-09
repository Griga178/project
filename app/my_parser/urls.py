from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name = 'index'),
    url(r'^links/$', views.LinkListView.as_view(), name = 'links'),
    path('add', views.LinkAddView.as_view(), name = 'add_link')


]
