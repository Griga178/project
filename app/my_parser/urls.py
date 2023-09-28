from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name = 'index'),
    # path('', views.LinkListView.as_view(), name = 'links'),
    url(r'^links/$', views.LinkListView.as_view(), name = 'links'),
    # url(r'^links/$', views.LinkListView.as_view(), name = 'links'),
]

# urlpatterns += [
#     url(r'^link/new/$', views.new_link, name='renew-book-librarian'),
# ]
