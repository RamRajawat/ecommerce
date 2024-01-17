from django_hosts import patterns, host
from django.contrib import admin
from . import urls


host_patterns = patterns('',
    host(r'www','ecommerce.urls', name='www'),
    # host(r'www','' , include('app.urls'),name='www'),
    host(r'admin/', admin.site.urls, name='admin'),
)