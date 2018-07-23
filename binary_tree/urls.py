from django.urls import path
from .views import (
    BinaryTreeView,
    PointsHistoryListView,
)

app_name = 'binary_tree'
urlpatterns = [
    path('binar/', BinaryTreeView.as_view(), name='binary_tree'),
    path('points-history/', PointsHistoryListView.as_view(), name='points-history'),
]
