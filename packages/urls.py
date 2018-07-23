from django.urls import path
from .views import (
    PackageListView,
    ByPackageFormView,
)

app_name = 'package'
urlpatterns = [
    path('', PackageListView.as_view(), name='packages-list'),
    path('buy-package/<int:package_id>', ByPackageFormView.as_view(), name='buy-package'),
]
