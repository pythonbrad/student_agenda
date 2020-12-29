from django.urls import path
from .views import authentification, user, administrator


urlpatterns = [
    path('auth/signin', authentification.signin_view),
    path('auth/login', authentification.login_view),
    path('auth/logout', authentification.logout_view),
    path('user/timetable/follow', user.get_timetable_follow_by_me_view),
    path('user/timetable/follow/<int:timetable_pk>', user.follow_timetable_view),
    path('user/timetable', user.get_timetable_view),
    path('user/timetable/<int:timetable_pk>/course', user.get_timetable_course_view),
    path('admin/timetable/create', administrator.create_timetable_view),
]
