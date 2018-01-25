from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
import selfstudy.views

from django.contrib.sitemaps.views import sitemap
from django.conf.urls import handler404, handler500

sitemaps = {
    'static': StaticViewSitemap,
}
# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', selfstudy.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^reset-password/$', auth_views.PasswordResetView.as_view(template_name='user_account/reset-password.html')),
    url(r'^reset-password-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', auth_views.PasswordResetConfirmView.as_view(template_name='user_account/confirm-password-reset.html'), name='password_reset_confirm'),
    url(r'^reset-password-done', auth_views.PasswordResetDoneView.as_view(template_name='user_account/done-password-reset.html'), name='password_reset_done'),
    url(r'^reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name='user_account/complete-password-reset.html'), name='password_reset_complete'),
    url(r'^login/$', selfstudy.views.user_login, name='login'),
    url(r'^logout/$', selfstudy.views.user_logout, name='user-logout'),
    url(r'^register-account/$', selfstudy.views.register, name='register'),
    url(r'^shopping-cart/$', selfstudy.views.cart_view, name='cart'),
    url(r'^checkout/$', selfstudy.views.checkout, name='checkout'),
    url(r'^add-to-cart/$', selfstudy.views.add_to_cart, name='add-to-cart'),
    url(r'^notify/$', selfstudy.views.notify, name='notify'),
    url(r'^cancel/$', selfstudy.views.cancel, name='cancel'),
    url(r'^success/$', selfstudy.views.success, name='success'),
    url(r'^contact/$', selfstudy.views.contact, name='contact'),
    #url(r'about/$', selfstudy.views.about, name='about'),
    url(r'^terms-and-conditions/$', selfstudy.views.terms, name='terms and conditions'),
    url(r'^frequently-asked-questions/$', selfstudy.views.faq, name='faq'),
    url(r'^update-currency/$', selfstudy.views.update_currency, name='currency'),
    url(r'^course-library/(?P<course_id>[0-9]+)/(?P<course_title>[A-Za-z\s:,0-9]+)/detail/$', selfstudy.views.course_library, name='courses'),
    url(r'^course-library/(?P<category_id>[0-9]+)/(?P<category_title>[A-Za-z\s:,0-9]+)/$', selfstudy.views.courses_by_category, name='courses by category'),
    url(r'^course-library/$', selfstudy.views.course_library_main, name='courses-main'),
    url(r'^account/$', selfstudy.views.account, name='account'),
    url(r'^account/my-courses/$', selfstudy.views.my_courses, name='my-courses'),
    url(r'^account/edit/$', selfstudy.views.edit_details, name='user-edit'),
    url(r'^upload-vouchers/$', selfstudy.views.import_data, name='import data')
    
]

handler404 = selfstudy.views.error_404
handler500 = selfstudy.views.error_500