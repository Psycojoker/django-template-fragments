from django.conf.urls import patterns, url

from views import fragments

urlpatterns = patterns('',
    url(r'^fragments.js$', fragments, name='fragments'),
)
