from django.conf.urls import url 
from . import views
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^create/$', views.create, name = 'create'),
    url(r'^secrets/$', views.secrets, name = 'secrets'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^popular/$', views.popular, name = 'popular'),
    url(r'^add/$', views.add, name = 'add'),
    url(r'^logout/$', views.logout, name= 'logout'),
    url(r'^like/(?P<id>\d+)$', views.like, name = 'like'),
]