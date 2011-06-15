from django.conf.urls.defaults import patterns, url

from search import views


urlpatterns = patterns('',
    url(r'^$', views.index, name='dashboard'),
    url(r'^$', views.index, name='search'),
    url(r'^search/atom/?$', views.SearchFeed(), name='search.feed'),
)
