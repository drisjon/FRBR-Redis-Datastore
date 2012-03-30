"""
 mod:`url` FRBR-Redis-Datastore Aristotle base URLS
"""
__author__ = 'Jeremy Nelson'
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^call_number/', include('call_number.urls')),
    url(r'^policies/', include('policies.urls')),
    url(r'^book_search/', include('book_search.urls')),
    url(r'^article_search/', include('article_search.urls')),
    url(r'^portfolio/', include('portfolio.urls')), 
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
