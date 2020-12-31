from django.urls import path
from .views import authentification, user, administrator


urlpatterns = [
    path('auth/signin', authentification.signin_view),
    path('auth/login', authentification.login_view),
    path('auth/logout', authentification.logout_view),
    path('user/timetable/follow', user.get_timetable_follow_by_me_view),
    path('user/timetable/<int:timetable_pk>/follow/', user.follow_timetable_view),
    path('user/timetable', user.get_timetable_view),
    path('user/timetable/<int:timetable_pk>/classe', user.get_timetable_classes_view),
    path('admin/timetable/add', administrator.add_timetable_view),
    path('admin/timetable/course/<int:course_pk>/lesson/add', administrator.add_timetable_classe_view),
    path('admin/timetable/<int:timetable_pk>/lecturer/add', administrator.add_timetable_lecturer_view),
    path('admin/timetable/<int:timetable_pk>/location/add', administrator.add_timetable_location_view),
]
