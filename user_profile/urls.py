from django.urls import path
from .views import (
    NewUserByRefCodeView,
    AuthView,
    user_logout,
    UserProfileDetailView,
)


app_name = 'user'
urlpatterns = [
    path('register-by-ref/<str:ref_code>/', NewUserByRefCodeView.as_view(), name='register-by-ref'),
    path('login/', AuthView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', UserProfileDetailView.as_view(), name='profile'),
]
