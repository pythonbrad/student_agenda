from django.urls import path
from .views import authentification


urlpatterns = [
    path('auth/signin', authentification.signin_view),
    path('auth/login', authentification.login_view),
    path('auth/logout', authentification.logout_view),
]
