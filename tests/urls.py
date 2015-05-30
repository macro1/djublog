from django.conf.urls import url

from djublog import views

urlpatterns = [
    url(r'^feed$', views.feed_view, name='ufeed'),
]
