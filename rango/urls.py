from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_id>[0-9]+)/$', views.detail, name='detail2'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_id>[0-9]+)/like/$', views.like, name='like'),
    url(r'^category/views/(?P<category_id>[0-9]+)/$', views.increaseView, name='increaseView'),
    url(r'category/likes/(?P<category_id>[0-9]+)/$', views.increaseLike, name='increaseLike'),
    url(r'category/(?P<category_id>[0-9]+)/views/$', views.increaseDetailView, name='increaseDetailView'),
    url(r'category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add/$', views.add_page, name='add_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'logout/$', views.user_logout, name='logout'),
]