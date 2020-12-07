from django.urls import path
from . import views


urlpatterns = [
    path('signin', views.signin_view),
    path('login', views.login_view),
    path('logout', views.logout_view),
]
