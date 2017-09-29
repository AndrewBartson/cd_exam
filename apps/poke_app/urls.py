from django.conf.urls import url

from . import views          

urlpatterns = [ 
    url(r'^$', views.dashboard),
    url(r'^add/(?P<id>\d+)$', views.add),  
]