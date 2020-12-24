from django.urls import path
from .views import authentification


urlpatterns = [
    path('signin', authentification.signin_view),
    path('login', authentification.login_view),
    path('logout', authentification.logout_view),
]
