from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import selfstudy.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', selfstudy.views.index, name='index'),
    url(r'^db', selfstudy.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', selfstudy.views.user_login, name='user-login'),
    url(r'^logout/', selfstudy.views.user_logout, name='user-logout'),
    url(r'^course-library/(?P<course_id>[0-9]+)/detail/$', selfstudy.views.course_library, name='courses')
]
