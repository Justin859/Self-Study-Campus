from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

import selfstudy.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', selfstudy.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reset-password/$', auth_views.PasswordResetView.as_view(template_name='user_account/reset-password.html')),
    url(r'^reset-password-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', auth_views.PasswordResetConfirmView.as_view(template_name='user_account/confirm-password-reset.html'), name='password_reset_confirm'),
    url(r'^reset-password-done', auth_views.PasswordResetDoneView.as_view(template_name='user_account/done-password-reset.html'), name='password_reset_done'),
    url(r'^reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name='user_account/complete-password-reset.html'), name='password_reset_complete'),
    url(r'^login/$', selfstudy.views.user_login, name='user-login'),
    url(r'^logout/$', selfstudy.views.user_logout, name='user-logout'),
    url(r'^register-account/$', selfstudy.views.register, name='register'),
    url(r'^shopping-cart/$', selfstudy.views.cart_view, name='cart'),
    url(r'^checkout/$', selfstudy.views.checkout, name='checkout'),
    url(r'^notify/$', selfstudy.views.notify, name='notify'),
    url(r'^cancel/$', selfstudy.views.cancel, name='cancel'),
    url(r'^success/$', selfstudy.views.success, name='success'),
    url(r'^update-currency/$', selfstudy.views.update_currency, name='currency'),
    url(r'^course-library/(?P<course_id>[0-9]+)/(?P<course_title>[A-Za-z\s:,0-9]+)/detail/$', selfstudy.views.course_library, name='courses'),
    url(r'^account/my-courses/$', selfstudy.views.my_courses, name='my-courses'),
    url(r'^account/edit/$', selfstudy.views.edit_details, name='user-edit'),
    url(r'^upload-vouchers/$', selfstudy.views.import_data, name='import data')
    
]
