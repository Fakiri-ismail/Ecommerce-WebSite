from django.urls import path
from .views import login_view, register_user, register_seller
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', register_user, name="register"),
    path('registerAsSeller/', register_seller, name="registerAsSeller")
]