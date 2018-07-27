from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.generic import TemplateView
from cryptotrade.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    path('', TemplateView.as_view(template_name='landings/home.html'), name='landing-home'),
    path('admin/', admin.site.urls),
    path('dashboard/', include([
        path('', include('dashboard_cabinet.urls')),
        path('b-trees/', include('binary_tree.urls')),
        path('l-trees/', include('linear_tree.urls')),
        path('accounts/', include('user_profile.urls')),
        path('packages/', include('packages.urls')),
        path('finance/', include('finance.urls')),
        path('news/', include('news.urls')),
    ])),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
