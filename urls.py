from django.conf.urls.defaults import *
#from first.alpha.views import print_Header, contact
from first.alpha.chat import getMsg
from first.alpha.index import index
from django.contrib.auth.views import login, logout
from first.alpha.register import register


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
        (r'chat',getMsg),
        (r'accounts/login',login), 
        (r'accounts/logout',logout),
        (r'accounts/register',register),
        (r'accounts/profile',getMsg),

        (r'',index)
 )



    # Example:
    # (r'^first/', include('first.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

