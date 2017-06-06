from django.conf.urls import url
from . import views

urlpatterns = [
    #url(r'^$', views.post_list, name='post_list'),
    url(r'^$', views.post_srr, name='post_srr'),
    #url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^job_new/$', views.post_srr, name='post_srr'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.job_status, name='job_status'),
    url(r'^dst_detail/(?P<pk>[0-9]+)/$', views.dst_detail, name='dst_detail'),

    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
]
