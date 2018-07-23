from django.urls import path
from .views import (
    LinearTreeListView,
)

app_name = 'linear_tree'
urlpatterns = [
    path('linear/', LinearTreeListView.as_view(), name='linear_tree'),
]
