from django.urls import path
from . import views


urlpatterns = [
    path('signin', views.authentification.signin_view),
    path('login', views.authentification.login_view),
    path('logout', views.authentification.logout_view),
]
